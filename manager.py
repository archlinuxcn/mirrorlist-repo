#!/usr/bin/python3

import sys
import time
import argparse
import pprint
from urllib.parse import urlparse, urlunparse, quote
import socket
from ipaddress import ip_address, IPv4Address, IPv6Address
from http.client import HTTPConnection, HTTPSConnection
from collections import OrderedDict
import logging
import json

import yaml  # in python-yaml package


SOURCE_YAML = "mirrors.yaml"
OUTPUT_README = "README.md"
OUTPUT_MIRRORLIST = "archlinuxcn-mirrorlist"
OUTPUT_GEOJSON = "geolocs.json"

README_ITEM_TEMPLATE = """```ini
## {title}{comments}
[archlinuxcn]
Server = {url}$arch
```
"""

MIRRORLIST_ITEM_TEMPLATE = """\
## {title}
# Server = {url}$arch
"""

README_TEMPLATE = """## Arch Linux CN Community repo mirrors list

Here is a list of public mirrors of our [community repository](https://github.com/archlinuxcn/repo).

If you interested in making a mirror of our repository, please open an issue or pull request (or contact us at repo@archlinuxcn.org and hope the mail reaches).

{}

## Arch Linux CN Community repo debuginfod configuration

(This is included in our `archlinuxcn-mirrorlist-git` package.)

```bash
cp -v archlinuxcn.urls /etc/debuginfod/
```
"""

## ordered_load/dump_yaml from https://stackoverflow.com/a/21912744
def ordered_load_yaml(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

def ordered_dump_yaml(data, stream=None, Dumper=yaml.Dumper, **kwds):
    class OrderedDumper(Dumper):
        pass
    def _dict_representer(dumper, data):
        return dumper.represent_mapping(
            yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
            data.items())
    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    return yaml.dump(data, stream, OrderedDumper, **kwds)

def mirror_score(m):
    if m['provider'] == 'CDN':
        return 1000

    try:
        protocols = m['protocols']
    except KeyError:
        return 0

    score = 0
    if 'https' in protocols:
        score += 100
    if 'ipv6' in protocols:
        score += 100
    if 'http' in protocols and 'https' not in protocols:
        score += 10
    if 'ipv4' in protocols:
        score += 10

    return score

def mirror_title(item):
    title = f'{item["provider"]}'
    if "location" in item:
        title += f' ({item["location"]})'
    if "protocols" in item:
        title += " ({})".format(", ".join(item["protocols"]))
    return title


def mirror_comments(item):
    comments = []
    if "added_date" in item:
        comments.append(f'## Added: {item["added_date"]}')
    if "comment" in item:
        comments.append(f"## {item['comment']}")
    if comments:
        return '\n' + '\n'.join(comments)
    else:
        return ''


def readme_item(item):
    return README_ITEM_TEMPLATE.format(
        title=mirror_title(item), comments=mirror_comments(item), **item)


def gen_readme(mirrors):
    with open(OUTPUT_README, 'w') as output:
        readme_items = [
            readme_item(item) for item in mirrors
            if {'http', 'https'} & set(item['protocols'])
        ]
        print(README_TEMPLATE.format('\n'.join(readme_items)), file=output)


def mirrorlist_item(item):
    return MIRRORLIST_ITEM_TEMPLATE.format(
        title=mirror_title(item), **item)


def gen_mirrorlist(mirrors):
    with open(OUTPUT_MIRRORLIST, 'w') as output:
        print(f"""\
##
## Arch Linux CN community repository mirrorlist
## Generated on {time.strftime('%Y-%m-%d')}
##
""", file=output)

        print("\n".join(
            mirrorlist_item(item) for item in mirrors
            if {'http', 'https'} & set(item['protocols'])
        ), file=output, end='')


def sub_readme(args):
    with open(SOURCE_YAML, 'r') as source:
        try:
            mirrors = ordered_load_yaml(source)
            # mirrors.sort(key=lambda m: -mirror_score(m))
            gen_readme(mirrors)
        except yaml.YAMLError as e:
            sys.exit(repr(e))


def sub_mirrorlist(args):
    with open(SOURCE_YAML, 'r') as source:
        try:
            mirrors = ordered_load_yaml(source)
            # mirrors.sort(key=lambda m: -mirror_score(m))
            gen_mirrorlist(mirrors)
        except yaml.YAMLError as e:
            sys.exit(repr(e))


def sub_list(args):
    with open(SOURCE_YAML, 'r') as source:
        try:
            mirrors = ordered_load_yaml(source)
            pprint.pprint(mirrors)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)


def try_connect(domain, url, connection):
    try:
        http = connection(domain, timeout=5)
        http.request('GET', url.path, headers={
            'User-Agent': 'curl/8.0.1',
        })
        res = http.getresponse()
        if res.status == 200:
            return True
    except Exception:
        return False


def try_protocols(mirror):
    url = urlparse(mirror['url'])
    domain = url.hostname
    protocols = []
    print('Accessing "{provider}" at "{domain}": ... '.format(
        domain=domain, **mirror), end='', flush=True)

    try:
        for (family, _, _, _, sockaddr) in socket.getaddrinfo(domain, 80):
            ip = sockaddr[0]
            ipa = ip_address(ip)
            if ipa.is_global:
                if type(ipa) is IPv4Address and 'ipv4' not in protocols:
                    protocols.append("ipv4")
                if type(ipa) is IPv6Address and 'ipv6' not in protocols:
                    protocols.append("ipv6")
        protocols.sort()
    except socket.gaierror:
        pass
    else:
        if try_connect(domain, url, HTTPConnection):
            protocols.append("http")
            url = url._replace(scheme='http')
        if try_connect(domain, url, HTTPSConnection):
            protocols.append("https")
            url = url._replace(scheme='https')

    print(", ".join(protocols))
    mirror['protocols'] = protocols
    mirror['url'] = urlunparse(url)


def sub_protocols(args):
    mirrors = []
    with open(SOURCE_YAML, 'r') as source:
        try:
            mirrors = ordered_load_yaml(source)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)
    for m in mirrors:
        try_protocols(m)
    with open(SOURCE_YAML, "w") as output:
        print(ordered_dump_yaml(mirrors, encoding=None, allow_unicode=True,
                        default_flow_style=False), file=output)


def sub_all(args):
    sub_protocols(args)
    sub_readme(args)
    sub_mirrorlist(args)


def geoencoding(session, loc):
    res = session.get(
        'https://nominatim.openstreetmap.org/search?q=%s&format=jsonv2' % quote(loc),
        headers = {
            'User-Agent': 'archlinuxcn/mirrorlist-repo updater/0.1',
        },
    )
    geo = res.json()[0]
    logging.info('%s is at (%s, %s)', loc, geo['lat'], geo['lon'])
    return '%(lat)s, %(lon)s' % geo


def sub_geo(args):
    mirrors = []
    import requests
    session = requests.Session()
    with open(SOURCE_YAML, 'r') as source:
        try:
            mirrors = ordered_load_yaml(source)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)
    places = {}
    for m in mirrors:
        locs = m.get('geolocs')
        coords = m.get('geocoords')
        if locs and coords and len(locs) == len(coords):
            places.update(zip(locs, coords))
    for m in mirrors:
        locs = m.get('geolocs')
        coords = m.get('geocoords')
        if not locs:
            continue
        if locs and coords and len(locs) == len(coords):
            continue
        coords = []
        for loc in locs:
            coord = places.get(loc)
            if not coord:
                coord = places[loc] = geoencoding(session, loc)
            coords.append(coord)
        m['geocoords'] = coords
    with open(SOURCE_YAML, "w") as output:
        print(ordered_dump_yaml(mirrors, encoding=None, allow_unicode=True,
                        default_flow_style=False), file=output)


def sub_geojson(args):
    features = []
    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }
    with open(SOURCE_YAML, 'r') as source:
        try:
            mirrors = ordered_load_yaml(source)
            # mirrors.sort(key=lambda m: -mirror_score(m))
        except yaml.YAMLError as e:
            sys.exit(repr(e))

    for m in mirrors:
        coords = m.get('geocoords')
        if not coords:
            continue
        locs = m['geolocs']
        for loc, coord in zip(locs, coords):
            lat, lon = coord.split(', ')
            feature = {
                "type": "Feature",
                "properties": {
                    "mirror": m['provider'],
                    "url": m['url'],
                    "name": loc,
                },
                "geometry": {
                    "type": "Point",
                    "coordinates": [float(lon), float(lat)],
                }
            }
            features.append(feature)

    with open(OUTPUT_GEOJSON, 'w') as f:
        json.dump(geojson, f, ensure_ascii=False)


def main():
    parser = argparse.ArgumentParser(
        description='update mirrors protocols and generate mirrorlist and README.md')
    sub = parser.add_subparsers()
    listparser = sub.add_parser('list', help=f'list mirrors in {SOURCE_YAML}')
    listparser.set_defaults(func=sub_list)
    protparser = sub.add_parser(
        'protocols', help='try access to URLs of the mirrors and update the protocols')
    protparser.set_defaults(func=sub_protocols)
    readmeparser = sub.add_parser(
        'readme', help=f'generate {OUTPUT_README} from {SOURCE_YAML}')
    readmeparser.set_defaults(func=sub_readme)
    mirrorlistparser = sub.add_parser(
        'mirrorlist', help=f'generate {OUTPUT_MIRRORLIST} from {SOURCE_YAML}')
    mirrorlistparser.set_defaults(func=sub_mirrorlist)
    allparser = sub.add_parser('all', help='do all 3 above')
    allparser.set_defaults(func=sub_all)
    geoparser = sub.add_parser(
        'geo', help=f'update geo coordinates for {SOURCE_YAML}')
    geoparser.set_defaults(func=sub_geo)
    geojsonparser = sub.add_parser(
        'geojson', help=f'generate {OUTPUT_GEOJSON} for {SOURCE_YAML}')
    geojsonparser.set_defaults(func=sub_geojson)

    args = parser.parse_args()
    if 'func' not in args:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == '__main__':
    try:
        import nicelogger
        nicelogger.enable_pretty_logging('INFO')
    except ImportError:
        pass
    main()

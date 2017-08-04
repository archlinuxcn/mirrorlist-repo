#!/usr/bin/env python3

import sys
import argparse
import pprint
from urllib.parse import urlparse, urlunparse
import socket
from ipaddress import ip_address, IPv4Address, IPv6Address
from http.client import HTTPConnection, HTTPSConnection
from collections import OrderedDict

import yaml  # in python-yaml package


SOURCE_YAML = "mirrors.yaml"
OUTPUT_README = "README.md"
OUTPUT_MIRRORLIST = "archlinuxcn-mirrorlist"

README_ITEM_TEMPLATE = """```ini
## {title}
[archlinuxcn]
Server = {url}$arch
{comments}```
"""

MIRRORLIST_ITEM_TEMPLATE = """
## {title}
#Server = {url}$arch
"""

README_TEMPLATE = """### Arch Linux CN Community repo mirrors list

Here is a list of public mirrors of our [community repository](https://github.com/archlinuxcn/repo).

If you interested in making a mirror of our repository, please contact us at repo@archlinuxcn.org.

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

def mirror_title(item):
    title = f'{item["provider"]}'
    if "location" in item:
        title += f' ({item["location"]})'
    if "protocols" in item:
        title += " ({})".format(", ".join(item["protocols"]))
    return title


def mirror_comments(item):
    comments = ""
    if "added_date" in item:
        comments += f'## Added: {item["added_date"]}\n'
    return comments


def readme_item(item):
    return README_ITEM_TEMPLATE.format(
        title=mirror_title(item), comments=mirror_comments(item), **item)


def gen_readme(mirrors):
    with open(OUTPUT_README, 'w') as output:
        readme_items = [readme_item(item) for item in mirrors]
        print(README_TEMPLATE + '\n'.join(readme_items), file=output)


def mirrorlist_item(item):
    return MIRRORLIST_ITEM_TEMPLATE.format(
        title=mirror_title(item), **item)


def gen_mirrorlist(mirrors):
    with open(OUTPUT_MIRRORLIST, 'w') as output:
        print("".join(mirrorlist_item(item) for item in mirrors), file=output)


def sort_mirrors_by_protocol(mirrors):
    def sort_key(mirror):
        key = 0
        if 'https' in mirror['protocols']:
            key -= 2
        if 'ipv6' in mirror['protocols']:
            key -= 1
        return key
    mirrors.sort(key=sort_key)


def sub_readme(args):
    with open(SOURCE_YAML, 'r') as source:
        try:
            mirrors = ordered_load_yaml(source)
            sort_mirrors_by_protocol(mirrors)
            gen_readme(mirrors)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)


def sub_mirrorlist(args):
    with open(SOURCE_YAML, 'r') as source:
        try:
            mirrors = ordered_load_yaml(source)
            sort_mirrors_by_protocol(mirrors)
            gen_mirrorlist(mirrors)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)


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
        http = HTTPConnection(domain)
        http.request('GET', '/' + url.path)
        res = http.getresponse()
        if res.status == 200:
            return True
    except:
        return False


def try_protocols(mirror):
    url = urlparse(mirror['url'])
    domain = url.hostname
    protocols = []
    print('Accessing "{provider}" at "{domain}": ... '.format(
        domain=domain, **mirror), end='', flush=True)

    for (family, _, _, _, sockaddr) in socket.getaddrinfo(domain, 80):
        ip = sockaddr[0]
        ipa = ip_address(ip)
        if ipa.is_global:
            if type(ipa) is IPv4Address and 'ipv4' not in protocols:
                protocols.append("ipv4")
            if type(ipa) is IPv6Address and 'ipv6' not in protocols:
                protocols.append("ipv6")

    if try_connect(domain, url, HTTPConnection):
        protocols.append("http")
    if try_connect(domain, url, HTTPSConnection):
        protocols.append("https")
        url = tuple(['https', *url[1:]])  # change the scheme to https
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

    args = parser.parse_args()
    if 'func' not in args:
        parser.print_help()
        sys.exit(1)
    args.func(args)


if __name__ == '__main__':
    main()

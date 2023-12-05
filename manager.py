#!/usr/bin/python3

import argparse
import datetime
import re
import socket
import sys
from urllib.parse import urlparse, urlunparse

import httpx  # in python-httpx and python-h2 packages
import orjson  # in python-orjson package
import ruamel.yaml  # in python-ruamel-yaml package

SOURCE_YAML = "mirrors.yaml"
OUTPUT_README = "README.md"
OUTPUT_MIRRORLIST = "archlinuxcn-mirrorlist"
OUTPUT_GEOJSON = "mirrors.geojson"

README_ITEM_TEMPLATE = """\
### {provider}

```ini
## {title}{comments}
[archlinuxcn]
Server = {url}$arch
```
"""

MIRRORLIST_ITEM_TEMPLATE = """\
## {title}{comments}
# Server = {url}$arch
"""

README_TEMPLATE = """\
# Arch Linux CN Community Repository Mirrors

Here is a list of public mirrors of [our community repository](https://github.com/archlinuxcn/repo).

## Usage

Simply install the `archlinuxcn-mirrorlist` package.

To help you choose the best mirror, you can view the [list of mirrors](https://archlinuxcn.org/mirrors/list.html), the [map of mirrors](https://archlinuxcn.org/mirrors/map.html) and the [synchronization status of mirrors](https://build.archlinuxcn.org/grafana/d/iK2vLpGGk/mirrors).

### Debuginfod Configuration

```bash
cp -v archlinuxcn.urls /etc/debuginfod/
```

## Apply Mirror

If you are interested in applying mirror of our repository, please refer to the [application.md](application.md) for instructions.

## Mirrors
"""


def mirror_title(item):
    return f'{item["provider"]} ({item["region"]}) ({", ".join(item["protocols"])})'


def mirror_comments(item):
    return f'\n## {item["comment"]}' if "comment" in item else ""


def readme_item(item):
    return README_ITEM_TEMPLATE.format(
        title=mirror_title(item), comments=mirror_comments(item), **item
    )


def generate_readme(mirrors):
    with open(OUTPUT_README, "w", encoding="utf-8") as output:
        print(
            README_TEMPLATE,
            file=output,
        )
        print(
            ("\n".join(readme_item(item) for item in mirrors)),
            file=output,
            end="",
        )


def mirrorlist_item(item):
    return MIRRORLIST_ITEM_TEMPLATE.format(
        title=mirror_title(item), comments=mirror_comments(item), **item
    )


def generate_mirrorlist(mirrors):
    with open(OUTPUT_MIRRORLIST, "w", encoding="utf-8") as output:
        print(
            f"""\
##
## Arch Linux CN Community Repository mirrorlist
## Generated on {datetime.date.today()}
##
""",
            file=output,
        )
        print(
            "\n".join(mirrorlist_item(item) for item in mirrors),
            file=output,
            end="",
        )


def sub_readme(args):
    with open(SOURCE_YAML, encoding="utf-8") as source:
        try:
            mirrors = ruamel.yaml.YAML(typ="safe").load(source)["archlinuxcn"]
        except ruamel.yaml.YAMLError as error:
            sys.exit(repr(error))
    generate_readme(mirrors)


def sub_mirrorlist(args):
    with open(SOURCE_YAML, encoding="utf-8") as source:
        try:
            mirrors = ruamel.yaml.YAML(typ="safe").load(source)["archlinuxcn"]
        except ruamel.yaml.YAMLError as error:
            sys.exit(repr(error))
    generate_mirrorlist(mirrors)


def sub_list(args):
    with open(SOURCE_YAML, encoding="utf-8") as source:
        try:
            mirrors = ruamel.yaml.YAML(typ="safe").load(source)["archlinuxcn"]
        except ruamel.yaml.YAMLError as error:
            sys.exit(repr(error))
    for i, m in enumerate(mirrors, start=1):
        print(f'{i:02d}. {m["provider"]}')


def get_http_connection(url, provider):
    protocols = set()
    for ssl_verify, http_connection in (
        (False, "http"),
        (True, "https"),
    ):
        try:
            client = httpx.Client(
                headers={"User-Agent": "curl/8.5.0"},
                verify=ssl_verify,
                timeout=10,
            )
            response = client.head(f"{http_connection}://{url.hostname}{url.path}")
            if response.status_code == httpx.codes.OK:
                protocols.add(http_connection)
            response.raise_for_status()
        except (httpx.HTTPError, httpx.InvalidURL) as error:
            print(provider, http_connection, error)
    return protocols


def get_ip_version(url, provider):
    protocols = set()
    socket.setdefaulttimeout(10)
    for socket_family, ip_version in (
        (socket.AF_INET, "ipv4"),
        (socket.AF_INET6, "ipv6"),
    ):
        try:
            if socket.getaddrinfo(url.hostname, 443, socket_family):
                protocols.add(ip_version)
        except OSError as error:
            print(provider, ip_version, error)
    return protocols


def update_protocols(mirrors):
    for m in mirrors:
        url = urlparse(m["url"])
        provider = m["provider"]
        m["protocols"] = sorted(
            get_http_connection(url, provider) | get_ip_version(url, provider)
        )
        m["url"] = urlunparse(url)


def sub_protocols(args):
    mirrors = []
    yaml = ruamel.yaml.YAML()
    with open(SOURCE_YAML, encoding="utf-8") as source:
        try:
            mirrors = yaml.load(source)["archlinuxcn"]
        except ruamel.yaml.YAMLError as error:
            sys.exit(repr(error))
    update_protocols(mirrors)
    with open(SOURCE_YAML, "w", encoding="utf-8") as output:
        yaml.explicit_start = True
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.dump({"archlinuxcn": mirrors}, output)


def get_coordinates(client, loc):
    try:
        params = dict(
            zip(["city", "state", "country"][-len(loc.split(", ")) :], loc.split(", "))
        )
        params["format"] = "jsonv2"
        params["limit"] = "1"
        response = client.get(
            "https://nominatim.openstreetmap.org/search", params=params
        )
        if not response.json():
            raise ValueError(f"Invalid location for {loc}")
    except (httpx.HTTPError, httpx.InvalidURL) as error:
        sys.exit(repr(error))
    return f'{response.json()[0]["lat"]}, {response.json()[0]["lon"]}'


def update_coordinates(mirrors):
    places = {}
    client = httpx.Client(
        headers={"User-Agent": "curl/8.5.0"},
        http2=True,
    )
    for m in mirrors:
        locs = m.get("location")
        coords = m.get("coordinates")
        if locs is coords is None:
            continue
        coords = []
        for loc in locs:
            if loc not in places:
                places[loc] = get_coordinates(client, loc)
            coords.append(places[loc])
        m["coordinates"] = coords


def sub_coordinates(args):
    mirrors = []
    yaml = ruamel.yaml.YAML()
    with open(SOURCE_YAML, encoding="utf-8") as source:
        try:
            mirrors = yaml.load(source)["archlinuxcn"]
        except ruamel.yaml.YAMLError as error:
            sys.exit(repr(error))
    update_coordinates(mirrors)
    with open(SOURCE_YAML, "w", encoding="utf-8") as output:
        yaml.explicit_start = True
        yaml.indent(mapping=2, sequence=4, offset=2)
        yaml.dump({"archlinuxcn": mirrors}, output)


def generate_geojson(mirrors):
    features = []
    geojson = {
        "type": "FeatureCollection",
        "features": features,
    }
    for m in mirrors:
        locs = m.get("location")
        coords = m.get("coordinates")
        if locs is coords is None:
            continue
        for loc, coord in zip(locs, coords, strict=True):
            lat, lon = map(float, coord.split(", "))
            features.append(
                {
                    "type": "Feature",
                    "properties": {
                        "provider": m["provider"],
                        "url": m["url"],
                        "location": loc,
                    },
                    "geometry": {
                        "type": "Point",
                        "coordinates": [lon, lat],
                    },
                }
            )
    return geojson


def sub_geojson(args):
    with open(SOURCE_YAML, encoding="utf-8") as source:
        try:
            mirrors = ruamel.yaml.YAML(typ="safe").load(source)["archlinuxcn"]
        except ruamel.yaml.YAMLError as error:
            sys.exit(repr(error))
    geojson = generate_geojson(mirrors)
    with open(OUTPUT_GEOJSON, "w", encoding="utf-8") as output:
        print(
            re.sub(
                r"(\[\n\s+)(.*)(,\n\s+)(.*)(\n\s+\])",
                r"[\2, \4]",
                orjson.dumps(geojson, option=orjson.OPT_INDENT_2).decode("utf8"),
            ),
            file=output,
        )


def sub_all(args):
    sub_list(args)
    sub_protocols(args)
    sub_readme(args)
    sub_mirrorlist(args)
    sub_coordinates(args)
    sub_geojson(args)


def main():
    parser = argparse.ArgumentParser(
        description="Manage files of Arch Linux CN Community Repository mirrorlist"
    )
    sub = parser.add_subparsers()
    listparser = sub.add_parser("list", help=f"List mirrors from {SOURCE_YAML}")
    listparser.set_defaults(func=sub_list)
    protocolsparser = sub.add_parser(
        "protocols", help=f"Update protocols for {SOURCE_YAML}"
    )
    protocolsparser.set_defaults(func=sub_protocols)
    readmeparser = sub.add_parser(
        "readme", help=f"Generate {OUTPUT_README} from {SOURCE_YAML}"
    )
    readmeparser.set_defaults(func=sub_readme)
    mirrorlistparser = sub.add_parser(
        "mirrorlist", help=f"Generate {OUTPUT_MIRRORLIST} from {SOURCE_YAML}"
    )
    mirrorlistparser.set_defaults(func=sub_mirrorlist)
    coordinatesparser = sub.add_parser(
        "coordinates", help=f"Update coordinates for {SOURCE_YAML}"
    )
    coordinatesparser.set_defaults(func=sub_coordinates)
    geojsonparser = sub.add_parser(
        "geojson", help=f"Generate {OUTPUT_GEOJSON} from {SOURCE_YAML}"
    )
    geojsonparser.set_defaults(func=sub_geojson)
    allparser = sub.add_parser("all", help="Execute all operations")
    allparser.set_defaults(func=sub_all)
    args = parser.parse_args()
    if "func" not in args:
        parser.print_help()
    args.func(args)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3

import sys
import argparse
import pprint
from urllib.parse import urlparse
import socket
from ipaddress import ip_address, IPv4Address, IPv6Address
from http.client import HTTPConnection, HTTPSConnection

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


def mirror_title(item):
    title = "{provider}".format(**item)
    if "location" in item:
        title += " ({location})".format(**item)
    if "protocols" in item:
        title += " ({})".format(", ".join(item["protocols"]))
    return title


def mirror_comments(item):
    comments = ""
    if "added_date" in item:
        comments += "## Added: {}\n".format(item["added_date"])
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


def sub_readme(args):
    with open(SOURCE_YAML, 'r') as source:
        try:
            mirrors = yaml.load(source)
            gen_readme(mirrors)

        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)


def sub_mirrorlist(args):
    with open(SOURCE_YAML, 'r') as source:
        try:
            mirrors = yaml.load(source)
            gen_mirrorlist(mirrors)

        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)


def sub_list(args):
    with open(SOURCE_YAML, 'r') as source:
        try:
            mirrors = yaml.load(source)
            pprint.pprint(mirrors)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)


def try_connect(domain, url, connection):
    try:
        http = HTTPConnection(domain, timeout=1)
        http.request("GET", url)
        res = http.getresponse()
        if res.status == 200:
            return True
    except:
        return False


def get_protocols(mirror):
    url = urlparse(mirror['url'])
    domain = url.hostname
    protocols = set()
    print('Accessing "{provider}" at "{domain}": ... '.format(
        domain=domain, **mirror), end='', flush=True)

    for (family, _, _, _, sockaddr) in socket.getaddrinfo(domain, 80):
        ip = sockaddr[0]
        ipa = ip_address(ip)
        if ipa.is_global:
            if type(ipa) is IPv4Address:
                protocols.add("ipv4")
            if type(ipa) is IPv6Address:
                protocols.add("ipv6")

    if try_connect(domain, mirror['url'], HTTPConnection):
        protocols.add("http")
    if try_connect(domain, mirror['url'], HTTPSConnection):
        protocols.add("https")
    print(", ".join(protocols))
    return list(protocols)


def sub_protocols(args):
    mirrors = []
    with open(SOURCE_YAML, 'r') as source:
        try:
            mirrors = yaml.load(source)
        except yaml.YAMLError as e:
            print(e)
            sys.exit(1)
    for m in mirrors:
        m["protocols"] = get_protocols(m)
    with open(SOURCE_YAML, "w") as output:
        print(yaml.dump(mirrors, encoding=None, allow_unicode=True,
                        default_flow_style=False), file=output)


def sub_all(args):
    sub_protocols(args)
    sub_readme(args)
    sub_mirrorlist(args)


def main():
    parser = argparse.ArgumentParser(
        description='update mirrors status and generate mirrorlist or README.md')
    sub = parser.add_subparsers(help='actions as subcommands')
    listparser = sub.add_parser(
        'list', help='list mirrors in {}'.format(SOURCE_YAML))
    listparser.set_defaults(func=sub_list)
    protparser = sub.add_parser(
        'protocols', help='try access to URLs of the mirrors and update the protocols'.format(SOURCE_YAML))
    protparser.set_defaults(func=sub_protocols)
    readmeparser = sub.add_parser(
        'readme', help='write {} with the information from {}'.format(OUTPUT_README, SOURCE_YAML))
    readmeparser.set_defaults(func=sub_readme)
    mirrorlistparser = sub.add_parser(
        'mirrorlist', help='write {} with the information from {}'.format(OUTPUT_MIRRORLIST, SOURCE_YAML))
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

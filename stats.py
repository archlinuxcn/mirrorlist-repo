#!/usr/bin/python3

import asyncio
import sys
from email.utils import parsedate_to_datetime

import httpx  # in python-httpx and python-h2 packages
import orjson  # in python-orjson package
import ruamel.yaml  # in python-ruamel-yaml package

SOURCE_YAML = "mirrors.yaml"
OUTPUT_JSON = "stats.json"


FILES = (
    "lastupdate",
    "x86_64/archlinuxcn.db",
    "any/archlinuxcn.db",
)


async def fetch(client, mirror, file):
    provider = mirror["provider"]
    url = mirror["url"]
    try:
        response = await client.head(url + file)
        if response.status_code == httpx.codes.OK:
            timestamp = parsedate_to_datetime(response.headers.get("Last-Modified"))
            return provider, file, timestamp, None
        response.raise_for_status()
    except (httpx.HTTPError, httpx.InvalidURL) as error:
        return provider, file, None, error


async def gather(mirrors):
    mirrors.append(
        {
            "provider": "tier0",
            "url": "https://repo.archlinuxcn.org/",
        }
    )
    client = httpx.AsyncClient(
        headers={"User-Agent": "curl/8.5.0"},
        http2=True,
        timeout=10,
        follow_redirects=True,
    )
    tasks = []
    for m in mirrors:
        for file in FILES:
            tasks.append(fetch(client, m, file))
    return await asyncio.gather(*tasks)


def process(data, mirrors):
    success = {}
    failed = {}
    for provider, file, timestamp, error in data:
        if timestamp is not None:
            success[(provider, file)] = timestamp
        elif error is not None:
            failed[(provider, file)] = error
    stats = []
    for m in mirrors:
        provider = m["provider"]
        if provider == "tier0":
            continue
        tag = {}
        information = {}
        for file in FILES:
            if (provider, file) in success:
                information[file] = str(
                    success[("tier0", file)] - success[(provider, file)]
                )
                tag = "success"
            elif (provider, file) in failed:
                information[file] = str(failed[(provider, file)])
                tag = "failed"
        stats.append(
            {
                key: key_comment
                for key, key_comment in {
                    "provider": provider,
                    "comment": m["comment"] if "comment" in m else "",
                    "url": m["url"],
                    "region": m["region"],
                    "protocols": m["protocols"],
                    "tag": tag,
                    "information": information,
                }.items()
                if key != "comment" or key_comment
            }
        )
    return stats


async def main():
    with open(SOURCE_YAML, encoding="utf-8") as source:
        try:
            mirrors = ruamel.yaml.YAML(typ="safe").load(source)["archlinuxcn"]
        except ruamel.yaml.YAMLError as error:
            sys.exit(repr(error))
        data = await gather(mirrors)
        stats = process(data, mirrors)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as output:
        print(
            orjson.dumps(
                {"archlinuxcn": stats},
                option=orjson.OPT_INDENT_2,
            ).decode("utf8"),
            file=output,
        )


if __name__ == "__main__":
    asyncio.run(main())

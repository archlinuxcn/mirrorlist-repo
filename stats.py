#!/usr/bin/python3

import asyncio
from urllib.parse import urljoin

import yaml
import aiohttp

def humantime(t: int) -> str:
  '''seconds -> XhYmZs'''
  m, s = divmod(t, 60)
  h, m = divmod(m, 60)
  d, h = divmod(h, 24)
  ret = ''
  if d:
    ret += '%dd' % d
  if h:
    ret += '%dh' % h
  if m:
    ret += '%dm' % m
  if s:
    ret += '%ds' % s
  if not ret:
    ret = '0s'
  return ret

async def get_lastupdate(session, name, url):
  try:
    res = await session.get(url)
    content = await res.text()
    dt = int(content)
    print(f'{name} done.')
    return name, dt
  except Exception as e:
    return name, e

async def main():
  with open('mirrors.yaml') as f:
    data = yaml.load(f, Loader=yaml.FullLoader)

  async with aiohttp.ClientSession(
    timeout = aiohttp.ClientTimeout(total=10),
  ) as session:
    futures = []
    for mirror in data:
      url = urljoin(mirror['url'], 'lastupdate')
      fu = get_lastupdate(session, mirror['provider'], url)
      futures.append(fu)
    fu = get_lastupdate(session, 'tier0', 'https://repo.archlinuxcn.org/lastupdate')
    futures.append(fu)
    results = await asyncio.gather(*futures)

  done = {}
  error = {}
  for name, dt in results:
    if isinstance(dt, int):
      done[name] = dt
    else:
      error[name] = dt

  print('\nLags:')
  tier0 = done.pop('tier0')
  for name, dt in sorted(done.items(), reverse=True, key=lambda x: x[1]):
    print(f'{name} {humantime(tier0-dt)}')

  print('\nErrors:')
  for name, e in error.items():
    print(f'{name} {e!r}')

if __name__ == '__main__':
  asyncio.run(main())

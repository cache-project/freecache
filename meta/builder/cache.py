import os
import pathlib

cache_dir = os.path.join(os.getcwd(), 'cache')
pathlib.Path(cache_dir).mkdir(exist_ok=True)


def in_cache(key):
  return os.path.isfile(os.path.join(cache_dir, key))


def open_cache(key, mode = 'r'):
  return open(os.path.join(cache_dir, key), mode)

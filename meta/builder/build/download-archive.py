import os
import tempfile
import tarfile
import hashlib
import pathlib
import requests
from tqdm import tqdm

from meta.builder.cache import in_cache, open_cache


def download(url, hash, output):
  print('downloading {}'.format(url))
  response = requests.get(url, stream = True)
  m = hashlib.sha3_256()
  with tqdm(unit = 'B', unit_scale = True) as pbar:
    for data in response.iter_content(chunk_size=10000):
      output.write(data)
      m.update(data)
      pbar.update(len(data))
      digest = m.digest()
  if hash and digest.hex() != hash:
    raise Exception('{}: hash mismatch (got {}, expected {})'.format(url, digest.hex(), hash))
  elif not hash:
    print('hash: {}'.format(digest.hex()))

def extract(format, archive, output_file):
  if format == 'tar':
    print('extracting tar archive to {}'.format(output_file))
    tar_file = tarfile.open(archive.name)
    tar_file.extractall(os.path.dirname(output_file))
  else:
    raise Exception('invalid archive format {}'.format(format))

def build(file_meta, output_file, args):
  pathlib.Path(output_file).mkdir(parents=True, exist_ok=True)
  url = file_meta['url']
  if args.force_hash and 'hash' not in file_meta:
    raise Exception('missing hash and force-hash enabled')
  hash = 'hash' in file_meta and file_meta['hash']
  if 'format' in file_meta:
    format = file_meta['format']
  else:
    format = 'tar'

  if hash and in_cache(hash):
    with open_cache(hash, 'rb') as file:
      print('found in cache')
      extract(format, file, output_file)
  elif hash:
    with open_cache(hash, 'a+b') as file:
      download(url, hash, file)
      extract(format, file, output_file)
  else:
    with tempfile.NamedTemporaryFile() as file:
      download(url, False, file)
      extract(format, file, output_file)
    
  return os.path.basename(output_file)

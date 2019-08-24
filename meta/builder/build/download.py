import os
import tempfile
import hashlib
import shutil
import requests
from tqdm import tqdm

from meta.builder.cache import in_cache, open_cache


def download(url, hash, output):
  print('downloading {}'.format(url))
  response = requests.get(url, stream = True)
  m = hashlib.sha3_256()
  with tqdm(unit = 'B', unit_scale = True) as pbar:
    for data in response.iter_content(chunk_size=10000):
      for output_file in output:
        output_file.write(data)
      m.update(data)
      pbar.update(len(data))
      digest = m.digest()
  if hash and digest.hex() != hash:
    raise Exception('{}: hash mismatch (got {}, expected {})'.format(url, digest.hex(), hash))
  elif not hash:
    print('hash: {}'.format(digest.hex()))

def build(file_meta, output_file, args):
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
      filename = file.name
    shutil.copy2(filename, output_file)
  elif hash:
    with open_cache(hash, 'wb') as file:
      with open(output_file, 'wb') as output:
        download(url, hash, [file, output])
  else:
    with tempfile.NamedTemporaryFile() as file:
      with open(output_file, 'wb') as output:
        download(url, False, [file, output])
    
  return os.path.basename(output_file)

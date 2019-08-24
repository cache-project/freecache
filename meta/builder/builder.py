#!/usr/bin/env python3

import os
import gzip
import argparse
import pathlib
import yaml
import shutil
from git import Repo

import meta.builder.licenses
import meta.builder.modules

ignore = [
  '.DS_Store',
  '.git',
  'out',
  'cache'
]


def build(directory, out_directory, args):
  print('[hierdir] {}'.format(directory))
  pathlib.Path(out_directory).mkdir(parents=True, exist_ok=True)
  licenses = meta.builder.licenses.get_licenses()
  meta_file_path = os.path.join(directory, 'meta.yml')
  if not os.path.isfile(meta_file_path):
    raise Exception('hierdir {} is missing meta.yml'.format(directory))
  with open(meta_file_path, 'r') as meta_file:
    meta_dict = yaml.load(meta_file.read(), Loader=yaml.Loader)
  if meta_dict is None:
    meta_dict = {}
  filename_map = {}
  for file in meta_dict:
    file_path = os.path.join(directory, file)
    out_file_path = os.path.join(out_directory, file)
    file_meta = meta_dict[file]
    if file != 'source.tar.gz':
      if 'license' not in file_meta:
        raise Exception('{} missing a license'.format(file_path))
      if file_meta['license'] not in licenses:
        raise Exception('{} has invalid license ({})'.format(file_path, file_meta['license']))
    if 'build' in file_meta:
      builders = meta.builder.modules.get_builders()
      builder_name = file_meta['build']
      builder = builders[builder_name]
      print('[build:{}] {}'.format(builder_name, file_path))
      filename_map[file] = builder.build(file_meta, out_file_path, args)
    elif not os.path.exists(file_path):
      raise Exception('{} doesn\'t exist'.format(file_path))
    else:
      if 'transform' not in file_meta:
        file_meta['transform'] = 'copy'
      transformers = meta.builder.modules.get_transformers()
      transform_name = file_meta['transform']
      transformer = transformers[transform_name]
      print('[transform:{}] {}'.format(transform_name, file_path))
      filename_map[file] = transformer.transform(meta_dict, file_path, out_file_path, args)
  children = [child for child in os.listdir(directory) if child != 'meta.yml' and child not in meta_dict and child not in ignore]
  if 'index.html' not in os.listdir(out_directory):
    with open(os.path.join(out_directory, 'index.html'), 'w') as index:
      index.write('<link rel="stylesheet" href="/runtime/style.css" /><ul>')
      for child in children:
        index.write('<li><a href="{}"><strong><code>{}/</code></strong></a></li>'.format(child, child))
      for file in meta_dict:
        file_meta = meta_dict[file]
        if 'index' not in file_meta or file_meta['index']:
          if 'title' in file_meta:
            title = '{} <em>(<code>{}</code>)</em>'.format(file_meta['title'], file)
          else:
            title = '<code>{}</code>'.format(file)
          index.write('<li><a href="{}">{}</a></li>'.format(filename_map[file], title))
      index.write('</ul>')
  for child in children:
    if child != 'meta.yml' and child not in meta_dict and child not in ignore:
      child_path = os.path.join(directory, child)
      child_out_path = os.path.join(out_directory, child)
      if os.path.isdir(child_path):
        build(child_path, child_out_path, args)
      else:
        raise Exception('file {} isn\'t listed in meta.yml'.format(child_path))


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Build FreeCache')
  parser.add_argument('input_dir', type=str, help='The input directory', default=os.getcwd())
  parser.add_argument('-o', '--output', type=str, help='The output directory' , default=os.path.join(os.getcwd(), 'out'))
  parser.add_argument('--force-hash', action='store_const', const=True, help='Force download-archive works to have a hash', default=False)
  args = parser.parse_args()
  if os.path.isdir(args.output):
    print('removing existing output directory')
    shutil.rmtree(args.output)
  elif os.path.isfile(args.output):
    print('removing existing output directory')
    os.unlink(args.output)
  print('creating source archive')
  repo = Repo(args.input_dir)
  archive_path = os.path.join(args.input_dir, 'source.tar.gz')
  with gzip.open(archive_path, 'wb') as archive_file:
    repo.archive(archive_file)
  print('building')
  build(args.input_dir, args.output, args)
  os.unlink(archive_path)
  print('done')

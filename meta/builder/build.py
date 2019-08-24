#!/usr/bin/env python3

import os
import argparse
import pathlib
import yaml
import shutil

import meta.builder.licenses
import meta.builder.modules

ignore = [
  '.DS_Store',
  '.git',
  'out'
]


def build(directory, out_directory):
  print('[hierdir] {}'.format(directory))
  pathlib.Path(out_directory).mkdir(parents=True, exist_ok=True)
  licenses = meta.builder.licenses.get_licenses()
  meta_file_path = os.path.join(directory, 'meta.yml')
  if not os.path.isfile(meta_file_path):
    raise Exception('hierdir {} is missing meta.yml'.format(directory))
  with open(meta_file_path, 'r') as meta_file:
    meta_dict = yaml.load(meta_file.read(), Loader=yaml.Loader)
  filename_map = {}
  for file in meta_dict:
    file_path = os.path.join(directory, file)
    out_file_path = os.path.join(out_directory, file)
    if not os.path.exists(file_path):
      raise Exception('{} doesn\'t exist'.format(file_path))
    file_meta = meta_dict[file]
    if 'license' not in file_meta:
      raise Exception('{} missing a license'.format(file_path))
    if file_meta['license'] not in licenses:
      raise Exception('{} has invalid license ({})'.format(file_path, file_meta['license']))
    if 'transform' not in file_meta:
      file_meta['transform'] = 'copy'
    transformers = meta.builder.modules.get_transformers()
    transform_name = file_meta['transform']
    transformer = transformers[transform_name]
    if transformer is None:
      raise Exception('{} has invalid transform ({})'.format(file_path, transform_name))
    print('[transform:{}] {}'.format(transform_name, file_path))
    filename_map[file] = transformer.transform(meta_dict, file_path, out_file_path)
  children = [child for child in os.listdir(directory) if child != 'meta.yml' and child not in meta_dict and child not in ignore]
  if 'index.html' not in os.listdir(out_directory):
    with open(os.path.join(out_directory, 'index.html'), 'w') as index:
      index.write('<ul>')
      for child in children:
        index.write('<li><a href="{}"><strong><code>{}</code></strong></a></li>'.format(child, child))
      for file in meta_dict:
        index.write('<li><a href="{}"><code>{}</code></a></li>'.format(filename_map[file], file))
      index.write('</ul>')
  for child in children:
    if child != 'meta.yml' and child not in meta_dict and child not in ignore:
      child_path = os.path.join(directory, child)
      child_out_path = os.path.join(out_directory, child)
      if os.path.isdir(child_path):
        build(child_path, child_out_path)
      else:
        raise Exception('file {} isn\'t listed in meta.yml'.format(child_path))


if __name__ == "__main__":
  parser = argparse.ArgumentParser(description='Build FreeCache')
  parser.add_argument('input_dir', type=str, help='The input directory', default=os.getcwd())
  parser.add_argument('-o', '--output', type=str, help='The output directory' , default=os.path.join(os.getcwd(), 'out'))
  args = parser.parse_args()
  if os.path.isdir(args.output):
    shutil.rmtree(args.output)
  elif os.path.isfile(args.output):
    os.unlink(args.output)
  build(args.input_dir, args.output)

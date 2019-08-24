#!/usr/bin/env python3

import os
import yaml

ignore = [
  '.DS_Store',
  '.git'
]


def get_licenses(root_dir):
  licenses_directory = os.path.join(root_dir, 'licenses')
  license_files = os.listdir(licenses_directory)
  return [filename.replace('.txt', '') for filename in license_files]


def validate(licenses, directory):
  meta_file_path = os.path.join(directory, 'meta.yml')
  with open(meta_file_path, 'r') as meta_file:
    meta = yaml.load(meta_file.read(), Loader=yaml.Loader)
  for file in meta:
    file_path = os.path.join(directory, file)
    if not os.path.exists(file_path):
      raise Exception('{} doesn\'t exist'.format(file_path))
    file_meta = meta[file]
    if 'license' not in file_meta:
      raise Exception('{} missing a license'.format(file_path))
    if file_meta['license'] not in licenses:
      raise Exception('{} has invalid license ({})'.format(file_path, file_meta['license']))
  children = os.listdir(directory)
  for child in children:
    if child != 'meta.yml' and child not in meta and child not in ignore:
      validate(licenses, os.path.join(directory, child))

if __name__ == "__main__":
  start_in = os.getcwd()
  print('Validating FreeCache starting in {}...'.format(start_in))
  validate(get_licenses(start_in), start_in)
  print('Valid!')

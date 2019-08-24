import os

def transform(meta_dict, input_file, output_file):
  os.symlink(input_file, output_file)

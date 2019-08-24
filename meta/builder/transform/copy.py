import os
import shutil

def transform(meta_dict, input_file, output_file):
  if os.path.isfile(input_file):
    shutil.copy2(input_file, output_file)
  else:
    shutil.copytree(input_file, output_file)
  return os.path.basename(output_file)

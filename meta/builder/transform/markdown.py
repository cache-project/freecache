import os
import mistletoe

header = '<link rel="stylesheet" href="/runtime/style.css" />'


def transform(meta_dict, input_file, output_file, args):
  output_file_html = output_file.replace('.md', '.html')

  with open(output_file_html, 'w') as o_f:
    with open(input_file, 'r') as i_f:
      o_f.write(header + mistletoe.markdown(i_f.read()))

  return os.path.basename(output_file_html)

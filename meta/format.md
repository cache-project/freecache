# Format of FreeCache

FreeCache is organized in a hierarchical directory structure. The directory
hierarchy is currently being designed.

There is a difference between a physical directory and a hierarchical
directory. A physical directory is a directory on your file system. A
hierarchical directory is a directory that (1) hasn't been referenced by a
`meta.yml` and (2) contains a `meta.yml`.

Every hierarchical directory has a YAML file named `meta.yml`. This file
contains metadata for every entry in that directory. It has a section for each
file, with each containing that file's metadata.

## Metadata keys

`publisher`: The organization or person who published the work

`license`: The SPDX identifier for the license under which the work is released
(see licenses/&larr;license name&rarr; for full license text)

`copyright`: The copyright statement without the &copy; (e.g. 2019 Cache
Project)

`language`: A BCP 47 language code for the primary language of the work

`transform`: The transform module used to transform the input file into an
output file

`builder`: The builder module used to generate the output file

import importlib
import inspect
import os


def _get_module_path():
  module_filename = inspect.getframeinfo(inspect.currentframe()).filename
  return os.path.dirname(os.path.abspath(module_filename))


def get_transform_path():
  return os.path.join(_get_module_path(), 'transform')


def get_builder_path():
  return os.path.join(_get_module_path(), 'builders')


_transformers = None

def get_transformers():
  global _transformers
  if _transformers == None:
    transform_path = get_transform_path()
    files = [filename.replace('.py', '') for filename in os.listdir(transform_path)]
    _transformers = { module: importlib.import_module('meta.builder.transform.{}'.format(module)) for module in files }
  
  return _transformers


_builders = None

def get_builders():
  global _builders
  if _builders == None:
    transform_path = get_builder_path()
    files = [filename.replace('.py', '') for filename in os.listdir(transform_path)]
    _builders = { module: importlib.import_module('meta.builder.build.{}'.format(module)) for module in files }
  
  return _builders

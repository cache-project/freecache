import os


_licenses = None

def get_licenses():
  global _licenses
  if _licenses == None:
    licenses_directory = os.path.join(os.getcwd(), 'licenses')
    license_files = os.listdir(licenses_directory)
    _licenses = [filename.replace('.txt', '') for filename in license_files]
  
  return _licenses

from setuptools import setup
import os

_here = os.path.abspath(os.path.dirname(__file__))

version = {}
with open(os.path.join(_here, 'webresourcecrawler', 'version.py')) as f:
    exec(f.read(), version)

setup(name='webresourcecrawler',
      version=version['__version__'],
      description=(
          'Recursively crawl URL to gather resources such as twitter handle and facebook ids.'),
      author='Bryan Seungmin Lee',
      author_email='smblee14@gmail.com',
      license='MPL-2.0',
      packages=['webresourcecrawler'],
      include_package_data=True,
      )

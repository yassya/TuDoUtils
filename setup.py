try:
  from setuptools import setup
except ImportError:
  from distutils.core import setup

config = {
  'description': "A small package for doing common things with ROOT",
  'author': "Christian Jung",
  'url': "https://github.com/yassya/TuDoUtils",
  'download_url': 'https://github.com/yassya/TuDoUtils',
  'author_email': 'christian.jung@udo.edu',
  'version': '0.1',
  'install_requires': [], # TODO figure out how to require ROOT here
  'packages': ['TuDoUtils'],
  'scripts': [],
  'name': 'TuDoUtils'
}

setup(**config)

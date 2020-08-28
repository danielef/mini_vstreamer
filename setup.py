from setuptools import find_packages, setup
from pip._internal.req import parse_requirements

def load_requirements(fname):
    req = []
    with open(fname, 'r') as f:
        req = f.read().splitlines()
    return req

setup(name = 'mini_vstreamer',
      version = '0.1',
      package_dir = {'': 'src'},
      packages = find_packages(where='src'),
      install_requires = load_requirements('requirements.txt'))

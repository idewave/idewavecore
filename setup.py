import pathlib

from setuptools import setup, find_packages


# The directory containing this file
HERE = pathlib.Path(__file__).parent


# The text of the README file
README = (HERE / "README.md").read_text()


with open('requirements.txt') as f:
    dependencies = f.read().splitlines()


setup(name='idewavecore',
      version='0.0.1',
      description='Framework for creating custom servers',
      long_description=README,
      long_description_content_type="text/markdown",
      url='https://github.com/idewave/idewavecore',
      author='Sergio Ivanuzzo',
      author_email='sergio.ivanuzzo@gmail.com',
      license='Apache license 2.0',
      packages=find_packages(exclude=("test",)),
      install_requires=dependencies,
      zip_safe=False)

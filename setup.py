from codecs import open as codecs_open
from setuptools import setup, find_packages

# Get the long description from the relevant file
with codecs_open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

with open('joydivision/__init__.py') as f:
  for line in f:
      if line.find("__version__") >= 0:
          version = line.split("=")[1].strip()
          version = version.strip('"')
          version = version.strip("'")
          break


setup(name='rio-joydivision',
      version=version,
      description=u"Lines will tear us apart",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Damon Burgett",
      author_email='damon@mapbox.com',
      url='https://github.com/dnomadb/rio-joydivision',
      license='BSD',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'click',
          'rasterio',
          'shapely'
      ],
      extras_require={
          'test': ['pytest'],
      },
      entry_points="""
      [rasterio.rio_commands]
      joydivision=joydivision.scripts.cli:joydivision
      """      )

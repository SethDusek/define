from version import __version__ as version
try:
            from setuptools import setup
except ImportError:
            from distutils.core import setup

setup(name='define',
      description='Terminal Dictionary',
      long_description=open('README.md').read(),
      version=version,
      author='SethDusek',
      author_email='shibe@openmailbox.org',
      url='https://github.com/SethDusek/define',
      data_files=[
          ("share/man/man1", ["define.1"]),
          ("share/doc/define", ["LICENSE"])
          ],
      packages=['define'],
      entry_points={'console_scripts': ['define=define.define:main']},
      install_requires=['requests'],
      classifiers=['Intended Audience :: End Users/Desktop',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3'],
      license='BSD')

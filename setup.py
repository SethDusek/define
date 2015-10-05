try:
            from setuptools import setup
except ImportError:
            from distutils.core import setup

setup(name='define',
      description='Terminal Dictionary',
      long_description=open('README.rst').read(),
      version='1.66',
      author='SethDusek',
      author_email='shibe@openmailbox.org',
      url='https://github.com/SethDusek/define',
      data_files=[
      ("share/man/man1", ["define.1"]),
      ("share/doc/define", ["LICENSE"])
      ],
      scripts=['define'],
      install_requires=['requests'],
      classifiers=['Intended Audience :: End Users/Desktop',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3'],
      license='BSD')

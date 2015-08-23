from distutils.core import setup

setup(name='define',
      description='Terminal Dictionary',
      long_description=open('README.rst').read(),
      version='0.2',
      author='Johnathan "shaggytwodope" Jenkins',
      author_email='twodopeshaggy@gmail.com',
      url='https://github.com/SethDusek/define',
      data_files=[
      ("share/man/man1", ["define.1"]),
      ("share/doc/define", ["LICENSE"])
      ],
      scripts=['define'],
      requires=['wordnik', 'requests', 'wget'],
      classifiers=['Intended Audience :: End Users/Desktop',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3'],
      license='BSD')

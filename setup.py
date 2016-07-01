from distutils.core import setup

version_file = open('VERSION', 'r')
version = version_file.readline()

setup(
    name='grepspider',
    version=version,
    packages=['grepspider'],
    url='https://github.com/westial/grepspider',
    license='GPL v3',
    author='Jaume Mila',
    author_email='jaume@westial.com',
    description='Recursive web crawler with regular expression content filter.'
)

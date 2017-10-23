"""setup file to install the direct_downloader module."""
from setuptools import setup

setup(name='direct-downloader',
      version='1.2.1',
      description='Get direct links for files located at different file hoster.',
      author='Markus Freitag',
      author_email='fmarkus@mailbox.org',
      license='MIT',
      packages=['direct_downloader'],
      scripts=['bin/direct-downloader'],
      install_requires=['requests'],
      zip_safe=False)

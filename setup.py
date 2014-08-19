from os import path as os_path
from setuptools import setup, find_packages

import front_edit

description = long_description = "Front end editing for Django."
if os_path.exists('README.rst'):
    long_description = open('README.rst').read()

version = front_edit.VERSION

def read(fname):
    return open(os_path.join(os_path.dirname(__file__), fname)).read()

setup(name='django-front-edit',
    version=version,
    description=description,
    long_description=long_description,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Internet :: WWW/HTTP :: Site Management",
        "Topic :: Software Development :: User Interfaces",
        "Topic :: Utilities",
        "Framework :: Django",
    ],
    keywords='django mail queue smtp backend',
    maintainer='Dwaiter.com',
    maintainer_email='dev@dwaiter.com',
    url='https://bitbucket.org/dwaiter/django-front-edit',
    license='BSD',
    packages=find_packages(),
    include_package_data=True,
    install_requires=['django>=1.4', 'beautifulsoup4>=4.3.2', 'django-classy-tags>=0.5.1']
)
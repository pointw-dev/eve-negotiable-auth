#!/usr/bin/env python

from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='eve-negotiable-auth',
    version='0.9.4',
    description='Eve Negotiable authentication',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Michael Ottoson',
    author_email='michael@pointw.com',
    url='https://github.com/pointw-dev/eve-negotiable-auth',
    keywords=['eve', 'api', 'rest', 'auth', 'http'],
    packages=find_packages(),
    license='MIT',
    install_requires=['eve>=0.8.0', 'authparser>=1.0'],
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Environment :: No Input/Output (Daemon)',
        'Intended Audience :: Developers',
        'Intended Audience :: Telecommunications Industry',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: HTTP Servers',
        'Topic :: Security',
    ]
)

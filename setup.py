import os
import sys

if (sys.version_info < (3, 6)):
    print("Python 3.6 or higher is required, please see https://www.python.org/ or your OS package repository", file=sys.stderr)
    sys.exit(2)

from setuptools import setup, find_packages

long_desc=open('README.md').read()

if os.path.exists('README.rst'):
    long_desc = open('README.rst').read()

setup(
    name='SNMPv3 Hash Generator',
    version='0.1',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'snmpv3-hashgen=scripts.snmpv3_hashgen:main',
        ],
    },

    license='Apache Software License',
    long_description=long_desc,

    author="Adam Bishop",
    author_email="adam@omega.org.uk",
    description="Generates SNMPv3 hashes as described in rfc3414 suitable for use with ESXi and other SNMP daemons",
    url="https://github.com/TheMysteriousX/SNMPv3-Hash-Generator",

    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
)


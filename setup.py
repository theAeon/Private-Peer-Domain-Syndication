'''sets up the python package'''

from setuptools import setup, find_packages

setup(
    name='ppds',
    version='0.0.1.dev',

    description='Private Peer Domain Syndication',
    long_description='A python implementation of PPDS hostfile patching',

    url='https://github.com/theAeon/Private-Peer-Domain-Syndication',

    author="Andrew Donshik",
    author_email='andrewdonshik@gmail.com',

    license="GPL-3.0",

    classifiers=[
        'Development Status :: 1 - Development'
        'Intended Audience :: Privacy-Minded Individuals'
        'Topic :: Networking'
        'License :: OSI Approved :: GPL 3.0'
        'Programming Language :: Python :: 3'
    ],

    keywords='networking',

    packages=['ppds'],

    install_requires=['requests'],

    entry_points={
        'console_scripts': [
            'ppds=ppds.__main__:exec_cli'
        ]
    }
)

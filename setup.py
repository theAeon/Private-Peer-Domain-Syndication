'''sets up the python package'''

from setuptools import setup, find_packages

setup(
    name='ppds',
    version='0.0.1.dev1',

    description='Private Peer Domain Syndication',
    long_description='''
    PPDS:
    Andrew Donshik, 2017

The Private-Peer-Domain-Syndication Manifesto:

PPDS is an open-source and semi-centralized replacement to traditional domain registration and distribution methods. PPDS is meant to be a drop-in challenger to traditional domain serving and registration. It seeks to completely remove the commercial and governmental reliance of domain spaces, and make domain resolution and registration a user controlled and user regulated process. Domain name servers are replaced by RSS-esque domain aggregators that can be created and maintained by anyone. It is their responsibility to map domain names to their respective IP address, but they can choose to map any domain to any address they wish. Users of PPDS can also subscribe to other peoples' domain aggregators, and these aggregations are downloaded in full or in part to their computer. These domain aggregators come in the form of JSON mappings between the ip address and the new domain. Requests for these domains are resolved locally whenever possible, minimizing the amount of outgoing information related to their browsing activity. Users can enable multiple aggregators at once if they want, and users decide how domains are deduplicated between multiple aggregators. The goal of the project is to make domain names an openly managed and accessible resource.

Repo formatting and protocol to follow.

The current idea of implementation is to create a hosts-file patch manager that downloads from a central repository (user-repos will be possible of course) that is verified through some kind of cert service.


TODO:

Implement download requests from the repositories.

*Real* Conflict Management

Some kind of public key private key verification for repositories.

GUI

A spec so that people can code implementations that aren't written by me

Building/Running:

I've only tested this against Python 3.6, but there's no reason it wouldn't work on earlier versions.

DOES NOT WORK ON PYTHON 2

CURRENTLY DOES NOT WORK ON WINDOWS

run setup.py install or setup.py build bdist_wheel and install with pip
''',

    url='https://github.com/theAeon/Private-Peer-Domain-Syndication',
    download_url='https://github.com/theAeon/Private-Peer-Domain-Syndication/tarball/0.0.1.dev1',

    author="Andrew Donshik",
    author_email='andrewdonshik@gmail.com',

    license="GPL-3.0",

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3 :: Only',
        'Operating System :: POSIX',
        'Topic :: Internet :: Name Service (DNS)',
    ],

    keywords='networking',

    packages=find_packages(),

    install_requires=['requests'],

    # extras_require={'dev': ['pyinstaller']},

    entry_points={
        'console_scripts': [
            'ppds=ppds.__main__:exec_cli'
        ]
    }
)

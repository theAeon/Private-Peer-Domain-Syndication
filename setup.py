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
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Environment :: MacOS X',
        'Operating System :: POSIX',
        'Topic :: Internet :: Name Service (DNS)',
    ],

    keywords='networking',

    packages=['ppds'],

    install_requires=['requests'],

    # extras_require={'dev': ['pyinstaller']},

    entry_points={
        'console_scripts': [
            'ppds=ppds.__main__:exec_cli'
        ]
    }
)

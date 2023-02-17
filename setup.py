"""HTTP tools setup."""
from setuptools import (
    find_packages,
    setup)

from pathlib import Path


def read(rel_path):
    init = Path(__file__).resolve().parent / rel_path
    return init.read_text('utf-8', 'ignore')


description = ('httptools helps you to capture, repeat'
               ' and live intercept HTTP requests. It '
               'is built on top of '
               '[mitmproxy](https://mitmproxy.org/)')
setup(
    name='http-tools',
    version='2.1.1',
    description=description,
    author='Ajin Abraham',
    author_email='ajin25@gmail.com',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        ('License :: OSI Approved :: GNU Lesser '
         'General Public License v3 or later (LGPLv3+)'),
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(include=[
        'http_tools', 'http_tools.*',
        'http_tools.modules', 'http_tools.web',
    ]),
    entry_points={
        'console_scripts': [
            'httptools = http_tools.__main__:main',
        ],
    },
    include_package_data=True,
    url='https://github.com/MobSF/httptools',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    install_requires=[
        'mitmproxy==6.0.2',
        'markupsafe==2.0.1',
    ],
)

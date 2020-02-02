from setuptools import (
    find_packages,
    setup)

description = ('httptools helps you to capture, repeat'
               ' and live intercept HTTP requests. It '
               'is built on top of '
               '[mitmproxy](https://mitmproxy.org/)')
setup(
    name='http-tools',
    version='1.1.0',
    description=description,
    author='Ajin Abraham',
    author_email='ajin25@gmail.com',
    license='GPL v3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
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
    long_description=description,
    install_requires=[
        'mitmproxy==5.0.1',
    ],
)

# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


__version__ = '0.0.1'


if __name__ == '__main__':
    setup(
        name='noseapp_requests',
        url='https://github.com/brannt/noseapp_requests',
        version=__version__,
        packages=find_packages(),
        author='Artem Gorokhov',
        author_email='a.gorohov@corp.mail.ru',
        description='requests extension for noseapp lib',
        include_package_data=True,
        zip_safe=False,
        platforms='any',
        install_requires=[
            'noseapp',
            'requests==2.6.0',
        ],
    )

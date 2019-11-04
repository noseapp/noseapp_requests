# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages


__version__ = '0.0.2'


if __name__ == '__main__':
    setup(
        name='noseapp_requests',
        url='https://github.com/brannt/noseapp_requests',
        version=__version__,
        packages=find_packages(exclude=['docs', 'test*']),
        author='Artem Gorokhov',
        author_email='a.gorohov@corp.mail.ru',
        description='requests extension for noseapp lib',
        classifiers=[
            'Development Status :: 3 - Alpha',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Testing',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.6',
            'Programming Language :: Python :: 2.7',
        ],
        keywords='noseapp requests testing',
        include_package_data=True,
        zip_safe=False,
        platforms='any',
        install_requires=[
            'noseapp>=1.0.9',
            'requests==2.20.0',
        ],
        extras_require={
            'doc': ['Sphinx']
        }
    )

from setuptools import setup, find_packages
import os

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

with open('requirements.txt', 'r', encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='django-tictactoe',
    version='1.0.0',
    author='Nestor Wheelock',
    author_email='nestorwheelock@gmail.com',
    description='A reusable Django app module for tic-tac-toe games with REST API and optional frontend templates',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/nestorwheelock/django-tictactoe',
    packages=find_packages(exclude=['tests', 'tests.*', 'planning', 'planning.*']),
    include_package_data=True,
    install_requires=requirements,
    python_requires='>=3.8',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Framework :: Django :: 4.2',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Topic :: Games/Entertainment :: Board Games',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='django tic-tac-toe game rest-api',
    project_urls={
        'Bug Reports': 'https://github.com/nestorwheelock/django-tictactoe/issues',
        'Source': 'https://github.com/nestorwheelock/django-tictactoe',
    },
)

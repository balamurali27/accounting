# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in accounting/__init__.py
from accounting import __version__ as version

setup(
	name='accounting',
	version=version,
	description='Basic Double Entry Accounting System with an Immutable Ledger',
	author='Balamurali M',
	author_email='balamurali@erpnext.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)

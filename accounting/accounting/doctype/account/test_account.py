# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and Contributors
# See license.txt
from __future__ import unicode_literals

import os
import unittest

import frappe

from .account import Account


def create_test_accounts():
	app_path = os.path.dirname(frappe.get_app_path('accounting'))
	json_file = os.path.join(os.getcwd(), app_path, "standard_coa.json")
	Account.load_tree_from_json(json_file)


class TestAccount(unittest.TestCase):
	pass

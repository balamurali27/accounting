# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest


from ..account.test_account import create_test_accounts


def create_test_supplier(supplier_name: str = frappe.mock("name")):
	create_test_accounts()
	return frappe.get_doc({
		"doctype": "Supplier",
		"supplier_name": supplier_name,
	}).insert(ignore_if_duplicate=True)


class TestSupplier(unittest.TestCase):
	pass

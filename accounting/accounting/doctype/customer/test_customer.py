# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and Contributors
# See license.txt
from __future__ import unicode_literals

import unittest

import frappe

from ..account.test_account import create_test_accounts


def create_test_customer(customer_name: str = frappe.mock("name")):
	create_test_accounts()
	return frappe.get_doc({
		"doctype": "Customer",
		"customer_name": customer_name,
	}).insert(ignore_if_duplicate=True)


class TestCustomer(unittest.TestCase):
	pass

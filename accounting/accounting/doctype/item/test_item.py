# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest


def create_test_item(
	item_name: str = frappe.mock("name"),
	price: int = 10,
):
	return frappe.get_doc({
		"doctype": "Item",
		"item_name": item_name,
		"price": price,
		"image": frappe.mock("url")
	}).insert(ignore_if_duplicate=True)


class TestItem(unittest.TestCase):
	pass

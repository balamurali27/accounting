# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and Contributors
# See license.txt
from __future__ import unicode_literals

from typing import Dict, List

import frappe

from accounting.controllers.test_transaction import TestTransaction

from ..customer.test_customer import create_test_customer
from ..item.test_item import create_test_item


def get_test_sales_invoice_item(item=create_test_item(), quantity: int = 1):
	return frappe.get_doc({
		"doctype": "Sales Invoice Item",
		"item": item.name,
		"quantity": quantity,
	})


def get_test_sales_invoice(items: List, customer=create_test_customer()):
	return frappe.get_doc({
		"doctype": "Sales Invoice",
		"customer": customer.name,
		"items": items
	})


class TestSalesInvoice(TestTransaction):

	def test_invoice_submission_creates_balanced_gl_entries(self):
		"""Ensure submitting Sales Invoice creates balanced GL entries."""
		sales_invoice_items = [
			get_test_sales_invoice_item().as_dict(),
			get_test_sales_invoice_item().as_dict()
		]
		sales_invoice = get_test_sales_invoice(sales_invoice_items)
		before = frappe.db.count("GL Entry")
		sales_invoice.submit()
		after = frappe.db.count("GL Entry")
		gl_count_increase = after - before
		self.assertEqual(gl_count_increase, 2, msg=frappe.get_all("GL Entry"))
		self._test_gl_entries_are_balanced()

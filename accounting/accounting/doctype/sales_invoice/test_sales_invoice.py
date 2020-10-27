# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe

from ..customer.test_customer import create_test_customer
from ..item.test_item import create_test_item
from accounting.controllers.test_transaction import TestTransaction


def get_test_sales_invoice(
	item=create_test_item(), customer=create_test_customer()
):
	return frappe.get_doc({
		"doctype": "Sales Invoice",
		"item": item.name,
		"quantity": 1,
		"customer": customer.name
	})


class TestSalesInvoice(TestTransaction):

	def test_invoice_submission_creates_balanced_gl_entries(self):
		"""Ensure submitting Sales Invoice creates balanced GL entries."""
		sales_invoice = get_test_sales_invoice()
		sales_invoice.submit()
		gl_count = frappe.db.count("GL Entry")
		self.assertEqual(gl_count, 2, msg=frappe.get_all("GL Entry"))
		self._test_gl_entries_are_balanced()

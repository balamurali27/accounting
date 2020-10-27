# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe

from accounting.controllers.test_transaction import TestTransaction

from ..item.test_item import create_test_item
from ..supplier.test_supplier import create_test_supplier


def get_test_purchase_invoice(
	item=create_test_item(), supplier=create_test_supplier()
):
	return frappe.get_doc({
		"doctype": "Purchase Invoice",
		"item": item.name,
		"quantity": 1,
		"rate": 10,
		"supplier": supplier.name
	})


class TestPurchaseInvoice(TestTransaction):

	def test_invoice_submission_creates_balanced_gl_entries(self):
		"""Ensure submitting Purchase Invoice creates balanced GL entries."""
		purchase_invoice = get_test_purchase_invoice()
		purchase_invoice.submit()
		gl_count = frappe.db.count("GL Entry")
		self.assertEqual(gl_count, 2, msg=frappe.get_all("GL Entry"))
		self._test_gl_entries_are_balanced()

# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe

from accounting.controllers.test_transaction import TestTransaction

from ..item.test_item import create_test_item
from ..supplier.test_supplier import create_test_supplier


def get_test_purchase_invoice_item(
	item=create_test_item(), rate: float = 10, quantity: int = 1
):
	return frappe.get_doc({
		"doctype": "Purchase Invoice Item",
		"item": item.name,
		"rate": 10,
		"quantity": quantity,
	})


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
		purchase_invoice_items = [
			get_test_purchase_invoice_item().as_dict(),
			get_test_purchase_invoice_item().as_dict()
		]
		purchase_invoice = get_test_purchase_invoice(purchase_invoice_items)
		before = frappe.db.count("GL Entry")
		purchase_invoice.submit()
		after = frappe.db.count("GL Entry")
		gl_count_increase = after - before
		self.assertEqual(gl_count_increase, 2, msg=frappe.get_all("GL Entry"))
		self._test_gl_entries_are_balanced()

# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe

from accounting.controllers.transaction import Transaction


class PurchaseInvoice(Transaction):

	def before_submit(self):
		supplier = frappe.get_doc("Supplier", self.supplier)
		self.debit_account = supplier.account
		self.credit_account = "Sales"

	def on_submit(self):
		self.amount = self.rate * self.quantity
		super().on_submit()

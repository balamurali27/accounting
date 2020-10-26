# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe

from accounting.controllers.transaction import Transaction


class PurchaseInvoice(Transaction):

	def __init__(self):
		self.debit_account = self.account
		self.credit_account = frappe.get_doc("Account", "Sales")

	def on_submit(self):
		self.amount = self.rate * self.quantity
		super().on_submit()
		# update item qty

# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe

from accounting.controllers.transaction import Transaction


class SalesInvoice(Transaction):

	def before_submit(self):
		self.debit_account = "Sales"
		customer = frappe.get_doc("Customer", self.customer)
		self.credit_account = customer.account

	def on_submit(self):
		item = frappe.get_doc("Item", self.item)
		self.amount = item.price * self.quantity
		super().on_submit()
		# update item qty

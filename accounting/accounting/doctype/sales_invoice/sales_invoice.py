# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe

from accounting.controllers.transaction import Transaction


class SalesInvoice(Transaction):

	def __init__(self):
		self.debit_account = frappe.get_doc("Account", "Sales")
		self.credit_account = self.account

	def on_submit(self):
		self.amount = self.item.price * self.quantity
		super().on_submit()
		# update item qty

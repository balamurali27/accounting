# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from datetime import date

import frappe
from frappe.model.document import Document


class Transaction(Document):
	"""Generic controller for double entry transactions."""

	def _make_gl_entries(self, amount: int):
		try:
			frappe.get_doc(
				doctype="GL Entry",
				posting_date=date.today,
				account=self.debit_account,
				debit=amount
			).insert()
			frappe.get_doc(
				doctype="GL Entry",
				posting_date=date.today,
				account=self.credit_account,
				credit=amount
			).insert()
		except frappe.exceptions.ValidationError:
			frappe.db.rollback()

	def on_submit(self):
		self._make_gl_entries(self.amount)

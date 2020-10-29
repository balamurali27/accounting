# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from datetime import date

import frappe
from frappe.model.document import Document


class Transaction(Document):
	"""Generic controller for double entry transactions."""

	def _make_gl_entry(self, account: str, debit: float = 0, credit: float = 0):
		"""Make GL Entry for today with voucher info."""
		frappe.get_doc(
			doctype="GL Entry",
			posting_date=date.today(),
			account=account,
			debit=debit,
			credit=credit,
			voucher_type=self.doctype,
			voucher_no=self.name
		).insert()

	def _make_gl_entries(self, amount: float):
		try:
			self._make_gl_entry(self.debit_account, debit=amount)
			self._make_gl_entry(self.credit_account, credit=amount)
		except frappe.exceptions.ValidationError:
			frappe.db.rollback()

	def on_submit(self):
		self._make_gl_entries(self.amount)

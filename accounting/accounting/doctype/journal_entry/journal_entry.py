# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _

from accounting.controllers.transaction import Transaction


class JournalEntry(Transaction):

	def _check_for_balanced_entries(self):
		debit_sum = 0
		credit_sum = 0
		for entry in self.accounts:
			debit_sum += entry.debit
			credit_sum += entry.credit
		if debit_sum != credit_sum:
			frappe.throw(
				msg=_(
					"Total credits don't equal debits. Make them equal and try again."
				),
				exc=frappe.exceptions.LinkValidationError,
			)

	def before_submit(self):
		self._check_for_balanced_entries()

	def _make_gl_entries_for_accounts(self):
		for entry in self.accounts:
			self._make_gl_entry(
				account=entry.account, debit=entry.debit, credit=entry.credit
			)

	def on_submit(self):
		self._make_gl_entries_for_accounts()

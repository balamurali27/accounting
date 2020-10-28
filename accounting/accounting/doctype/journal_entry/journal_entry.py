# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe import _
from datetime import date

import frappe

from frappe.model.document import Document


class JournalEntry(Document):

	def _check_for_balanced_entries(self):
		debit_sum = 0
		credit_sum = 0
		for account in self.accounts:
			debit_sum += account.debit
			credit_sum += account.credit
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
		for account in self.accounts:
			frappe.get_doc(
				doctype="GL Entry",
				posting_date=date.today(),
				account=account.account,
				debit=account.debit,
				credit=account.credit
			).insert()

	def on_submit(self):
		self._make_gl_entries_for_accounts()

# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and Contributors
# See license.txt
from __future__ import unicode_literals

from datetime import date
from typing import List

import frappe

from accounting.controllers.test_transaction import TestTransaction

from ..account.test_account import create_test_accounts


def get_test_journal_entry_account(credit: int = 0, debit: int = 0):
	create_test_accounts()
	return frappe.get_doc({
		"doctype": "Journal Entry Account",
		"account": "Debtors",
		"debit": debit,
		"credit": credit
	})


def get_test_journal_entry(accounts: List):
	return frappe.get_doc({
		"doctype": "Journal Entry",
		"accounts": accounts,
		"posting_date": date.today()
	})


class TestJournalEntry(TestTransaction):

	def test_journal_submission_creates_balanced_gl_entries(self):
		"""Ensure submitting JournalEntry creates balanced GL entries."""
		accounts = [
			get_test_journal_entry_account(100, 0).as_dict(),
			get_test_journal_entry_account(0, 100).as_dict()
		]
		journal_entry = get_test_journal_entry(accounts)
		before = frappe.db.count("GL Entry")

		journal_entry.submit()

		after = frappe.db.count("GL Entry")
		gl_count_increase = after - before
		self.assertEqual(gl_count_increase, 2, msg=frappe.get_all("GL Entry"))
		self._test_gl_entries_are_balanced()

	def test_exception_is_thrown_if_accounting_entries_arent_balanced(self):
		"""
		Ensure submitting JournalEntry with unbalanced accounting entries throws err.
		"""
		accounts = [
			get_test_journal_entry_account(100, 0).as_dict(),
		]
		journal_entry = get_test_journal_entry(accounts)
		self.assertRaises(
			frappe.exceptions.ValidationError, journal_entry.submit
		)
		accounts = [
			get_test_journal_entry_account(100, 0).as_dict(),
			get_test_journal_entry_account(0, 100).as_dict(),
			get_test_journal_entry_account(0, 100).as_dict(),
		]
		journal_entry = get_test_journal_entry(accounts)
		self.assertRaises(
			frappe.exceptions.ValidationError, journal_entry.submit
		)

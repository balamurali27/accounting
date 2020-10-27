# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and Contributors
# See license.txt
from __future__ import unicode_literals

import unittest

import frappe


class TestTransaction(unittest.TestCase):
	"""Generic test case for double entry transactions."""

	def setUp(self):
		pass

	def tearDown(self):
		frappe.db.rollback()

	def _test_gl_entries_are_balanced(self):
		"""Test if sum(credits) = sum(debits)."""
		credit_sum = frappe.db.sql("SELECT SUM(credit) FROM `tabGL Entry`")[0]
		debit_sum = frappe.db.sql("SELECT SUM(debit) FROM `tabGL Entry`")[0]
		self.assertEqual(credit_sum, debit_sum)

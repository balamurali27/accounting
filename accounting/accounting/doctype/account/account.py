# -*- coding: utf-8 -*-
# Copyright (c) 2020, Balamurali M and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import json

import frappe
from frappe.utils.nestedset import NestedSet, rebuild_tree


def is_group(child: dict) -> bool:
	"""Return true if child is a group."""
	if child.get("is_group"):
		return True
	elif len(
		set(child.keys()) - set([
			"account_type", "root_type", "is_group", "tax_rate",
			"account_number"
		])
	):
		return True
	return False


class Account(NestedSet):

	@classmethod
	def _import_accounts(cls, children, parent, root_type, root_account=False):
		for account_name, child in children.items():
			if root_account:
				root_type = child.get("root_type")
			if account_name in [
				"account_number", "account_type", "root_type", "is_group",
				"tax_rate"
			]:
				continue

			account = frappe.get_doc({
				"doctype": "Account",
				"account_name": account_name,
				"parent_account": parent,
				"is_group": is_group(child),
				"root_type": root_type,
				"account_number": child.get("account_number"),
				"account_type": child.get("account_type"),
			})
			account.insert(ignore_if_duplicate=True)

			cls._import_accounts(child, account.name, root_type)

	@classmethod
	def load_tree_from_json(cls, file):
		"""Load account tree from a standard json file"""
		with open(file, "r") as f:
			coa: dict = json.load(f)
		chart: dict = coa["tree"]
		cls._import_accounts(chart, None, None, root_account=True)
		rebuild_tree("Account", "parent_account")

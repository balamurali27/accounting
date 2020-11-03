# Copyright (c) 2013, Balamurali M and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from typing import List, Dict, Tuple

import frappe
from frappe import _
from frappe.utils.nestedset import get_descendants_of

from accounting.accounting.report.profit_and_loss.profit_and_loss import \
	get_date_filter

asset_name = "Application of Funds (Assets)"
liability_name = "Source of Funds (Liabilities)"
asset_accounts = [asset_name] + get_descendants_of("Account", asset_name)
liability_accounts = [liability_name] + get_descendants_of("Account", liability_name)

def get_balance_sheet_data(filters: Dict) -> Dict:
	date_filter = get_date_filter(filters)
	assets = frappe.get_list(
		"GL Entry",
		filters={
			**{
				"account": ["in", asset_accounts]
			},
			**date_filter
		},
		fields=['account', 'sum(debit) as amount'],
		group_by='account'
	)
	liabilities = frappe.get_list(
		"GL Entry",
		filters={
			**{
				"account": ["in", liability_accounts]
			},
			**date_filter
		},
		fields=['account', 'sum(debit) as amount'],
		group_by='account'
	)
	return assets + [{}] + liabilities


def execute(filters: Dict = None) -> Tuple[List[Dict], List[Dict]]:
	data = get_balance_sheet_data(filters)
	columns = [{
		"fieldname": "account",
		"label": _("Account"),
		"fieldtype": "Link",
		"options": "Account",
		"width": 300
	}, {
		"fieldname": "amount",
		"label": _("Amount"),
		"fieldtype": "int",
		"width": 300
	}]
	return columns, data

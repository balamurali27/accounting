# Copyright (c) 2013, Balamurali M and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from typing import Dict, List, Tuple

import frappe
from frappe import _
from frappe.utils.nestedset import get_descendants_of

income_accounts = ["Income"] + get_descendants_of("Account", "Income")
expense_accounts = ["Expenses"] + get_descendants_of("Account", "Expenses")


def get_date_filter(filters: Dict) -> Dict:
	from_date = filters.get('from_date')
	to_date = filters.get('to_date')
	if from_date and to_date:
		return {"posting_date": ['between', (from_date, to_date)]}
	elif from_date:
		return {"posting_date": ['>=', from_date]}
	elif to_date:
		return {"posting_date": ['<=', to_date]}
	else:
		return {}


def get_profit_loss_data(filters: Dict = None) -> List[Dict]:
	date_filter = get_date_filter(filters)
	incomes = frappe.get_list(
		"GL Entry",
		filters={
			**{
				"account": ["in", income_accounts]
			},
			**date_filter
		},
		fields=['account', 'sum(debit) as amount'],
		group_by='account'
	)
	expenses = frappe.get_list(
		"GL Entry",
		filters={
			**{
				"account": ["in", expense_accounts]
			},
			**date_filter
		},
		fields=['account', '-1 * sum(debit) as amount'],
		group_by='account'
	)
	total_income = {
		"account": "Total Income",
		"amount": sum(d['amount'] for d in incomes)
	}
	total_expense = {
		"account": "Total Expenses",
		"amount": sum(d['amount'] for d in expenses)
	}

	# expense is -ve
	net_profit = total_income['amount'] + total_expense['amount']
	net_profit_or_loss = {
		"account": "Net Profit" if net_profit >= 0 else "Net Loss",
		"amount": net_profit
	}
	data = incomes + [total_income] + [{}] + expenses + [total_expense] + [
		net_profit_or_loss
	]

	return data


def execute(filters=None) -> Tuple[List[Dict], List[Dict]]:
	data = get_profit_loss_data(filters)
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

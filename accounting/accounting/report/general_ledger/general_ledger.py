# Copyright (c) 2013, Balamurali M and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

from typing import Dict, List

import frappe
from frappe import _

from accounting.accounting.report.profit_and_loss.profit_and_loss import \
	get_date_filter


def get_voucher_filter(filters: Dict = None) -> Dict:
	voucher_no = filters.get('voucher_no')
	voucher_type = filters.get('voucher_type')
	ret = {}
	if voucher_type:
		ret.update({"voucher_type": voucher_type})
	if voucher_no:
		ret.update({"voucher_no": voucher_no})
	return ret


def get_general_ledger_data(filters: Dict = None) -> List[Dict]:
	date_filter = get_date_filter(filters)
	voucher_filter = get_voucher_filter(filters)
	gl_entries = frappe.get_list(
		"GL Entry",
		filters={
			**date_filter,
			**voucher_filter
		},
		fields=['account', 'debit', 'credit', 'voucher_no', 'voucher_type'],
	)

	data = gl_entries
	return data


def execute(filters=None):
	data = get_general_ledger_data(filters)
	columns = [{
		"fieldname": "account",
		"label": _("Account"),
		"width": 100
	}, {
		"fieldname": "debit",
		"label": _("Debit"),
		"width": 100
	}, {
		"fieldname": "credit",
		"label": _("Credit"),
		"width": 100
	}, {
		"fieldname": "voucher_no",
		"label": _("Debit"),
		"width": 100
	}, {
		"fieldname": "voucher_type",
		"label": _("Voucher Type"),
		"width": 200
	}]
	return columns, data

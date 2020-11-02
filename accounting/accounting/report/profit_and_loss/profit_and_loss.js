// Copyright (c) 2016, Balamurali M and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports['Profit and Loss'] = {
	filters: [
		{
			fieldname: 'from_date',
			label: __('From'),
			fieldtype: 'Date',
		},
		{
			fieldname: 'to_date',
			label: __('To'),
			fieldtype: 'Date',
			reqd: 1,
			default: frappe.datetime.get_today()
		},
	],
};

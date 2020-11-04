// Copyright (c) 2020, Balamurali M and contributors
// For license information, please see license.txt

frappe.ui.form.on('Journal Entry', {
	refresh: function (frm) {
		console.log(frm.doc.name);
		frm.add_custom_button(__('Accounting Ledger'), function () {
			frappe.set_route('query-report', 'General Ledger', {
				voucher_type: 'Journal Entry',
				voucher_no: frm.doc.name,
			});
		});
	},
});

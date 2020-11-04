// Copyright (c) 2020, Balamurali M and contributors
// For license information, please see license.txt

frappe.ui.form.on('Sales Invoice', {
	refresh: function (frm) {
		frappe.require('/assets/accounting/js/utils.js', () => {
			add_accounting_ledger_btn(frm);
		});
	},
});

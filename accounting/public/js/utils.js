function add_accounting_ledger_btn(frm) {
	frm.add_custom_button(__('Accounting Ledger'), function () {
		frappe.set_route('query-report', 'General Ledger', {
			voucher_type: frm.doc.doctype,
			voucher_no: frm.doc.name,
		});
	});
}

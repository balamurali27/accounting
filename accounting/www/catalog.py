from __future__ import unicode_literals

import frappe
from frappe import _


def get_context(context):
	if frappe.session.user == "Guest":
		frappe.throw(_("Log in to access this page."), frappe.PermissionError)
	context.items = frappe.get_all(
		"Item", fields=['name', 'item_name', 'description', 'price', 'image']
	)

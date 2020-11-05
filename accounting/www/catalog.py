from __future__ import unicode_literals
import frappe


def get_context(context):
	context.items = frappe.get_all(
		"Item", fields=['name', 'item_name', 'description', 'price', 'image']
	)

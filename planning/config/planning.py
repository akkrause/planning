from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
		{
			"label": _("Planning"),
			"items": [
				{
					"type": "doctype",
					"name": "Operation Schedule",
					"description": _("Schedule of planned operations."),
				},
				{
					"type": "doctype",
					"name": "Material Schedule",
					"description": _("Schedule of planned material transaction."),
				},

			]
		}
	]

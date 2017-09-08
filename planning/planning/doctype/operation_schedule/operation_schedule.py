# -*- coding: utf-8 -*-
# Copyright (c) 2017, akrause and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class OperationSchedule(Document):
	pass

@frappe.whitelist()
def get_events(start, end, filters=None):
	"""Returns events for Gantt / Calendar view rendering.

	:param start: Start date-time.
	:param end: End date-time.
	:param filters: Filters (JSON).
	"""
	from frappe.desk.calendar import get_event_conditions
	conditions = get_event_conditions("Operation Schedule", filters)

	data = frappe.db.sql("""select name, operation, planned_start_date,
		planned_end_date, status
		from `tabProduction Order`
		where ((ifnull(planned_start_date, '0000-00-00')!= '0000-00-00') \
				and (planned_start_date <= %(end)s) \
			and ((ifnull(planned_start_date, '0000-00-00')!= '0000-00-00') \
				and planned_end_date >= %(start)s)) {conditions}
		""".format(conditions=conditions), {
			"start": start,
			"end": end
		}, as_dict=True, update={"allDay": 0})
	return data

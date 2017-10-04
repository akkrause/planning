// Copyright (c) 2017, akrause and contributors
// For license information, please see license.txt

frappe.views.calendar["Operation Schedule"] = {
	field_map: {
		"start": "planned_start_time",
		"end": "planned_end_time",
		"id": "name",
		"title": "operation",
		"status": "status",
		"allDay": "allDay"
	},
	get_events_method: "planning.planning.doctype.operation_schedule.operation_schedule.get_events"
}
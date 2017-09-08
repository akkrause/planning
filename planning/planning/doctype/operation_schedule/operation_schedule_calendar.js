// Copyright (c) 2017, akrause and contributors
// For license information, please see license.txt

frappe.views.calendar["Operation Schedule"] = {
	field_map: {
		"start": "planned_start_date",
		"end": "planned_end_date",
		"id": "name",
		"title": "operation",
		"status": "status";
	},
	gantt: true,
	get_css_class: function(data) {
		if(data.status==="Completed") {
			return "success";
		} else if(data.status==="In Process") {
			return "warning";
		} else {
			return "danger";
		}
	},
	filters: [
		{
			"fieldtype": "Link",
			"fieldname": "sales_order",
			"options": "Sales Order",
			"label": __("Sales Order")
		}	
	],
	get_events_method: "planning.planning.doctype.operation_schedule.operation_schedule.get_events"
}
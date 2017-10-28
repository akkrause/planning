# -*- coding: utf-8 -*-
# Copyright (c) 2017, akrause and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from operator import attrgetter

class PlanningSettings(Document):

	def __init__(self, arg1, arg2=None):
		super(PlanningSettings, self).__init__(arg1, arg2)
		self.holiday_list = frappe.db.sql("""SELECT name,
				parent,
				parentfield,
				parenttype,
				holiday_date,
				description
				FROM `tabHoliday`;""", as_dict=1)
		self.workstation_list = frappe.db.sql("SELECT name, holiday_list FROM `tabWorkstation`;", as_dict=1)
		
	def clear_tables(self):
		frappe.db.sql("""delete
			from `tabOperation Schedule`;""")
		frappe.db.sql("""delete
			from `tabMaterial Schedule`;""")
			
	def get_production_order_operations(self):
		poo_list = frappe.db.sql("""SELECT name,
				parent,
				parentfield,
				parenttype,
				idx,
				operation,
				planned_end_time,
				time_in_mins,
				status,
				planned_operating_cost,
				description,
				planned_start_time,
				workstation,
				hour_rate,
				completed_qty,
				bom
			FROM `tabProduction Order Operation`
			WHERE status <> 'Completed';""", as_dict=1)
					
	def run_planning(self):
#		for p in sorted(self.holiday_list, key=attrgetter('holiday_date')):
#			print p.name, p.parent, p.holiday_date, p.description
		print self.workstation_list

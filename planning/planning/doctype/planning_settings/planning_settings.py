# -*- coding: utf-8 -*-
# Copyright (c) 2017, akrause and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from operator import attrgetter

class PlanningSettings(Document):

	def clear_tables(self):
		frappe.db.sql("""delete
			from `tabOperation Schedule`;""")
		frappe.db.sql("""delete
			from `tabMaterials Schedule`;""")
			
	def get_production_order_operations(self):
		poo_list = frappe.db.sql("""SELECT name,
				creation,
				modified,
				modified_by,
				owner,
				docstatus,
				parent,
				parentfield,
				parenttype,
				idx,
				operation,
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
			
			
		for p in sorted(poo_list, key=attrgetter('planned_start_time')):
			print p.name, p.parent, p.status, p.planned_start_time, p.time_in_mins
				
	def run_planning(self):
		self.get_production_order_operations()
		

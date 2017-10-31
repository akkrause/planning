# -*- coding: utf-8 -*-
# Copyright (c) 2017, akrause and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from operator import attrgetter
from datetime import date

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
		self.workstation_list = frappe.db.sql("""SELECT name,
				holiday_list
				FROM `tabWorkstation`;""", as_dict=1)
		self.poo_list = []
		
	def clear_tables(self):
		frappe.db.sql("""delete
			from `tabOperation Schedule`;""")
		frappe.db.sql("""delete
			from `tabMaterial Schedule`;""")
			
	def get_production_order_operations(self):
		self.poo_list = frappe.db.sql("""SELECT poo.name,
				poo.parent,
				poo.parentfield,
				poo.parenttype,
				poo.operation,
				poo.time_in_mins,
				poo.status,
				poo.planned_operating_cost,
				poo.description,
				poo.workstation,
				poo.hour_rate,
				poo.completed_qty,
				po.expected_delivery_date
			FROM `tabProduction Order Operation` AS poo
			INNER JOIN `tabProduction Order` AS po
				ON po.name = poo.parent
			WHERE poo.status <> 'Completed';""", as_dict=1)
					
	def run_planning(self):
		self.clear_tables()
		self.get_production_order_operations()
		
		for p in self.poo_list:
			if any((x.parent == "Production" and x.holiday_date == date(2017,11,25)) for x in self.holiday_list):
#			if any((x.parent == "Production")  for x in self.holiday_list):
				for p in self.holiday_list:
					print p.parent, p.holiday_date, p.description
#		for p in sorted(self.poo_list, key=attrgetter('holiday_date')):
#			print p.name, p.parent, p.workstation, p.expected_delivery_date

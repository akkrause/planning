# -*- coding: utf-8 -*-
# Copyright (c) 2017, akrause and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.utils import cstr, flt, cint, nowdate, add_days, comma_and
import frappe
from frappe.model.document import Document
from operator import attrgetter
from datetime import date, datetime, timedelta

class PlanningSettings(Document):

	def __init__(self, arg1, arg2=None):
		super(PlanningSettings, self).__init__(arg1, arg2)
		self.holiday = frappe.db.sql("""
				SELECT name,
					parent,
					parentfield,
					parenttype,
					holiday_date,
					description
				FROM `tabHoliday`;""", as_dict=1)
		self.workstation_list = frappe.db.sql("""
				SELECT name,
					holiday_list
				FROM `tabWorkstation`;""", as_dict=1)
		self.workstation_hours = frappe.db.sql("""
				SELECT parent,
					idx,
					start_time,
					end_time
				FROM `tabWorkstation Working Hour`;""", as_dict=1)
#		self.plan_time = datetime.now()
		
	def clear_tables(self):
		frappe.db.sql("""delete
			from `tabOperation Schedule`;""")
		frappe.db.sql("""delete
			from `tabMaterial Schedule`;""")
			
	def run_planning(self):
		self.clear_tables()
		plan_time = datetime.now()
		
		po_list = frappe.db.sql("""
				SELECT
					name,
					status,
					production_item,
					description,
					expected_delivery_date
				FROM `tabProduction Order`
				WHERE status not IN ('Completed', 'Cancelled', 'Closed', 'Stopped')""", as_dict=1)
		
		for po in sorted(po_list, key=attrgetter('expected_delivery_date')):
			self.schedule_operations(po, plan_time)
			
	def schedule_operations(self, po, plan_time):
		poo_list = frappe.db.sql("""
			SELECT name,
				parent,
				parentfield,
				parenttype,
				idx,
				operation,
				time_in_mins,
				status,
				planned_operating_cost,
				description,
				workstation,
				hour_rate,
				completed_qty
			FROM `tabProduction Order Operation`
			WHERE parent = '{po}';""".format(po=po.name), as_dict=1)
		
		for o in sorted(poo_list, key=attrgetter('idx')):
			ps = frappe.new_doc("Operation Schedule")
			ps.update(o)
			
			plan_time = self.find_start_plan_time(o, plan_time)
			
			
			print o.parent, o.idx, o.operation, o.time_in_mins
			print plan_time
		
#			if any((x.parent == "Production" and x.holiday_date == date(2017,11,25)) for x in self.holiday_list):
#			if any((x.parent == "Production")  for x in self.holiday_list):
#				for p in self.holiday_list:
#					print p.parent, p.holiday_date, p.description
#		for p in sorted(self.poo_list, key=attrgetter('holiday_date')):
#			print p.name, p.parent, p.workstation, p.expected_delivery_date
			
	def find_start_plan_time(self, o, plan_time):
		plan_time = self.skip_holidays(o, plan_time)
		return plan_time
		
	def skip_holidays(self, o, plan_time):
		if any((x.name == o.workstation) for x in self.workstation_list):
			holiday_list = next(x.holiday_list for x in self.workstation_list if x.name == o.workstation)
			plan_date = plan_time.date()
			if any((x.holiday_date == plan_date and x.parent == holiday_list) for x in self.holiday):
				plan_time = datetime.combine(plan_date + timedelta(1), datetime.min.time())
				self.skip_holidays(o, plan_time)
		return plan_time
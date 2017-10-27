// Copyright (c) 2017, akrause and contributors
// For license information, please see license.txt

frappe.ui.form.on('Planning Settings', {
	'Run Now': function(frm) {
		frappe.call({
			method:"run_planning",
		});
	}
});

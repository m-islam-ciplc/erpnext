# Copyright (c) 2025, Confidence Infrastructure PLC and contributors
# License: GNU General Public License v3. See license.txt

import frappe
from frappe.utils import cint

from erpnext.assets_only.config import ASSETS_ONLY_MODE, VISIBLE_DESKTOP_ICONS


def is_assets_only_mode() -> bool:
	return bool(ASSETS_ONLY_MODE)


@frappe.whitelist()
def apply_desktop_icon_visibility():
	"""Hide ERPNext desk modules except Assets and Organization."""
	if not is_assets_only_mode():
		return {"skipped": True}

	icons = frappe.get_all(
		"Desktop Icon",
		filters={"app": "erpnext", "standard": 1},
		fields=["name", "hidden"],
	)

	updated = 0
	for icon in icons:
		hidden = 0 if icon.name in VISIBLE_DESKTOP_ICONS else 1
		if cint(icon.hidden) != hidden:
			frappe.db.set_value("Desktop Icon", icon.name, "hidden", hidden, update_modified=False)
			updated += 1

	_set_default_workspace_for_assets_only()

	frappe.db.commit()
	frappe.clear_cache()
	return {"updated": updated, "visible": sorted(VISIBLE_DESKTOP_ICONS)}


def _set_default_workspace_for_assets_only():
	"""Open Assets workspace after login (/desk, not /desk/assets)."""
	if not frappe.db.exists("Workspace", "Assets"):
		return

	for user in frappe.get_all("User", filters={"enabled": 1, "user_type": "System User"}, pluck="name"):
		frappe.db.set_value("User", user, "default_workspace", "Assets", update_modified=False)


@frappe.whitelist()
def restore_desktop_icon_visibility():
	"""FULL_ERP: show all standard ERPNext desk icons again."""
	icons = frappe.get_all("Desktop Icon", filters={"app": "erpnext", "standard": 1}, pluck="name")
	for name in icons:
		frappe.db.set_value("Desktop Icon", name, "hidden", 0, update_modified=False)

	frappe.db.commit()
	frappe.clear_cache()
	return {"restored": len(icons)}

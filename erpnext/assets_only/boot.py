# Copyright (c) 2025, Confidence Infrastructure PLC and contributors
# License: GNU General Public License v3. See license.txt

import frappe

from erpnext.assets_only.desktop import is_assets_only_mode


def extend_bootinfo(bootinfo):
	"""Mark assets-only mode. Do not override bootinfo['home_page'] — it must be a Page name (e.g. 'desktop'), not a URL."""
	if not is_assets_only_mode():
		return

	bootinfo["assets_only_mode"] = True
	# Default workspace is set on User records via desktop.apply_desktop_icon_visibility()

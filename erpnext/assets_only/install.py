# Copyright (c) 2025, Confidence Infrastructure PLC and contributors
# License: GNU General Public License v3. See license.txt

from erpnext.assets_only.desktop import apply_desktop_icon_visibility, is_assets_only_mode


def run_after_install():
	"""Run default ERPNext install, then apply assets-only desk visibility."""
	from erpnext.setup.install import after_install

	after_install()

	if is_assets_only_mode():
		apply_desktop_icon_visibility()

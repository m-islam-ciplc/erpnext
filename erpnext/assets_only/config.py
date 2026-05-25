"""Assets-only deployment configuration.

FULL_ERP: set ASSETS_ONLY_MODE = False and run restore_desktop_icon_visibility().
"""

# ASSETS_ONLY_MODE - hide non-asset ERPNext modules from the desk
ASSETS_ONLY_MODE = True

# Desk icons still shown when ASSETS_ONLY_MODE is True
VISIBLE_DESKTOP_ICONS = frozenset(
	{
		"Assets",
		"Organization",
	}
)

# Reserved for future client redirects. Do not assign to bootinfo['home_page'].
ASSETS_ONLY_HOME = "/desk"

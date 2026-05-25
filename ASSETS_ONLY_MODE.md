# Assets-Only Mode (asset-dev)

> ## ⛔ CRITICAL — READ FIRST
>
> **NEVER DELETE** ERPNext module code, workspaces, or doctypes to simplify the app.
> Asset-only mode = **disable / comment / hide only**, so **full ERP can be restored later**.
> AI agents: `.cursor/rules/never-delete-erpnext-modules.mdc` + `fixed-assets-project.mdc` (always apply).

This branch customizes ERPNext for **group-wide fixed asset management** while keeping the full ERPNext codebase intact for a possible future full-ERP rollout.

## External systems

| System | Role |
|--------|------|
| Procurement software | Purchase / PO / GRN |
| Tally | Accounting & vouchers |
| LDAP | User directory |
| ERPNext | Asset register, depreciation schedules, custodian/location, reports |

## Scope

- All fixed asset types (see `asset categories demo.txt`), not IT-only.
- Existing assets + assets capitalized after procurement (no ERPNext buying flow).
- Custodian and Asset Movement for assignments across the group.

## Do not delete code

Irrelevant modules (Accounts, Stock, Selling, Buying, HR, etc.) must **remain in the repo**.

Disable them using:

- `ASSETS_ONLY_MODE` flag (to be added in custom config)
- Commented sections in `hooks.py` marked `ASSETS_ONLY_MODE` / `FULL_ERP`
- Role permissions and hidden workspaces (`is_hidden`)
- New additive files (reports, custom fields, LDAP sync)

## Restore full ERP

1. Set `ASSETS_ONLY_MODE = False` in `erpnext/assets_only/config.py`
2. Set `app_home = "/desk"` in `erpnext/hooks.py`
3. Set `after_install = "erpnext.setup.install.after_install"` in `erpnext/hooks.py`
4. Run: `bench --site <site> execute erpnext.assets_only.desktop.restore_desktop_icon_visibility`
5. `bench clear-cache`

No module reinstall required.

## Apply desk hiding on an existing site

```bash
bench --site assets.localhost execute erpnext.assets_only.desktop.apply_desktop_icon_visibility
bench --site assets.localhost clear-cache
```

Hard-refresh the browser (Ctrl+Shift+R).

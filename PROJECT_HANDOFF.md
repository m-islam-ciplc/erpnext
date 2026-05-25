# ERPNext Fixed Assets Project — Handoff Notes

**Saved from chat:** May 2026  
**Company:** Confidence Infrastructure PLC ([confidenceinfrastructure.com](https://confidenceinfrastructure.com/))  
**Branch:** `asset-dev` (from `version-16`)  
**Purpose:** Group-wide fixed asset register + depreciation; not full ERP today.

---

## 1. What you are building

| System | Role |
|--------|------|
| **ERPNext (this project)** | Fixed asset register, depreciation schedules, custodian/location, reports |
| **Procurement software** | All purchases / PO / GRN |
| **Tally** | Accounting and vouchers |
| **LDAP** (planned) | User directory → Employee for custodian |

**Scope:** All fixed asset types for the **group** (manufacturing, dredging, EPC) — **not IT-only**.  
**Companies:** Start with **Confidence Infrastructure PLC** only; add Zodiac Dredging, Steel, Concrete, Electric, etc. later as separate **Company** records in ERPNext.

**Asset entry:** Use **Existing Asset** (no Purchase Invoice / Purchase Receipt in ERPNext). Future assets from procurement are registered when received/capitalized, with procurement reference fields (planned).

---

## 2. Critical project rule (never break)

**NEVER DELETE** ERPNext module code (Accounts, Stock, HR, Buying, etc.) to simplify the app.

- **Disable only:** comment blocks, config flags, `hidden` on desk icons, permissions.
- **Tags:** `# ASSETS_ONLY_MODE` / `# FULL_ERP: restore by uncommenting`
- **Docs:** `ASSETS_ONLY_MODE.md`, `.cursor/rules/fixed-assets-project.mdc`, `.cursor/rules/never-delete-erpnext-modules.mdc`

**Restore full ERP later:** Set `ASSETS_ONLY_MODE = False` in `erpnext/assets_only/config.py`, restore hooks, run `restore_desktop_icon_visibility()`.

---

## 3. Environment (Windows + WSL + Docker)

| Item | Value |
|------|--------|
| Windows repo | `d:\GitHub_m-islam-ciplc\erpnext` |
| WSL bench | `~/frappe-bench` (user `mislam`) |
| ERPNext symlink | `~/frappe-bench/apps/erpnext` → `/mnt/d/GitHub_m-islam-ciplc/erpnext` |
| Site name | `assets.localhost` |
| ERPNext / Frappe | v16 |
| Python | 3.14 |
| Node | 24 |

**Docker (not WSL MariaDB):**

| Container | Port | Password |
|-----------|------|----------|
| `assets-dev-mariadb` | **3307** | `admin` (root) |
| `assets-dev-redis` | **6380** | — |

**Start stack:**

```powershell
docker start assets-dev-mariadb assets-dev-redis
wsl -d Ubuntu bash -lc "redis-cli -p 6380 ping && sleep 3 && cd ~/frappe-bench && bench start"
```

**LAN (optional, was reset):** Run `scripts/open-lan-access.ps1` as Administrator when needed.

**URLs:**

- Local: **http://127.0.0.1:8000**
- Login: **Administrator** / **admin**
- After login: app uses **`/desk`** (do not bookmark `/desk/assets` — invalid)

**MySQL Workbench:** Host `127.0.0.1`, Port `3307`, User `root`, Password `admin`

**Site DB user** (auto-generated; in `sites/assets.localhost/site_config.json`):

- Read from: `~/frappe-bench/sites/assets.localhost/site_config.json`

---

## 4. Factory reset (done)

- Site dropped and recreated; old DB removed.
- Archived site folder deleted (no old data kept).
- Redis flushed.
- Setup wizard must be completed again if starting fresh.
- **Developer mode:** on  
- **Public signup:** disabled  

**Re-run reset:**

```bash
bash /mnt/d/GitHub_m-islam-ciplc/erpnext/scripts/reset-site.sh
```

---

## 5. ERPNext defaults vs your data

**ERPNext ships NO default Asset Categories.** You create them manually.

**Standard Chart of Accounts** (after Setup Wizard) includes fixed asset **accounts**, not categories:

- Capital Equipment, Electronic Equipment, Furniture and Fixtures, Office Equipment, Plants and Machineries, Buildings, Software  
- Accumulated Depreciation, CWIP Account  
- **No Land account** in standard chart (add if needed)

**Depreciation requires CoA accounts:** Fixed Asset on Asset Category; Accumulated Depreciation + Depreciation Expense on category or Company defaults. Tally remains books; ERPNext still needs account links for depreciation engine.

---

## 6. Recommended asset categories (manufacturing + dredging + EPC)

Broad **Asset Categories** (Items hold detail like Laptop, Dredger, Crane):

1. Land  
2. Buildings & Civil Works  
3. Plant & Machinery  
4. **Dredging & Marine**  
5. **EPC / Construction Plant**  
6. Vehicles  
7. Electrical & Power Equipment  
8. Computer & IT Equipment  
9. Office Equipment  
10. Furniture & Fixtures  
11. Tools & Workshop Equipment  
12. Laboratory & Testing Equipment  
13. Leasehold Improvements  
14. Intangible Assets  
15. Capital Work in Progress (CWIP)  

Reference file in repo: `asset categories demo.txt`

**Map categories to CoA accounts** (e.g. Dredging → Capital Equipment or Plants and Machineries; IT → Electronic Equipment).

---

## 7. Custodian / assignment (built-in)

- **Asset** field: **Custodian** → **Employee**  
- **Asset Movement:** Issue / Receipt / Transfer  
- **LDAP (planned):** Users from LDAP → link/create **Employee** records  

**Employee** link added under **Assets → Setup** in workspace sidebar.

---

## 8. Code built on `asset-dev` (assets-only UI)

**New module:** `erpnext/assets_only/`

| File | Purpose |
|------|---------|
| `config.py` | `ASSETS_ONLY_MODE = True` |
| `desktop.py` | Hide/show desk icons; set User `default_workspace` = Assets |
| `boot.py` | `assets_only_mode` flag in bootinfo (**do not** set `home_page` to a URL) |
| `install.py` | Chains `after_install` + applies visibility |

**Hooks changed:** `erpnext/hooks.py`

- `after_install` → `erpnext.assets_only.install.run_after_install`  
- `extend_bootinfo` → includes `erpnext.assets_only.boot.extend_bootinfo`  
- `app_home` = `/desk`  

**Visible on desk:** **Assets**, **Organization** only (18 other ERPNext tiles hidden in DB).

**Apply / restore:**

```bash
bench --site assets.localhost execute erpnext.assets_only.desktop.apply_desktop_icon_visibility
bench --site assets.localhost execute erpnext.assets_only.desktop.restore_desktop_icon_visibility
bench --site assets.localhost clear-cache
```

---

## 9. Important bugs / lessons from chat

1. **Wrong menu:** Finance Book is **not** under Assets — it is under **Accounting → Invoicing** (or search). Optional for simple setup.  
2. **Wrong URL:** `/desk/assets` → Page not found. Use **http://127.0.0.1:8000** and log in; Frappe uses `/desk` and default workspace **Assets**.  
3. **`home_page` bug:** Must be a Page name (e.g. `desktop`), **not** `/desk`. Fixed in `assets_only/boot.py`.  
4. **Verify from code/site** — do not ask user to confirm what DB/code can answer.  
5. **Never delete modules** — comment/flag/hide only.

---

## 10. Framework vs ERPNext menus (what you need)

| Keep / use | Ignore for now |
|------------|----------------|
| **Assets** (main app) | Hidden ERPNext modules (Accounting, Stock, …) |
| **Organization** (Company, User, Department) | Website |
| **Search** | **Build** for end users (dev only; developer mode on) |
| **Settings → LDAP** (when ready) | Full accounting workflows |
| **Data Import** (bulk assets later) | |

**Frappe** = framework (login, desk, permissions, settings). **ERPNext** = business modules. Your product is **Assets** + minimal **Organization**.

---

## 11. Implementation plan (one step at a time)

**Done:**

- Environment + site reset  
- Project rules saved (`.cursor/rules/`, `ASSETS_ONLY_MODE.md`)  
- Assets-only desk hiding (Phase 2 partial)  
- Employee link on Assets sidebar  

**Next (in order):**

1. **You:** Setup Wizard + first **Asset Category** + test asset (Existing Asset)  
2. **Code:** Procurement custom fields on Asset; default Existing Asset  
3. **Code:** LDAP + Employee sync  
4. **Code:** Depreciation export for Tally (schedules in ERPNext; posting optional)  
5. **Later:** Procurement import/API; other group companies  

---

## 12. Decisions still open

1. LDAP type (Active Directory vs OpenLDAP)?  
2. Track assets **on order** before receipt, or only when received?  
3. Tally: manual monthly export OK for v1?  
4. When to add other group companies as ERPNext **Company** records?

---

## 13. Key file paths

```
erpnext/
  assets_only/           # assets-only mode (no module deletion)
  hooks.py               # boot + after_install hooks
  workspace_sidebar/assets.json   # + Employee under Setup
  ASSETS_ONLY_MODE.md
  PROJECT_HANDOFF.md     # this file
  asset categories demo.txt
  scripts/
    reset-site.sh        # full site reset
    open-lan-access.ps1  # LAN access (Windows admin)
.cursor/rules/
  fixed-assets-project.mdc
  never-delete-erpnext-modules.mdc
```

---

## 14. After changing PC

1. Clone/open repo: `d:\GitHub_m-islam-ciplc\erpnext` (branch `asset-dev`)  
2. Start Docker + bench (commands in §3)  
3. Read this file + `ASSETS_ONLY_MODE.md`  
4. Hard refresh browser; login **http://127.0.0.1:8000**  
5. Continue with **Asset Category** creation if not done  

**Cursor rules** in `.cursor/rules/` should load automatically so the AI keeps the **never delete code** rule.

---

*End of handoff.*

# SmartStock — Progress Log

Record our project progress which show what we done till now

---

**Done**
# Session 19
- Built Purchase Order detail screen (procurement.ts API client, PO detail page)
# Session 18
- Added ABC classification API endpoint (POST /api/planning/abc-runs/run/)
- Built Items list frontend screen: fetches items, triggers ABC classification,
  displays SKU/name/class/reorder point/safety stock in a table
# Session 17
- Built JWT auth flow: AuthContext, Login page, ProtectedRoute
- Built live Dashboard: fetches real items/locations, calls check_reorder()
  live via API for each item, renders explainable reason text
# Session 16
- Built accounts API (Role, User, Permission, RolePermission)
- Built audit API (AuditTrail)
- Backend (models + services + tests + API) is functionally complete
# Session 15
- Built DRF API layer for inventory, procurement, production, planning
  (following the master_data pattern: serializers.py -> views.py -> urls.py
  -> registered in config/urls.py)
# Session 14
- Installed djangorestframework-simplejwt for JWT authentication
- Built master_data API: serializers, viewsets (ModelViewSet), router-based urls
# Session 13
- Wrote pytest tests for procurement (QC pass/fail gating), planning (reorder
  explainability + forecast calculation), production (reservation vs issue,
  full chain to FG receipt)
- Full suite: pytest -v -> 8 passed in 1.98s
# Session 12
- Installed pytest, pytest-django
- Wrote first automated test: test_stock_balance_is_derived_not_stored (inventory app)
- Test passing: 1 passed in 2.87s
# Session 11
- Created audit app: AuditTrail model (generic entity_type/entity_id reference,
  same polymorphic pattern as StockLedger.ref_doc_id)
- Uses settings.AUTH_USER_MODEL / get_user_model() - correct Django pattern
  for referencing the custom User model, avoids hard circular dependency
- Verified via shell: created one AuditTrail entry linked to real superuser
# Session 10
- Created planning app: ForecastRun, ReorderRecommendation, ABCClassificationRun,
  SupplierKPI, SupplierRiskScore models
- Wrote moving_average_forecast() - simple, transparent forecasting (no black-box AI)
# Session 09
- Created production app: BOMHeader, BOMLine, WorkOrder, MaterialReservation,
  MaterialIssue, FGReceipt models (single-level BOM by design)
- Wrote issue_material() and receive_finished_goods() services
# Session 08
- Created procurement app: PurchaseOrder, POLine, GoodsReceipt, GRLine, QCHold models
- QCHold uses OneToOneField to GRLine
- Full end-to-end shell test with passed and failed condition
# Session 07
- Created inventory app: StockLocation, StockLedger, StockAdjustment models
- All ledger/adjustment FKs use PROTECT (never lose audit history via cascade delete)
- Wrote get_current_stock() service function - balance derived via Sum(), never stored
- Fixed data loss bug: earlier admin panel entries never actually saved (see error log)
# Session 06
- Created master_data app: ItemCategory, Item, Supplier, ItemSupplier models
- makemigrations + migrate successful
- Registered in admin.py, created test rows via admin panel, confirmed FK dropdowns work
# Session 05
- Created accounts app: Role, User, Permission, RolePermission models
- makemigrations + migrate successful, superuser created
- Registered models in admin.py, confirmed all 4 models visible/working at /admin/
- Milestone: full RBAC foundation proven end-to-end
# Session 04
- Created smartstock database and smartstock_user
- Resolved password mismatch between .env and actual DB user password
- python manage.py migrate succeeded — full toolchain proven end-to-end
# Session 03
- Set up Python venv and install Django
- Created Django project skeleton
- manage.py check passes cleanly
# Session 02
- git init, created .gitignore (Python/Node/OS/IDE patterns)
- First commit: skeleton
- Created GitHub repo, connected via git remote add origin
- Pushed successfully — main branch live on GitHub
# Session 01
- Created monorepo skeleton (backend/, frontend/, docs/)
- Fixed folder naming (SmarStock -> smartstock)
- Set up progress log and error log

**Next:**
build out remaining screens (Items list, PO detail, Work Order detail)
if time permits, then shift focus to dissertation writing
**Notes:**
- Repo: https://github.com/arun95tech/SmartStock 
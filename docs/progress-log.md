# SmartStock — Progress Log

Record our project progress which show what we done till now

---

**Done**
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
- audit app (AuditTrail)
**Notes:**
- Repo: https://github.com/arun95tech/SmartStock 
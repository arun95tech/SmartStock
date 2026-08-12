# SmartStock — Error Log

Enter per error which encountered during work.

---

## Error log form
**Date:**
**Context:** (what you were doing)
**Error:** (exact message/behaviour)
**Cause:**
**Fix:**

---
**Context:** Testing issue_material() service in Django shell
**Error:** NameError: name 'MaterialIssue' is not defined, raised inside services.py
**Cause:** services.py used MaterialIssue.objects.create() but never imported MaterialIssue from .models
**Fix:** Added "from .models import MaterialIssue" to the top of services.py; had to restart the shell session since the already-imported broken version stayed in memory
**Time lost:** ~5 min
**Lesson:** a NameError inside a service function means check that file's own imports first, not the caller; also, editing a .py file does not affect an already-running shell session - always restart the shell after changing code it imports


**Context:** Setting up .env.example template file
**Error:** A real generated SECRET_KEY was accidentally written into .env.example (the committed template file) instead of a placeholder
**Cause:** Copy-paste mix-up between the real .env and the example template
**Fix:** Caught before any git commit and restored placeholder text in .env.example
**Time lost:** ~10 min
**Lesson:** never type or paste real secrets into  any file meant to be committed; verify git status/git log before every commit involving credential files

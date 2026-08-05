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

**Context:** Setting up .env.example template file
**Error:** A real generated SECRET_KEY was accidentally written into .env.example (the committed template file) instead of a placeholder
**Cause:** Copy-paste mix-up between the real .env and the example template
**Fix:** Caught before any git commit and restored placeholder text in .env.example
**Time lost:** ~10 min
**Lesson:** never type or paste real secrets into  any file meant to be committed; verify git status/git log before every commit involving credential files
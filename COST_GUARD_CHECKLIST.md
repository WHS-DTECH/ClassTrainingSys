# Cost Guard Checklist (Monthly)

Purpose: prevent surprise Neon public network transfer charges and catch regressions early.

## Monthly Billing Review (10-15 min)

- [ ] Open Neon Console -> Organization -> Billing.
- [ ] Record current month totals for:
  - Compute (CU-hours)
  - Storage (root branches)
  - Public network transfer (GB)
- [ ] Compare with last month and note percentage change.
- [ ] If Public network transfer is above 70 GB before month-end, investigate immediately.

## Weekly Quick Check (5 min)

- [ ] Open Neon Console -> Organization -> Projects and review Network transfer trend.
- [ ] Identify top project(s) with growth spikes.
- [ ] Confirm no unexpected export/download activity.

## App Safety Checks

- [ ] Confirm debug is OFF in production (`FLASK_DEBUG` not set to `1`).
- [ ] Confirm DB export is disabled in production (`ENABLE_DB_EXPORT` not set to `1`).
- [ ] Confirm heavy list/search pages still have limits and pagination enabled.
- [ ] Confirm lesson navigation/list routes do not fetch full content unless needed.

## Before Releasing Features

- [ ] Any new list endpoint has pagination (`limit`, `page`, `per_page`).
- [ ] Any new search endpoint has max result caps.
- [ ] No `SELECT *` style payloads returned to UI unless required.
- [ ] Large blobs/files are not served from DB rows if object storage/static files can be used.

## Alerts and Thresholds

- [ ] Set a personal alert reminder if monthly transfer exceeds:
  - 50 GB (watch)
  - 80 GB (action now)
  - 100 GB (over included Launch allowance)
- [ ] Track transfer overage estimate:
  - Overage GB = max(0, transfer - 100)
  - Cost estimate = Overage GB x $0.10

## Incident Playbook (If transfer spikes)

- [ ] Check recent deploys/feature flags.
- [ ] Check for accidental export/backup routes.
- [ ] Check high-traffic pages returning large payloads.
- [ ] Check repeated refresh/poll behavior in frontend.
- [ ] Temporarily reduce payload size and add stricter limits.

## Monthly Log

Use this table each month:

| Month | Compute (CUh) | Storage (GB-mo) | Transfer (GB) | Estimated Overage ($) | Notes |
|---|---:|---:|---:|---:|---|
| YYYY-MM |  |  |  |  |  |
| YYYY-MM |  |  |  |  |  |
| YYYY-MM |  |  |  |  |  |

## Repository-specific Notes

- This repo now includes route/query optimizations and admin pagination to reduce unnecessary transfer.
- Keep these protections during refactors:
  - capped search result sets
  - bounded history queries
  - paginated admin user/student views
  - restricted DB export route access

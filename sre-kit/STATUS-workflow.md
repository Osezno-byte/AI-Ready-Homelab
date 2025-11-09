# STATUS.md Workflow Guide

**Purpose**: Maintain a living snapshot of your infrastructure health
**Frequency**: Update daily (quick) or weekly (detailed)
**Time Required**: 5-10 minutes per update

---

## ✅ Template Structure

```markdown
# STATUS (Daily/Weekly)

## 🟢 Operational Summary
- Overall State:
- High-risk services:
- Changes since last status:

## 🔧 Recent Fixes (48 hours)
- [ID] Description

## 🚨 Issues (Open)
- [ID] Issue name
  - Severity:
  - Next action:
  - Owner:
  - Verification date:

## ⏳ Pending Verification
- [ID] Fix name
  - Waiting until:
  - Evidence needed:

## ✅ Completed (Verified)
- [ID] Fix name
  - Verification notes:
```

---

## ✅ How to Use It

### Step 1: Daily Quick Update (2 minutes)

**What to check**:
- Any new errors in logs?
- Any services down?
- Any performance degradation?

**What to update**:
- Add new issues to "🚨 Issues (Open)"
- Move fixed items to "⏳ Pending Verification"
- Update "Overall State" if needed

### Step 2: Weekly Detailed Review (10 minutes)

**What to check**:
- All pending verification items (have they been stable?)
- All open issues (any progress?)
- Resource usage trends
- Backup status

**What to update**:
- Move verified items to "✅ Completed"
- Archive completed items older than 30 days
- Update "High-risk services" list
- Document "Changes since last status"

---

## ✅ Best Practices

### Issue ID Format

Use sequential IDs for tracking:
- `ISSUE-001`, `ISSUE-002`, etc.
- Makes it easy to reference in commits, runbooks, incidents

### Severity Levels

- **CRITICAL**: Service down, data loss risk, security breach
- **HIGH**: Degraded performance, user impact, backup failure
- **MEDIUM**: Minor issues, tech debt, cosmetic problems
- **LOW**: Nice-to-have improvements, documentation gaps

### Verification Windows

**Rule**: Don't mark something "completed" until it's proven stable

**Typical windows**:
- Service restarts: 24 hours
- Configuration changes: 48 hours
- Major updates: 1 week
- DR changes: After next successful drill

### When to Update

**Daily update triggers**:
- Morning: Quick health check
- After any change: Document it
- When something breaks: Add to issues

**Weekly update triggers**:
- Sunday evening: Full review
- Before major changes: Baseline state
- After incidents: Lessons learned

---

## ✅ Example: Real STATUS.md Entry

```markdown
# STATUS (2025-11-08)

## 🟢 Operational Summary
- Overall State: HEALTHY (no critical issues)
- High-risk services: Home Assistant (recent automation changes)
- Changes since last status: Upgraded HA to 2025.11.2, added bedroom automation

## 🔧 Recent Fixes (48 hours)
- [ISSUE-042] Fixed Frigate camera disconnections (go2rtc implementation)
- [ISSUE-041] Resolved HA database bloat (recorder optimization)

## 🚨 Issues (Open)
- [ISSUE-043] Pi-hole occasionally slow to respond
  - Severity: LOW
  - Next action: Monitor for 48h, check DNS query logs
  - Owner: Bear
  - Verification date: 2025-11-10

## ⏳ Pending Verification
- [ISSUE-042] Frigate camera stability (waiting until 2025-11-09)
  - Evidence needed: Zero disconnections for 48 hours
- [ISSUE-041] HA database size remains stable (waiting until 2025-11-15)
  - Evidence needed: No growth beyond 85MB for 1 week

## ✅ Completed (Verified)
- [ISSUE-040] n8n workflows failing (verified stable 2025-11-06)
  - Verification notes: 72 hours with zero failures, logs clean
```

---

## ✅ Integration with Other Tools

### With PENDING-WORK.md

**STATUS.md** = Operational health (what's broken now?)
**PENDING-WORK.md** = Strategic projects (what are we building?)

**When to move from STATUS → PENDING-WORK**:
- Issue requires multi-step fix
- Issue is actually tech debt
- Issue is project-worthy (e.g., "Implement ZFS snapshots")

### With Incident Reports

**When incident occurs**:
1. Add to STATUS.md immediately (🚨 Issues)
2. Create detailed incident report (separate file)
3. Link incident report in STATUS.md
4. Move through verification pipeline

### With Runbooks

**When creating runbook**:
1. Document procedure
2. Test procedure
3. Add "Last tested" date to STATUS.md
4. Reference runbook in issue fixes

---

## ✅ Safety Practices

### Mode Change Checklist

When switching between local-only, hybrid, and cloud-enhanced modes:

1. **Document the change** in STATUS.md with rationale
2. **Verify CSE policy** matches the new mode requirements
3. **Test redaction** if moving to hybrid/cloud-enhanced
4. **Validate rollback** procedure before enabling cloud components
5. **Record the mode** in git commit message

### Preflight Sanitize (Hybrid / Cloud-enhanced)

- Before any cloud planning, POST logs/configs to `tools/n8n/preflight_sanitize` and use only the `sanitized` output.
- Never persist raw inputs in n8n.
- Record the sanitize action in STATUS with a link to the evidence (hash/size only).

**Example usage**:
```bash
# Send diagnostics for sanitization
curl -X POST http://localhost:5678/webhook/sanitize \
  -H "Content-Type: application/json" \
  -d '{"logs": "$(cat error.log)", "config": "$(cat service.yml)"}' \
  > sanitized-output.json

# Use only the sanitized field for cloud planning
jq '.sanitized' sanitized-output.json > cloud-input.txt
```

**Redaction coverage**:
- Bearer tokens and API keys
- Passwords and secrets (key-value pairs)
- Environment variables (SECRET, TOKEN, KEY suffixes)
- Email addresses
- External IPv4 addresses (preserves RFC1918 private IPs)
- MAC addresses
- URL query parameters (token, key, sig, auth)
- GPS coordinates
- Home addresses

---

## ✅ Common Mistakes to Avoid

### Mistake 1: Marking Things "Completed" Too Soon

**Wrong**: Fixed service, marked completed immediately
**Right**: Fixed service, moved to "Pending Verification", monitored for 48h

### Mistake 2: Not Documenting Small Fixes

**Wrong**: Fixed minor issue, didn't document
**Right**: Documented in "Recent Fixes" even if small (helps with debugging later)

### Mistake 3: Letting STATUS.md Get Stale

**Wrong**: Only update when something breaks
**Right**: Weekly cadence even when nothing is broken

### Mistake 4: Too Much Detail

**Wrong**: Entire troubleshooting log in STATUS.md
**Right**: Summary in STATUS.md, details in incident report

---

## ✅ Automation Opportunities

### Check for Stale Pending Items

```bash
# Add to weekly automation
grep "Pending Verification" STATUS.md | while read line; do
  # Extract verification date
  # Alert if > 7 days old
done
```

### Generate Health Summary

```bash
# Count open issues
OPEN=$(grep -c "🚨 Issues" STATUS.md)

# Count pending verification
PENDING=$(grep -c "⏳ Pending" STATUS.md)

# Send to monitoring system
echo "Open issues: $OPEN, Pending: $PENDING"
```

### Archive Completed Items

```bash
# Move completed items older than 30 days to archive
# Keep STATUS.md focused on recent activity
```

---

## ✅ Metrics to Track (Optional)

### Operational Metrics

- **Mean Time Between Failures (MTBF)**: Days between issues
- **Mean Time To Recovery (MTTR)**: Hours to fix
- **Verification Success Rate**: % that stay fixed
- **Issue Backlog**: Open + pending count

### Reliability Score

```
Reliability Score = (Days Uptime / Days Monitored) × 100

Target: 99%+ for critical services
Acceptable: 95%+ for non-critical
```

---

## ✅ Next Steps

1. **Copy template** to your homelab directory
2. **Do first weekly update** (even if everything is working)
3. **Set calendar reminder** for weekly reviews
4. **Integrate with git commits** (reference STATUS.md in commit messages)

---

**See also**:
- [`samples/STATUS.sample.md`](../samples/STATUS.sample.md) - Complete template with examples
- [`incident-template.md`](incident-template.md) - For major incidents
- [`dr-test-matrix.md`](dr-test-matrix.md) - For disaster recovery testing

# INCIDENT REPORT TEMPLATE

**Last Updated**: 2025-11-09 | **Version**: 1.0.0

**Incident ID**: INC-YYYY-MM-DD-NNN
**Date**: YYYY-MM-DD
**Severity**: CRITICAL | HIGH | MEDIUM | LOW
**Status**: INVESTIGATING | MITIGATED | RESOLVED | CLOSED

---

## ✅ Summary

**What happened?** (One sentence)

Brief description of the incident.

---

## ✅ Impact

### Services Affected
- Service name (impact level)
- Service name (impact level)

### User Impact
- What functionality was degraded or unavailable?
- How many users affected? (For homelab: just you, or family members?)

### Duration
- **Started**: YYYY-MM-DD HH:MM TZ
- **Detected**: YYYY-MM-DD HH:MM TZ
- **Mitigated**: YYYY-MM-DD HH:MM TZ
- **Resolved**: YYYY-MM-DD HH:MM TZ
- **Total Downtime**: X hours Y minutes

---

## ✅ Detection

**How was it discovered?**
- [ ] Automated monitoring alert
- [ ] User report
- [ ] Manual observation
- [ ] Scheduled check
- [ ] Other: ___________

**Alert/Log Evidence**:
```
Paste relevant logs or alerts here
```

---

## ✅ Timeline

| Time | Event |
|------|-------|
| HH:MM | Incident began (service X started failing) |
| HH:MM | Alert triggered / First detection |
| HH:MM | Investigation started |
| HH:MM | Root cause identified |
| HH:MM | Mitigation applied |
| HH:MM | Service restored |
| HH:MM | Monitoring resumed |
| HH:MM | Incident closed |

---

## ✅ Root Cause

### What Caused It?

Detailed explanation of the root cause.

**Contributing Factors**:
- Factor 1
- Factor 2
- Factor 3

### Why Wasn't It Caught Earlier?

- Monitoring gap?
- Configuration drift?
- Undocumented dependency?
- Testing gap?

---

## ✅ Resolution

### Immediate Fix (What stopped the bleeding?)

Steps taken to restore service:

1. Step 1
2. Step 2
3. Step 3

### Permanent Fix (What prevents recurrence?)

Steps taken to prevent this from happening again:

1. Step 1
2. Step 2
3. Step 3

---

## ✅ Lessons Learned

### What Went Well?
- Detection was fast
- Response was coordinated
- Communication was clear
- etc.

### What Could Be Improved?
- Monitoring could be better
- Documentation was outdated
- Backup process wasn't tested
- etc.

---

## ✅ Action Items

| ID | Action | Owner | Due Date | Status |
|----|--------|-------|----------|--------|
| AI-001 | Update monitoring to catch X | Bear | YYYY-MM-DD | OPEN |
| AI-002 | Document Y in runbook | Bear | YYYY-MM-DD | OPEN |
| AI-003 | Test backup procedure Z | Bear | YYYY-MM-DD | OPEN |

---

## ✅ Verification

**How will we know this is fixed?**

- [ ] Service has been stable for 48 hours
- [ ] Monitoring confirms no recurrence
- [ ] Runbook updated and tested
- [ ] DR drill includes this scenario
- [ ] ACTION-ITEMS completed

**Verification Date**: YYYY-MM-DD (when all criteria met)

---

## ✅ Related Documents

- **STATUS.md**: [ISSUE-XXX] Link to tracking issue
- **Runbook**: Link to relevant runbook
- **PENDING-WORK.md**: [ID-XXXX] Follow-up project (if needed)
- **Logs**: Path to preserved logs

---

## ✅ Template Usage Notes

### When to Create an Incident Report

**Always**:
- Service completely unavailable
- Data loss or corruption
- Security breach
- Extended degradation (> 1 hour)

**Optional**:
- Minor transient issues (< 5 min downtime)
- Known issues with existing tickets
- Scheduled maintenance that went wrong

### Severity Definitions

**CRITICAL**:
- Complete service outage
- Data loss risk
- Security breach
- Affects critical infrastructure

**HIGH**:
- Significant degradation
- Multiple services affected
- User-facing impact
- Requires immediate attention

**MEDIUM**:
- Single service degraded
- Workaround available
- Limited user impact
- Can wait for business hours

**LOW**:
- Minor issues
- No user impact
- Cosmetic problems
- Low priority fixes

### Timeline Best Practices

**Use absolute times** (not relative):
- Good: "2025-11-08 14:30 EST"
- Bad: "30 minutes ago"

**Include timezone**: Always specify TZ
**Be precise**: Minute-level accuracy is fine
**Note gaps**: If there's a delay in detection, note why

### Root Cause Analysis

**Ask "Why?" 5 Times**:

1. Why did service X fail?
   - Because dependency Y was down

2. Why was dependency Y down?
   - Because configuration Z was wrong

3. Why was configuration Z wrong?
   - Because update process didn't validate

4. Why didn't update process validate?
   - Because runbook wasn't followed

5. Why wasn't runbook followed?
   - Because runbook was outdated

**Root cause**: Runbook maintenance process broken

### Action Item Tracking

**Make them SMART**:
- **Specific**: "Update Frigate runbook with go2rtc validation steps"
- **Measurable**: Can check if done
- **Assignable**: Clear owner
- **Realistic**: Can actually be completed
- **Time-bound**: Has a due date

**Track completion** in PENDING-WORK.md if multi-step

---

## ✅ Example: Real Incident Report

```markdown
# INCIDENT REPORT

**Incident ID**: INC-2025-11-05-001
**Date**: 2025-11-05
**Severity**: HIGH
**Status**: RESOLVED

---

## Summary

Frigate NVR camera disconnections caused 6 detection failures per day, degrading security monitoring.

---

## Impact

### Services Affected
- Frigate NVR (6 disconnections/day across 2 cameras)
- Home Assistant camera monitoring (degraded)

### User Impact
- Security monitoring unreliable
- False motion alerts when cameras reconnected
- Manual intervention required 6x/day

### Duration
- **Started**: 2025-10-20 (approximately - gradual onset)
- **Detected**: 2025-11-01 (via log review)
- **Mitigated**: 2025-11-05 14:30 EST
- **Resolved**: 2025-11-05 15:00 EST
- **Total Downtime**: Intermittent (15 days of degradation)

---

## Detection

**How discovered**: Manual log review during unrelated troubleshooting

**Log Evidence**:
```
[2025-11-05 10:23:41] frigate.error: Front_Yard lost connection
[2025-11-05 10:24:15] frigate.info: Front_Yard reconnected
```

---

## Root Cause

**What caused it**: Direct RTSP streams from cameras were unstable over network

**Contributing factors**:
- Cameras lack keepalive mechanism
- Network congestion during peak hours
- No monitoring for camera health
- Default Frigate RTSP configuration not optimized

---

## Resolution

### Immediate Fix

1. Implemented go2rtc as RTSP relay
2. Updated Frigate config to use go2rtc endpoints
3. Restarted Frigate service
4. Monitored for 48 hours

### Permanent Fix

1. Documented go2rtc architecture in runbook
2. Added camera health monitoring to STATUS.md
3. Created verification window (48h stability required)

---

## Lessons Learned

### What Went Well
- Detection happened before critical failure
- Fix was straightforward once root cause identified
- go2rtc solution was more reliable than expected

### What Could Be Improved
- Should have had camera health monitoring from day 1
- Frigate logs weren't being reviewed regularly
- No runbook existed for camera troubleshooting

---

## Action Items

| ID | Action | Owner | Due Date | Status |
|----|--------|-------|----------|--------|
| AI-001 | Add Frigate camera health check to weekly STATUS review | Bear | 2025-11-08 | ✅ DONE |
| AI-002 | Create "Frigate Camera Troubleshooting" runbook | Bear | 2025-11-10 | 🔄 IN PROGRESS |
| AI-003 | Set up automated alert for > 2 disconnections/day | Bear | 2025-11-15 | ⏳ PENDING |

---

## Verification

**Criteria**:
- [x] Service stable for 48 hours (verified 2025-11-07)
- [x] Zero disconnections observed
- [x] Monitoring confirms stability
- [ ] Runbook completed and tested (in progress)
- [ ] Automated alerting configured (pending)

**Verification Date**: 2025-11-07 (service stability verified, follow-up work pending)

---

## Related Documents

- **STATUS.md**: [ISSUE-042]
- **Runbook**: docs/runbooks/frigate-camera-troubleshooting.md (in progress)
- **PENDING-WORK.md**: [ID-1105] Complete Frigate monitoring improvements
```

---

**See also**:
- [`STATUS-workflow.md`](STATUS-workflow.md) - Daily/weekly health tracking
- [`dr-test-matrix.md`](dr-test-matrix.md) - Disaster recovery testing
- [`samples/STATUS.sample.md`](../samples/STATUS.sample.md) - Service health template

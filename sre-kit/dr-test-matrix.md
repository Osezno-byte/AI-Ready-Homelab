# DR TEST MATRIX

**Last Updated**: 2025-11-09 | **Version**: 1.0.0

**Purpose**: Validate disaster recovery procedures quarterly
**Frequency**: Every 3 months (Q1, Q2, Q3, Q4)
**Time Required**: 2-4 hours per quarter

---

## ✅ Why DR Testing Matters

**Untested backups = No backups**

Common failures:
- Backups exist but can't be restored
- Restore procedure is undocumented
- Dependencies weren't backed up
- Restoration takes too long
- Data corruption wasn't detected

**DR testing proves**:
- Backups actually work
- You know how to restore
- RTO/RPO are achievable
- Documentation is accurate

---

## ✅ Test Scenarios

### 1. Proxmox Node Failure

**Scenario**: Proxmox host completely fails (hardware death, corruption, etc.)

**Prerequisites**:
- [ ] Proxmox backups exist
- [ ] Backup location is accessible
- [ ] Restore procedure is documented

**Test Procedure**:
1. Identify a non-critical VM to test (e.g., test-vm-101)
2. Take snapshot/backup of VM
3. Delete VM completely
4. Restore VM from backup
5. Verify VM boots and functions correctly
6. Document time taken for each step

**Expected Outcome**:
- VM restored successfully
- All data intact
- Services function normally
- RTO: < 30 minutes for single VM

**Actual Outcome** (Fill in after test):
- Start time: ___________
- End time: ___________
- Issues encountered: ___________
- RTO achieved: ___________

**Pass/Fail**: ⬜ PASS | ⬜ FAIL

**Notes**:

---

### 2. Docker Stack Corruption

**Scenario**: Docker installation corrupted, need to rebuild all containers

**Prerequisites**:
- [ ] docker-compose.yml files backed up
- [ ] .env files backed up (but secrets redacted in git)
- [ ] Volume data backed up
- [ ] Image list documented

**Test Procedure**:
1. Select a non-critical service (e.g., uptime-kuma)
2. Stop service: `docker-compose down`
3. Delete volumes (CAREFUL - test service only)
4. Restore docker-compose.yml from backup
5. Restore .env file from backup
6. Restore volume data from backup
7. `docker-compose up -d`
8. Verify service functions correctly

**Expected Outcome**:
- Service restored successfully
- Configuration intact
- Data intact
- RTO: < 15 minutes for single service

**Actual Outcome**:
- Start time: ___________
- End time: ___________
- Issues encountered: ___________
- RTO achieved: ___________

**Pass/Fail**: ⬜ PASS | ⬜ FAIL

**Notes**:

---

### 3. Home Assistant Database Corruption

**Scenario**: HA database corrupted, need to restore from backup

**Prerequisites**:
- [ ] HA backup exists
- [ ] Backup is recent (< 24 hours)
- [ ] Restore procedure is documented
- [ ] Automations are in git/backed up separately

**Test Procedure**:
1. **Do NOT test in production** - Use test instance or snapshot first
2. Create snapshot of current HA VM
3. Access HA backup interface
4. Select backup to restore
5. Perform restoration
6. Verify HA boots correctly
7. Verify automations work
8. Verify history data is present
9. Document time taken

**Expected Outcome**:
- HA restored successfully
- Automations functional
- History data present (up to backup time)
- RTO: < 10 minutes

**Actual Outcome**:
- Start time: ___________
- End time: ___________
- Data loss: ___________ (time between backup and test)
- RTO achieved: ___________

**Pass/Fail**: ⬜ PASS | ⬜ FAIL

**Notes**:

---

### 4. Network Configuration Loss

**Scenario**: pfSense configuration lost, need to rebuild from documentation

**Prerequisites**:
- [ ] pfSense config.xml backed up
- [ ] VLAN config documented
- [ ] Firewall rules documented
- [ ] VPN config documented

**Test Procedure**:
1. **EXTREME CAUTION** - This can break network access
2. Export current pfSense config (backup)
3. Review documentation vs actual config
4. Identify any undocumented rules/settings
5. Update documentation BEFORE testing restoration

**Expected Outcome**:
- Documentation matches reality
- All critical rules documented
- VPN config documented
- RTO: < 1 hour to rebuild from docs

**Actual Outcome**:
- Documentation gaps found: ___________
- Undocumented rules: ___________
- Documentation updated: ⬜ YES | ⬜ NO

**Pass/Fail**: ⬜ PASS | ⬜ FAIL

**Notes**:

---

### 5. Full Backup Restoration Test

**Scenario**: Complete infrastructure loss, rebuild from backups

**Prerequisites**:
- [ ] Proxmox backup server accessible
- [ ] All VM backups documented
- [ ] Restoration priority list exists
- [ ] Network config documented

**Test Procedure**:
1. Document current state (all VMs, services, configs)
2. **Plan restoration order**:
   - Priority 1: pfSense (network)
   - Priority 2: Proxmox management
   - Priority 3: Critical services (HA, Frigate)
   - Priority 4: Supporting services (n8n, Uptime Kuma)
   - Priority 5: Optional services
3. Restore one VM from each priority tier (in test environment)
4. Verify each restoration
5. Document total time for complete rebuild

**Expected Outcome**:
- All priority 1-3 services restorable
- Documentation accurate
- RTO: < 4 hours for critical services
- RPO: < 24 hours (data loss acceptable)

**Actual Outcome**:
- Priority 1 RTO: ___________
- Priority 2 RTO: ___________
- Priority 3 RTO: ___________
- Total RTO: ___________
- Issues encountered: ___________

**Pass/Fail**: ⬜ PASS | ⬜ FAIL

**Notes**:

---

### 6. Configuration Drift Detection

**Scenario**: Infrastructure has drifted from documented state, detect gaps

**Prerequisites**:
- [ ] Infrastructure documented (network.mmd, services.mmd)
- [ ] Service configs in git
- [ ] Baseline snapshot exists

**Test Procedure**:
1. Compare current pfSense config to documented firewall rules
2. Compare docker-compose files to git repo
3. Compare HA automations to git repo
4. Identify any undocumented changes
5. Update documentation OR revert drift

**Expected Outcome**:
- < 5% drift from documented state
- All drift identified and documented
- Critical drift reverted

**Actual Outcome**:
- Undocumented firewall rules: ___________
- Undocumented Docker changes: ___________
- Undocumented HA automations: ___________
- Drift percentage: ___________%

**Pass/Fail**: ⬜ PASS | ⬜ FAIL

**Notes**:

---

## ✅ Quarterly Test Plan

### Q1 (January-March)
- [ ] Test 1: Proxmox Node Failure
- [ ] Test 3: Home Assistant Database Corruption
- [ ] Test 6: Configuration Drift Detection

### Q2 (April-June)
- [ ] Test 2: Docker Stack Corruption
- [ ] Test 4: Network Configuration Loss
- [ ] Test 6: Configuration Drift Detection

### Q3 (July-September)
- [ ] Test 1: Proxmox Node Failure
- [ ] Test 5: Full Backup Restoration Test
- [ ] Test 6: Configuration Drift Detection

### Q4 (October-December)
- [ ] Test 2: Docker Stack Corruption
- [ ] Test 3: Home Assistant Database Corruption
- [ ] Test 6: Configuration Drift Detection

**Note**: Test 6 (Configuration Drift) should run EVERY quarter

---

## ✅ RTO/RPO Targets

### Recovery Time Objective (RTO)

**How fast can you restore service?**

| Service | Priority | Target RTO | Actual RTO | Status |
|---------|----------|-----------|------------|--------|
| pfSense (Network) | CRITICAL | 15 min | ___ | ⬜ |
| Home Assistant | CRITICAL | 30 min | ___ | ⬜ |
| Frigate NVR | HIGH | 1 hour | ___ | ⬜ |
| Docker services | MEDIUM | 2 hours | ___ | ⬜ |
| n8n workflows | MEDIUM | 2 hours | ___ | ⬜ |
| Uptime Kuma | LOW | 4 hours | ___ | ⬜ |

### Recovery Point Objective (RPO)

**How much data loss is acceptable?**

| Service | Priority | Target RPO | Actual RPO | Status |
|---------|----------|-----------|------------|--------|
| Home Assistant | CRITICAL | 24 hours | ___ | ⬜ |
| Frigate recordings | HIGH | 48 hours | ___ | ⬜ |
| n8n workflows | MEDIUM | 1 week | ___ | ⬜ |
| Configuration files | CRITICAL | 0 (in git) | ___ | ⬜ |

---

## ✅ Test Results Summary

### Latest Test: YYYY-MM-DD

**Tests Passed**: __ / 6
**Tests Failed**: __ / 6
**Average RTO**: ___ minutes
**Critical Issues Found**: ___

**Action Items**:
- [ ] Issue 1: ___________
- [ ] Issue 2: ___________
- [ ] Issue 3: ___________

---

## ✅ Best Practices

### Before Testing

1. **Announce the test** (if affects production)
2. **Have rollback plan ready**
3. **Document current state** (baseline)
4. **Set timer** (measure RTO accurately)
5. **Have monitoring open** (watch for side effects)

### During Testing

1. **Take notes** (timestamp everything)
2. **Document issues immediately**
3. **Don't skip steps** (validates runbook accuracy)
4. **Measure time** (RTO is critical metric)
5. **Check dependencies** (does restore break other services?)

### After Testing

1. **Update STATUS.md** (test results)
2. **Update runbooks** (if procedure changed)
3. **Fix issues found** (add to PENDING-WORK.md)
4. **Update RTO/RPO metrics**
5. **Schedule next test** (quarterly cadence)

---

## ✅ Common Failure Modes

### Backup Exists But Can't Restore

**Symptoms**: Backup file present, but restoration fails

**Causes**:
- Wrong backup format
- Missing dependencies
- Encryption keys lost
- Incompatible versions

**Fix**: Test restoration quarterly, document procedure

### Restoration Takes Too Long

**Symptoms**: RTO target missed (e.g., 2 hours instead of 30 min)

**Causes**:
- Slow network
- Large backup size
- Manual steps not documented
- Missing automation

**Fix**: Optimize backup size, automate restoration, document faster procedure

### Data Loss Exceeds RPO

**Symptoms**: Restored data is older than expected

**Causes**:
- Backup frequency too low
- Backup schedule not running
- Backup job failing silently

**Fix**: Increase backup frequency, add monitoring for backup success

### Undocumented Dependencies

**Symptoms**: Service restores but doesn't work (missing dependencies)

**Causes**:
- Database not backed up
- Secrets not documented
- Network config not included
- External dependencies not noted

**Fix**: Document ALL dependencies, include in backup procedure

---

## ✅ Integration with STATUS.md

After each DR test, update STATUS.md:

```markdown
## ✅ Completed (Verified)
- [DR-Q1-2025] Quarterly DR testing completed (2025-03-15)
  - Verification notes:
    - Test 1 (Proxmox): PASS (RTO 22 min, under 30 min target)
    - Test 3 (HA DB): PASS (RTO 8 min, under 10 min target)
    - Test 6 (Drift): FAIL (12% drift found, updated docs)
  - Action items:
    - [AI-012] Fix configuration drift (added to PENDING-WORK.md)
    - [AI-013] Update Proxmox restore runbook (documented faster procedure)
```

---

## ✅ Next Steps

1. **Schedule Q1 test** in calendar (first week of each quarter)
2. **Assign owner** for each test
3. **Document baseline** (current RTO/RPO for each service)
4. **Run first test** and update this matrix
5. **Create action items** for any failures

---

**See also**:
- [`STATUS-workflow.md`](STATUS-workflow.md) - Daily/weekly health tracking
- [`incident-template.md`](incident-template.md) - For major incidents
- [`../docs/reliability/backup-restore-template.md`](../docs/reliability/backup-restore-template.md) - Backup procedures (coming soon)

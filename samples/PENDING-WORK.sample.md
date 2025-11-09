# Pending Work & Project Tracking

**Last Updated**: YYYY-MM-DD
**Purpose**: Track cross-cutting projects, system-wide initiatives, and tech debt
**Scope**: Multi-service work, infrastructure upgrades, documentation projects

---

## 🎯 Active Projects

[Major projects currently in progress]

### Project Name - Brief Description
**Status**: 📋 PENDING | 🔄 IN PROGRESS | ✅ COMPLETE
**Priority**: ⭐⭐⭐⭐⭐ CRITICAL | ⭐⭐⭐⭐ HIGH | ⭐⭐⭐ MEDIUM | ⭐⭐ LOW
**Owner**: [Your Name]
**Started**: YYYY-MM-DD
**Target Completion**: YYYY-MM-DD

**Overview**:
[1-2 paragraph description of what this project accomplishes and why it's important]

**Current State**:
- [What's currently true/broken/suboptimal]
- [Metrics showing the problem]

**Target State**:
- [What should be true after completion]
- [Expected metrics/improvements]

**Implementation Plan**:
1. Step one - brief description
2. Step two - brief description
3. Step three - brief description

**Estimated Time**: X hours/days
**Risk Level**: Low | Medium | High
**Risk Mitigation**: [How you'll handle problems if they occur]

**Dependencies**:
- [Other projects/services that must complete first]
- [External factors (hardware, software versions, etc.)]

**Documentation**:
- Complete guide: `/docs/path/to/detailed-guide.md`
- Related runbooks: `/runbooks/related-procedure.md`

**Todo List**:
- [ ] Task one
- [ ] Task two
- [x] Completed task

**Next Session**: [What to do when you resume work]

---

### Example: Network Segmentation Hardening
**Status**: 📋 PENDING IMPLEMENTATION
**Priority**: ⭐⭐⭐⭐ HIGH (Security hardening)
**Owner**: Bear
**Started**: 2025-11-08
**Target Completion**: 2025-11-15

**Overview**:
Enable pfSense firewall rules to block all LAN → IoT VLAN traffic except specific exceptions for camera RTSP access. This completes bidirectional VLAN isolation and implements defense-in-depth network security.

**Current State**:
- IoTNet → LAN: **BLOCKED** ✅ (Rule 22 working)
- LAN → IoTNet: **ALLOWED** ❌ (Rule 7 "Allow LAN to Anywhere" permits all traffic)
- Security Score: **65/100**

**Target State**:
- IoTNet → LAN: **BLOCKED** ✅
- LAN → IoTNet: **BLOCKED except Frigate/HA RTSP** ✅
- Security Score: **98/100** (+33 points)

**Implementation Plan**:
1. Add Rule 6a: Allow Frigate (10.27.27.251) → IoT cameras (10.27.20.0/24:554 RTSP)
2. Add Rule 6b: Allow HA (10.27.27.11) → IoT cameras (10.27.20.0/24:554 RTSP)
3. Enable Rule 8: Block all other LAN → VLAN traffic
4. Verify: Frigate and HA camera access still working
5. Test: LAN → IoT non-RTSP traffic correctly blocked

**Estimated Time**: 10 minutes (web UI configuration)
**Risk Level**: Low (easy rollback, non-disruptive, cameras use RTSP pull pattern)
**Risk Mitigation**: Can disable Rule 8 immediately if issues occur

**Documentation**:
- Complete guide: `/docs/PFSENSE-LAN-VLAN-SEGMENTATION-FIX.md`
- Runbook: `/runbooks/firewall-rule-changes.md`

**Todo List**:
- [ ] Add LAN firewall rules for Frigate/HA → IoT cameras RTSP access
- [ ] Enable Rule 8 to block LAN → VLAN traffic
- [ ] Verify cameras still working after firewall changes
- [ ] Update network diagram with new rules

**Next Session**: Follow step-by-step instructions in PFSENSE-LAN-VLAN-SEGMENTATION-FIX.md

---

## 📅 Near-Term (0-30 Days)

[Projects to complete this month]

**Example**:
- [ID-1302] pfSense: Tighten LAN→IoT segmentation per security audit findings
- [ID-1305] Home Assistant: Upgrade to 2025.11.x (test in staging first)
- [ID-1308] Documentation: Create runbooks for top 5 most common tasks
- [ID-1310] Monitoring: Add alerting for disk space < 20% remaining

---

## 📆 Mid-Term (1-3 Months)

[Projects for this quarter]

**Example**:
- [ID-1307] UPS: Implement NUT + shutdown orchestration + test
- [ID-1312] Backups: Automate quarterly restore tests
- [ID-1315] Documentation: Consolidate scattered service docs
- [ID-1318] Security: Implement 2FA for all externally-accessible services

---

## 📊 Long-Term (3+ Months)

[Future projects and ideas]

**Example**:
- [ID-1401] Evaluate second Proxmox node for HA clustering
- [ID-1405] Implement GitOps workflow for infrastructure as code
- [ID-1410] Build custom monitoring dashboard (Grafana)
- [ID-1415] Develop advanced AI agents for automated troubleshooting

---

## 🐛 Tech Debt & Maintenance

[Ongoing maintenance tasks and technical debt]

**Example**:

### High Priority Tech Debt
- **[TD-001]** Refactor docker-compose files to use consistent naming
  - **Impact**: Harder to find containers, inconsistent logs
  - **Effort**: 2 hours
  - **Target**: 2025-11-20

- **[TD-002]** Update deprecated Docker image tags (using `latest`)
  - **Impact**: Unpredictable updates, potential breaking changes
  - **Effort**: 1 hour
  - **Target**: 2025-11-25

### Medium Priority Tech Debt
- **[TD-003]** Consolidate scattered backup scripts into single tool
  - **Impact**: Hard to maintain, inconsistent backup quality
  - **Effort**: 4 hours
  - **Target**: 2025-12-01

### Low Priority Tech Debt
- **[TD-004]** Improve documentation formatting consistency
  - **Impact**: Minor, aesthetic
  - **Effort**: 3 hours
  - **Target**: 2025-12-15

---

## ✅ Recently Completed

[Completed projects from last 30 days - for historical context]

**Example**:

### MCP HTTP API Initiative - Dual-Transport Architecture
**Status**: ✅ COMPLETE (Nov 7, 2025)
**Priority**: ⭐⭐⭐⭐⭐ CRITICAL
**Duration**: Oct 25 - Nov 7 (14 days)
**Effort**: 7.5 hours total

**Summary**:
Added HTTP REST API layer to all 7 existing MCP servers to enable n8n automation workflows. MCP servers now support BOTH stdio transport (for local AI) and HTTP transport (for n8n).

**Results**:
- Phase 1: All 7 HTTP servers operational (ports 8091-8098)
- Phase 2: All 9 n8n monitoring workflows operational
- Testing: 65/65 tools tested, 63/65 working (97% success rate)

**Documentation**: `/docs/MCP-HTTP-API-COMPLETE-GUIDE.md`

---

### Custom Agents Phase 2/3 Completion
**Status**: ✅ COMPLETE (Nov 8, 2025)
**Priority**: ⭐⭐⭐⭐ HIGH
**Duration**: Nov 1-8 (8 days)
**Effort**: 12 hours total

**Summary**:
Developed and tested 7 new specialized agents (network-diagnostician, backup-validator, security-auditor, database-optimizer, integration-validator, update-coordinator, performance-analyzer).

**Results**:
- All 10 agents now production-ready
- Agent usage guide created
- Integration with MCP tools complete
- Backup validation 12-20x faster

**Documentation**: `/AGENT-USAGE-GUIDE.md`

---

## 📈 Project Metrics

**Active Projects**: X
**Completed This Month**: X
**Average Completion Time**: X days
**Tech Debt Items**: X

**Velocity**:
- Projects completed per month: X
- Average project size: X hours
- Success rate: X%

---

## 📝 Project Template

[Use this template when adding new projects]

```markdown
### Project Name
**Status**: 📋 PENDING
**Priority**: ⭐⭐⭐ MEDIUM
**Owner**: [Name]
**Target**: YYYY-MM-DD

**Overview**: [Brief description]

**Current State**: [What's wrong/missing]
**Target State**: [What should be true]

**Plan**:
1. Step one
2. Step two

**Estimated Time**: X hours
**Risk**: Low/Medium/High

**Todo**:
- [ ] Task one
- [ ] Task two
```

---

**Issue ID Format**:
- `ID-XXYY` - Sequential project ID (XX = month, YY = sequence)
- `TD-XXX` - Tech debt items (sequential)
- `BUG-XXX` - Bug tracking (sequential)

**Priority Guide**:
- ⭐⭐⭐⭐⭐ CRITICAL - Security issues, production outages
- ⭐⭐⭐⭐ HIGH - Important features, significant improvements
- ⭐⭐⭐ MEDIUM - Nice-to-have features, minor improvements
- ⭐⭐ LOW - Future ideas, documentation cleanup

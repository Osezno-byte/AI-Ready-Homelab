# Service Name - Current Status

**Last Updated**: YYYY-MM-DD HH:MM TZ
**Overall Health**: 🟢 OPERATIONAL | 🟡 MONITORING | 🔴 URGENT
**Next Review**: YYYY-MM-DD (brief reason)

---

## 🚨 URGENT - Action Required

[List critical issues needing immediate attention]

**Example**:
### Production Service Failing - 2025-11-08
- **Status**: 🚨 URGENT (service down since 14:30)
- **Issue**: Container restart loop due to configuration error
- **Impact**: Users cannot access service
- **Owner**: [Your Name]
- **Next Update**: 2025-11-08 16:00
- **Details**: See incident report `incident-2025-11-08-service-failure.md`

---

## ⏳ MONITORING - Awaiting Verification

[List changes deployed that need time-based verification]

**Example**:
### Database Optimization Deployed - 2025-11-05
- **Status**: ⏳ Awaiting Verification (deployed Nov 5, 2025)
- **Change**: Enabled automatic VACUUM and ANALYZE on database
- **Expected Result**: Database size reduction, faster queries
- **Testing**: Monitor database size and query performance
- **Verification Date**: 2025-11-12 (7 days of data)
- **Backup**: `database-backup-pre-optimization-20251105.sql`

### Network Segmentation Changes - 2025-11-03
- **Status**: ⏳ Awaiting Verification (deployed Nov 3, 2025)
- **Change**: Tightened firewall rules for IoT VLAN
- **Expected Result**: IoT devices cannot access LAN network
- **Testing**: Verify IoT devices still function, test cross-VLAN blocking
- **Verification Date**: 2025-11-10 (7 days testing)
- **Rollback Plan**: pfSense config backup `pfsense-config-20251103.xml`

---

## 🔧 RECENT FIXES - Last 30 Days

[List verified fixes from the last month - moves here from MONITORING after verification]

**Example**:
### Container Restart Issue Resolved - 2025-10-28
- **Status**: ✅ Complete and Verified (Nov 2, 2025)
- **Deployed**: 2025-10-28
- **Issue**: Service container restarting every 5 minutes
- **Root Cause**: Health check timeout too aggressive (5s, should be 30s)
- **Solution**: Updated docker-compose.yml health check interval
- **Result**: Container stable, zero restarts in 5 days
- **Monitoring Period**: Oct 28 - Nov 2 (5 days stable)
- **Backup**: `docker-compose.yml.backup-20251028`

### Backup Validation Failure Fixed - 2025-10-25
- **Status**: ✅ Verified Working (Oct 27, 2025)
- **Issue**: Nightly backups not running (cron job misconfigured)
- **Solution**: Fixed cron syntax error in `/etc/cron.d/backup-script`
- **Result**: Backups running successfully every night at 02:00
- **Monitoring Period**: Oct 25-27 (3 consecutive successful backups)
- **Verification**: Manual restore test passed

### Security Hardening - SSH Key-Only Auth - 2025-10-20
- **Status**: ✅ Completed and Verified (Oct 21, 2025)
- **Issue**: SSH accepting password authentication (brute force vulnerability)
- **Security Risk**: Exposed to password-guessing attacks
- **Previous Config**: `PasswordAuthentication yes` in `/etc/ssh/sshd_config`
- **Fixed Config**: `PasswordAuthentication no` (key-only authentication enforced)
- **Result**: SSH now requires Ed25519 key authentication only
- **Verification**: Tested SSH access with keys, confirmed password login disabled
- **Monitoring Period**: None required (immediate security hardening)

---

## 🟢 OPERATIONAL - Working Well

[List stable, well-functioning components]

**Example**:

### Core Services
- **Container Orchestration**: Docker Compose running 12 services (all healthy)
- **Reverse Proxy**: Nginx Proxy Manager handling SSL termination and routing
- **Monitoring**: Uptime Kuma tracking 8 services (all green)
- **Notifications**: Signal messenger delivering alerts successfully

### Network Infrastructure
- **pfSense Router**: Stable, handling firewall rules and VLAN segmentation
- **VLAN Segmentation**: 4 VLANs (LAN, HomeNet, IoT, Guest) properly isolated
- **DNS**: Pi-hole providing ad-blocking and local DNS resolution
- **VPN**: WireGuard providing remote access (3 active peers)

### Backup & Recovery
- **Automated Backups**: Nightly backups running successfully
- **Retention Policy**: 7 daily, 4 weekly, 12 monthly backups maintained
- **Last Restore Test**: 2025-10-15 (successful full restore in 45 minutes)
- **Off-site Backups**: Syncing to external location daily

---

## ℹ️ KNOWN NON-ISSUES - Expected Behavior

[Document things that LOOK like problems but are actually normal]

**Example**:

### Low Frigate Detection FPS (0.0-0.2 FPS)
- **What it looks like**: Frigate detection appears "off" or broken
- **What's actually happening**: Detection is motion-triggered and idle
- **Expected behavior**: Detection runs at 5 FPS when motion/objects present, 0.0-0.2 FPS when idle
- **Configuration**: person, dog, cat tracking enabled on all cameras
- **Why this is normal**: Motion-triggered detection conserves CPU/TPU resources
- **How to verify**: Check Frigate logs for detection events when motion occurs

### Docker Container "Unhealthy" Status on Startup
- **What it looks like**: Container shows as unhealthy for 30-60 seconds after restart
- **What's actually happening**: Application startup takes longer than first health check
- **Expected behavior**: Health check fails initially, then passes after service fully starts
- **Configuration**: Health check interval: 30s, retries: 3, start period: 60s
- **Why this is normal**: Large applications (databases, media servers) need time to initialize
- **How to verify**: Wait 60-90 seconds, container should become healthy

### High Database Write I/O During Optimization
- **What it looks like**: Database showing high disk writes (100+ MB/s)
- **What's actually happening**: Scheduled VACUUM/ANALYZE operation running
- **Expected behavior**: Weekly database maintenance causes temporary I/O spike
- **Configuration**: VACUUM runs every Sunday at 03:00
- **Why this is normal**: VACUUM rewrites database file to reclaim space
- **How to verify**: Check if operation occurs only during maintenance window

---

## 🔍 QUICK DIAGNOSTICS

[Essential commands for checking service health]

**Example**:

### Container Health
```bash
# Check all containers
docker ps -a

# Check specific container logs
docker logs <container-name> --tail 50

# Check container resource usage
docker stats --no-stream
```

### Network Connectivity
```bash
# Test DNS resolution
nslookup google.com

# Check firewall rules (pfSense)
ssh admin@10.27.27.1 "pfctl -sr"

# Verify VLAN connectivity
ping 10.27.20.1  # IoT VLAN gateway
```

### Service Status
```bash
# Check systemd services
systemctl status <service-name>

# Check service logs
journalctl -u <service-name> -n 50

# Check listening ports
netstat -tlnp | grep <port>
```

### Backup Verification
```bash
# List recent backups
ls -lh /path/to/backups/ | tail -10

# Verify backup size (should be > X MB)
du -sh /path/to/backups/latest-backup.tar.gz

# Test backup integrity
tar -tzf /path/to/backups/latest-backup.tar.gz > /dev/null && echo "OK"
```

---

## 📝 NOTES

[Additional context, links to runbooks, dashboards, external resources]

**Example**:

### Related Documentation
- **Runbook**: See `runbooks/service-restart-procedure.md`
- **Architecture**: See `docs/architecture/service-diagram.mmd`
- **DR Plan**: See `docs/reliability/disaster-recovery-plan.md`

### Monitoring Dashboards
- **Uptime Kuma**: http://monitoring.local:3001
- **Grafana**: http://grafana.local:3000/d/service-dashboard
- **Logs**: http://logs.local:5601 (Kibana)

### Known Issues & Workarounds
- **Issue #123**: Service occasionally fails health check under high load
  - **Workaround**: Increase health check timeout to 60s
  - **Permanent Fix**: Under investigation (CPU bottleneck suspected)

### Upcoming Maintenance
- **2025-11-15**: Scheduled OS updates (requires reboot)
- **2025-11-20**: SSL certificate renewal
- **2025-11-25**: Quarterly backup restore test

---

**Status Emojis Guide**:
- 🚨 URGENT - Immediate action required
- ⏳ MONITORING - Awaiting verification
- 🔧 RECENT FIXES - Completed in last 30 days
- 🟢 OPERATIONAL - Working well
- ℹ️ KNOWN NON-ISSUES - Expected behavior
- 🔍 QUICK DIAGNOSTICS - Health check commands

# Incident Classification: Noise vs Real — Karan Systems Pvt. Ltd.

**Classification:** Internal | IT Operations Use Only  
**Purpose:** Helps IT Support triage incoming alerts to distinguish transient noise (auto-resolving, low impact) from real incidents requiring manual investigation or escalation.

---

## Section 1: Noise Incidents

> Noise incidents are transient, self-healing events. They require no ticket, no escalation, and no manual fix. Log for trend awareness only.

---

### Microsoft 365 Temporary Login Failure

A brief Microsoft 365 service hiccup causes login errors for a small group of users. The issue resolves automatically within minutes with no data loss or access impact.

**Category:** Noise | **Resolution:** Auto-resolved | **Action:** None

---

### VPN Reconnect Drop (ISP / Cisco ASA Maintenance)

Short VPN disconnections occur during an upstream ISP maintenance window or a scheduled Cisco ASA firmware update. Clients automatically reconnect once the maintenance window closes.

**Category:** Noise | **Resolution:** Auto-resolved | **Action:** None

---

### Slow SharePoint / OneDrive Load Times

Microsoft cloud capacity events in a region temporarily slow file access and page loads for SharePoint or OneDrive. Performance self-recovers as Microsoft redistributes load.

**Category:** Noise | **Resolution:** Auto-resolved | **Action:** None

---

### Email Delivery Delay (Microsoft Exchange Queue)

Outbound emails are held briefly in the Microsoft Exchange Online transport queue during a backend service update. All emails are eventually delivered with a short delay.

**Category:** Noise | **Resolution:** Auto-resolved | **Action:** None

---

### DNS Resolution Hiccup (Automated Cache Flush)

The internal intranet portal becomes briefly unreachable due to an automated DNS cache flush on the primary server. The secondary DNS server takes over automatically within minutes.

**Category:** Noise | **Resolution:** Auto-resolved | **Action:** None

---

### Antivirus Signature / Engine Update Spike

Scheduled antivirus signature and engine updates cause a temporary CPU spike across Windows endpoints. The system normalises once the update download and baseline scan complete.

**Category:** Noise | **Resolution:** Auto-resolved | **Action:** None

---

### Automated Backup Job Performance Impact

A scheduled deep-archive backup job running during business hours causes slight file server latency for affected departments. Performance returns to normal once the job completes.

**Category:** Noise | **Resolution:** Auto-resolved | **Action:** None

---

### Microsoft Teams Call Quality Dip

Temporary audio or video degradation occurs during a Microsoft Teams backend service update. Quality self-recovers with no user action once the update completes.

**Category:** Noise | **Resolution:** Auto-resolved | **Action:** None

---

### Printer Queue Stuck After Spooler Restart

Print jobs pile up after a silent Windows Print Spooler service restart triggered by a background update. The queue auto-clears once the spooler service recovers.

**Category:** Noise | **Resolution:** Auto-resolved | **Action:** None

---

### Azure AD Token Refresh Latency

Apps briefly prompt users to re-login due to delayed token refresh during a backend Azure AD maintenance event. Signing back in resolves the issue immediately.

**Category:** Noise | **Resolution:** Auto-resolved | **Action:** None

---

## Section 2: Real Incidents

> Real incidents require manual investigation, root cause analysis (RCA), and/or escalation. They do not auto-resolve and may have compliance, security, or business continuity implications.

---

### Premature Access Removal (SailPoint Offboarding Bug)

An active employee loses group memberships and system access before their last working day due to an early SailPoint offboarding trigger. Requires IAM team investigation, access restoration, and trigger logic correction.

**Category:** Real | **Priority:** P2 | **Escalate To:** IAM Team | **RCA Required:** Yes

---

### Account Lockout — Stale Mobile Credentials

A user is locked out after updating their password on a laptop but not on their enrolled mobile device. Stale credentials cause repeated failed authentication attempts triggering a lockout. Requires helpdesk unlock and credential sync guidance.

**Category:** Real | **Priority:** P3 | **Escalate To:** Helpdesk | **RCA Required:** No

---

### Unauthorized PII Access — HR Salary Records

A non-HR employee gains read access to confidential salary records due to an incorrectly approved SailPoint access certification. Requires immediate access revocation, HR notification, and a Segregation of Duties (SoD) policy review.

**Category:** Real | **Priority:** P1 | **Escalate To:** IT Security + CISO | **RCA Required:** Yes

---

### Phishing Email — Credential Harvesting Attempt

Employees receive a spoofed email from a fake internal domain asking them to re-enter VPN credentials via a malicious link. Requires domain block, company-wide alert, investigation into whether credentials were compromised, and mandatory password resets.

**Category:** Real | **Priority:** P1 | **Escalate To:** IT Security | **RCA Required:** Yes

---

### Rogue Device Detected on Secure VLAN

An unknown MAC address obtains an IP on the secure VLAN, traced to an employee who connected an unauthorized personal wireless router. Requires NAC port isolation, physical device confiscation, and a management warning to the employee.

**Category:** Real | **Priority:** P2 | **Escalate To:** Network Security | **RCA Required:** Yes

---

### Corrupted Database Table Post-Migration

An application begins throwing 500 errors immediately after a change-window schema update, caused by incomplete data mapping in the migration scripts. Requires DBA-led rollback to a pre-migration snapshot and a full RCA of the migration process.

**Category:** Real | **Priority:** P1 | **Escalate To:** Database Reliability Team | **RCA Required:** Yes

---

### MFA Bypass Due to Misconfigured Conditional Access Policy

Users connecting from specific IP ranges bypass Multi-Factor Authentication due to an incorrect rule in the Azure AD Conditional Access policy. Requires policy correction, forced session sign-out for affected users, and an audit of recent logins from those IP ranges.

**Category:** Real | **Priority:** P1 | **Escalate To:** IAM / Security Team | **RCA Required:** Yes

---

### Ransomware Indicator Detected on Endpoint

The EDR platform flags unusual mass file encryption activity on an employee workstation. Requires immediate network isolation of the device, forensic disk imaging, threat hunting across the environment, and incident response activation.

**Category:** Real | **Priority:** P1 | **Escalate To:** IT Security + CISO | **RCA Required:** Yes

---

### Privilege Escalation via Orphaned Admin Account

A long-dormant privileged admin account is reactivated and used to access sensitive systems without authorisation. Requires immediate account disable, full access audit trail review, and an investigation into how and by whom the account was triggered.

**Category:** Real | **Priority:** P1 | **Escalate To:** IT Security + CISO | **RCA Required:** Yes

---

### Data Exfiltration Alert — Large Outbound File Transfer

The DLP platform flags an unusually large outbound file transfer to a personal cloud storage domain (e.g., personal Google Drive or Dropbox). Requires user interview, transfer content review, legal team notification if sensitive data is confirmed, and policy enforcement.

**Category:** Real | **Priority:** P1 | **Escalate To:** IT Security + Legal | **RCA Required:** Yes

---

## Quick Triage Reference

| Signal | Classification |
|---|---|
| Issue auto-resolved in under 15 minutes | Noise |
| Issue is affecting a specific user or account | Real — Investigate |
| SailPoint or Active Directory change detected in logs | Real — Always investigate |
| PII, financial, or sensitive data is involved | Real — P1, escalate immediately |
| Broad cloud service slowdown with no data exposure | Noise |
| Unusual authentication pattern or MFA bypass | Real — Investigate |
| Scheduled maintenance window activity | Noise |
| Unknown device or process on network | Real — Investigate |

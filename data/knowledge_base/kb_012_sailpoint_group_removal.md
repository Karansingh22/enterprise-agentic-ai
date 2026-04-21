# KB Article 012 — SailPoint Group Removal Guide
**Organization:** Karan Systems Pvt. Ltd.
**Department:** IT Support / Identity & Access Management (IAM)
**Version:** 2.3
**Last Updated:** April 2026
**Access Level:** All Employees, IT Administrators, HR

---

## 1. Overview

Removing group memberships is just as important as granting them. This article explains the various scenarios in which group memberships are removed from an employee's identity in **SailPoint IdentityNow**, how to request a removal, how to handle emergency removals, and how to investigate and recover from incorrect removals — such as accidental offboarding triggers or access revoked during certifications.

---

## 2. Reasons for Group Membership Removal

| Reason                              | Trigger                                    | Who Initiates             |
|-------------------------------------|--------------------------------------------|---------------------------|
| Employee no longer needs access     | Role change, project completion            | Employee or Manager       |
| Access Certification (quarterly)    | Automated SailPoint campaign               | Manager (certify/revoke)  |
| Employee Offboarding                | HRMS termination trigger                   | Automated (HR → SailPoint)|
| Security Incident Investigation     | Suspected policy violation / data breach   | IT Security               |
| Compliance Remediation              | Audit finding (SoD violation, over-privileged) | IAM/Compliance Team    |
| Contractor/Vendor Contract End      | Contract end date in SailPoint             | Automated                 |
| Manager-Directed Removal            | Business decision                          | Manager                   |

---

## 3. How to Remove Group Membership via SailPoint

### 3.1 Self-Initiated Removal (Employee)

1. Log in to `identity.karansystems.in`.
2. Navigate to **"My Access"** tab.
3. Find the group or entitlement you want to remove (use the search/filter).
4. Click on the group name to expand details.
5. Click **"Request Removal"** (button on the right side).
6. In the dialog box:
   - Confirm the item to be removed.
   - Add a **Reason** (optional but recommended): e.g., *"Project completed. No longer need access to DEV_SERVER_ADMIN group."*
7. Click **Submit**.
8. For non-sensitive groups: Removal is **processed immediately** (no approval needed).
9. For sensitive/privileged groups: Manager approval may be required before removal.

> 📌 Self-initiated removals are automatically logged in SailPoint for audit purposes.

### 3.2 Manager-Initiated Removal

1. SailPoint Dashboard → **"Manage My Team"** (top navigation).
2. Search and select the employee.
3. Navigate to **"Access"** tab on the employee's profile.
4. Find the group to be removed.
5. Click **"Revoke Access"** → Add justification → Confirm.
6. SailPoint processes the revocation and notifies the employee via email.

### 3.3 Bulk Removal (Multiple Employees or Multiple Groups)

For bulk operations (e.g., project ending — remove all project group access for 10 employees):

1. Raise a ticket at `helpdesk.karansystems.in` → Access Management → Bulk Revocation Request.
2. Attach a spreadsheet with columns: Employee ID | Group Name | Reason.
3. IAM team processes bulk removals within **2 business days**.
4. Confirmation report sent after completion.

---

## 4. Automated Group Removal — How It Works

### 4.1 Offboarding-Triggered Removal

When an employee's termination is confirmed in HRMS:

1. **HRMS** sends an offboarding event to **SailPoint** via real-time integration.
2. SailPoint's **Lifecycle Manager** triggers the **"Leaver"** lifecycle event.
3. All SailPoint entitlements (groups, roles, app access) are **queued for revocation**.
4. Active Directory groups are removed via the **AD Provisioning Connector**.
5. Revocation is completed within **2 hours** of the trigger event.
6. A **Provisioning Summary Report** is auto-generated and emailed to the IAM team and HR.

> **Known Issue / Risk:** If the offboarding trigger fires prematurely (e.g., incorrect last working day set in HRMS), it can cause access loss before the actual departure date. See Section 7 for recovery steps.

### 4.2 Access Certification-Triggered Removal

During quarterly certifications:
- Managers receive a SailPoint certification task.
- Any access item marked **"Revoke"** by the manager is queued for removal.
- Removals are executed **48 hours after the manager's certification submission** (grace period for corrections).
- Post-certification, a revocation report is available in SailPoint → Reports → Certification Results.

### 4.3 Automated SoD (Separation of Duties) Violation Removal

SailPoint enforces **SoD policies**. If a new access request creates a conflict:
- Example: A user cannot have both `SAP_PAYMENT_APPROVER` and `SAP_PAYMENT_CREATOR` (financial control).
- SailPoint will:
  1. Block the new access request (if automatic prevention is enabled).
  2. Or flag the conflict and notify the IAM team for manual review.
  3. The conflicting access item is revoked after IAM confirmation.

---

## 5. Emergency Group Removal (Security Incident)

In cases where immediate group removal is required:

**Scenario:** Employee Adam Fox suspected of unauthorized access to Finance data.

**Process:**
1. IT Security or HR contacts the **IAM On-Call Team** at `iam-oncall@karansystems.in` or calls the security hotline: **Ext. 2911**.
2. IAM verifies the request with the IT Security Team (verbal + email confirmation).
3. IAM admin logs in to SailPoint → **Administrator View** → **Identities** → Search employee.
4. Under **Entitlements**: Select all groups flagged for removal → **Revoke**.
5. Simultaneously, IT Security can **disable the AD account** directly in Active Directory.
6. Revocation is completed within **30 minutes**.
7. A **Security Access Removal Log** is created and attached to the security incident ticket.

---

## 6. What Happens After Group Removal

When a group is removed via SailPoint:

| System              | Action                                           | Sync Time      |
|---------------------|--------------------------------------------------|----------------|
| SailPoint           | Entitlement removed from identity profile        | Immediate      |
| Active Directory    | User removed from AD security group              | 5–15 minutes   |
| Application (SSO)   | Session invalidated / access denied on next login| 15–30 minutes  |
| Email/Distribution  | Removed from distribution list                   | 30–60 minutes  |
| VPN                 | VPN group membership revoked (if applicable)     | 15 minutes     |

> **Important:** Active sessions may not be immediately invalidated. For security-critical removals, the IT Security team can also force a **session invalidation** in Azure AD (Microsoft Entra).

---

## 7. Recovering from Incorrect Group Removal

### Scenario: Access Removed by Mistake (Before Departure / Incorrect Offboarding)

**Reference: Incident INC001 — Adam Fox | FINANCE_APP_USERS Removed Prematurely**

**Step-by-Step Recovery:**

1. **Identify the issue:**
   - Employee reports access denied to Finance App.
   - IT checks SailPoint → **Identities → Adam Fox → Access → Activity**.
   - Activity log shows: `2026-04-14 10:00 — FINANCE_APP_USERS Removed (Trigger: Offboarding Lifecycle Event)`.

2. **Verify the error:**
   - Check HRMS: Confirm Adam Fox's last working day is **not today**.
   - Confirm with HR: Was the offboarding trigger set incorrectly? (e.g., wrong last day entered).

3. **Restore access via SailPoint Admin:**
   - SailPoint Admin Console → **Identities → Adam Fox → Provisioning → Re-provision Role**.
   - Or: Navigate to the AD group `FINANCE_APP_USERS` → Members → Add Adam Fox.
   - In SailPoint: Manually add entitlement back under the identity.

4. **Verify restoration:**
   - AD: `Get-ADGroupMember -Identity FINANCE_APP_USERS` confirms Adam Fox is in the group.
   - Employee tests application access.

5. **Fix root cause:**
   - Correct the last working day in HRMS.
   - Submit a change request to the SailPoint integration team to review the offboarding trigger logic.

6. **Document:**
   - Close the incident ticket with root cause: *"HRMS incorrect last working day triggered premature offboarding."*
   - Add to post-incident review log.

### SLA for Access Restoration

| Priority | Scenario                            | SLA          |
|----------|-------------------------------------|--------------|
| P1       | Incorrect termination (active employee) | 2 hours  |
| P2       | Premature access removal (before last day) | 4 hours |
| P3       | Accidental certification revocation | Next business day |

---

## 8. SailPoint Group Removal Audit Reports

SailPoint maintains a complete audit trail of all group removals. IAM Admins and Compliance teams can generate reports:

1. SailPoint Admin → **Reports** → **Activity Reports**.
2. Select **"Provisioning Transactions"** report.
3. Filter by:
   - **Operation:** Revoke
   - **Date Range:** Specify period
   - **Identity:** Specific employee (optional)
   - **Source:** Active Directory (for AD groups)
4. Export as CSV or PDF.

**Key columns in the report:**
- `Identity Name` — Who lost access
- `Account` — Which system account
- `Entitlement` — Which group/role was removed
- `Operation` — Revoke/Deprovision
- `Requestor` — Who triggered the removal (system or person)
- `Status` — Success / Failed
- `Timestamp` — Date and time of removal

---

## 9. Related Articles

- KB Article 003 — Access Request Process
- KB Article 008 — Group Membership Request
- KB Article 011 — SailPoint Access Request
- KB Article 010 — Offboarding Process
- Incident Cases: INC001 — Adam Fox Access Removal

---

*IAM Team: `iam@karansystems.in` | IAM On-Call (Security Incidents): Ext. 2911 | Portal: `identity.karansystems.in`*

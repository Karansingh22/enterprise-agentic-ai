# KB Article 007 — Manager Change Process
**Organization:** Karan Systems Pvt. Ltd.
**Department:** Human Resources / IT Operations
**Version:** 1.3
**Last Updated:** April 2026
**Access Level:** All Employees, HR, IT Administrators

---

## 1. Overview

A Manager Change in Karan Systems refers to updating the official reporting relationship of an employee in the HRMS, Active Directory, and all connected enterprise systems. This change is triggered by organizational restructuring, internal transfers, role changes, or management departures. Accurate manager data is critical because it drives approval workflows for leave, access requests, expense approvals, and performance reviews.

---

## 2. When Is a Manager Change Required?

- An employee moves to a new team or department (internal transfer).
- A manager resigns, retires, or is terminated.
- Organizational restructuring / reorg.
- A new manager joins and takes over a team.
- An employee is promoted and their direct reports are realigned.
- Correction of an incorrect manager assignment after onboarding.

---

## 3. Who Can Initiate a Manager Change?

| Initiator              | Scenario                                              |
|------------------------|-------------------------------------------------------|
| HR Business Partner    | Org restructuring, lateral moves, manager departure   |
| Current Manager        | Team reallocation within the same department          |
| New Manager            | Confirm absorption of new direct reports              |
| Employee               | Only for correction requests; requires HR approval    |

> **Employees cannot unilaterally change their own manager.** All requests require HR validation.

---

## 4. Manager Change Process — Step by Step

### 4.1 HR-Initiated Manager Change

1. HR Business Partner logs in to **HRMS Portal** at `hrms.karansystems.in`.
2. Navigate to **Employee Directory → Search Employee → Update Reporting Manager**.
3. Enter the new manager's Employee ID or name.
4. Select the effective date.
5. Add a note (e.g., "Reorg Q2 2026 — Team merged under Finance Operations").
6. Submit. The request goes to:
   - **HR Head** for approval.
   - **IT/IAM Team** for Active Directory and SailPoint sync.

### 4.2 Manager-Initiated Change (Same Department)

1. Manager logs in to HRMS → **My Team → Report Reallocation**.
2. Selects the employee to be transferred.
3. Enters the receiving manager's Employee ID.
4. Provides justification (e.g., "Project assignment change").
5. Submits for HR approval.
6. HR approves → HRMS updated → IT systems synced automatically.

### 4.3 Employee-Initiated Correction Request

1. Employee raises a ticket at `helpdesk.karansystems.in` → **HR Services → Manager Update Request**.
2. Provides current incorrect manager name and correct manager name.
3. Ticket routed to HR Business Partner for verification.
4. HR validates and processes the correction within 2 business days.

---

## 5. Systems Updated After Manager Change

A manager change triggers updates across multiple systems via the HRMS-to-AD sync (runs every 4 hours):

| System                    | Update                                          | SLA         |
|---------------------------|-------------------------------------------------|-------------|
| HRMS Portal               | Org chart, reporting line                       | Immediate   |
| Active Directory (AD)     | `manager` attribute on user object              | 4 hours     |
| SailPoint IdentityNow     | Manager in identity profile, approval workflows | 4 hours     |
| Microsoft 365 / Exchange  | Org chart, GAL reporting line                   | 4–8 hours   |
| JIRA / ServiceNow         | Approver mapping for tickets                    | Next sync (24 hrs) |
| Expense Management (SAP)  | Expense approval hierarchy                      | Next business day |
| Performance Management    | Review hierarchy, goal cascading                | Next business day |

> **Note:** If a pending approval (leave, access request) is in the old manager's queue at the time of change, it must be manually reassigned. The employee should notify IT Helpdesk.

---

## 6. Impact on Active Approval Workflows

### 6.1 Leave Approvals

- Pending leave requests in the old manager's queue will **not** be automatically transferred.
- Employees with pending leave approvals should:
  1. Withdraw the leave request.
  2. Resubmit after the manager change is effective (visible in HRMS).

### 6.2 Access Requests in SailPoint

- Pending access requests awaiting the old manager's approval are **put on hold**.
- IT/IAM team will manually reassign them to the new manager's queue within 2 business days.
- Employee may contact `iam@karansystems.in` to expedite reassignment.

### 6.3 Expense Claims

- Expense claims submitted before the manager change are still routed to the **original manager** unless manually escalated.
- For re-routing, contact the Finance team: `finance-ops@karansystems.in`.

---

## 7. Manager Change During Termination/Offboarding

When a manager leaves the organization:

1. HR assigns a temporary acting manager immediately (same business day).
2. All direct reports are mapped to the acting manager within 4 hours.
3. A permanent reallocation is confirmed within **5 business days** post-departure.
4. If the departing manager had pending approvals, IT will reassign them to the acting manager.

See **KB Article 010 — Offboarding Process** for full details on manager offboarding.

---

## 8. Verification

After a manager change is processed, verify accuracy:

1. **HRMS:** Login → My Profile → Reporting Manager (should show new manager).
2. **SailPoint:** `identity.karansystems.in` → My Profile → Manager.
3. **Outlook GAL:** Open Outlook → Search your name → View contact → check "Reports To."
4. **Test Workflow:** Submit a leave request to verify it routes to the new manager.

If discrepancies exist after 24 hours, raise a ticket at `helpdesk.karansystems.in`.

---

## 9. Audit and Compliance

- All manager change transactions are logged in the HRMS audit trail.
- The IT Security team reviews manager change logs quarterly to detect unauthorized modifications.
- Historical manager data is retained for 7 years for compliance purposes.

---

## 10. Related Articles

- KB Article 009 — Onboarding Process
- KB Article 010 — Offboarding Process
- KB Article 008 — Group Membership Request

---

*HR Helpdesk: `hr-helpdesk@karansystems.in` | Ext. 1001 | IT Helpdesk: Ext. 2000*

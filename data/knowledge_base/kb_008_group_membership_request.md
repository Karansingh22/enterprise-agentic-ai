# KB Article 008 — Group Membership Request

**Organization:** Karan Systems Pvt. Ltd.
**Department:** IT Support / Identity & Access Management
**Last Updated:** April 2026
**Access Level:** All Employees

---

## 1. Overview

Groups in Karan Systems serve two primary purposes:

1. **Access Groups** — Grant permissions to applications, shared drives, and systems (e.g., `FINANCE_APP_USERS`, `DEV_GITHUB_WRITE`).
2. **Distribution Lists** — Email groups for communication (e.g., `IT_Alerts_DL`, `AllStaff@karansystems.in`).

Group membership is managed through **Active Directory (AD)** and synchronized to **SailPoint IdentityNow** for governance. This article explains how to request, modify, or remove group memberships.

---

## 2. Types of Groups at Karan Systems

| Group Type               | Naming Convention               | Examples                              |
| ------------------------ | ------------------------------- | ------------------------------------- |
| Application Access Group | `<APP>_<ROLE>`                | `FINANCE_APP_USERS`, `SAP_READ`   |
| Server/Network Access    | `SRV_<NAME>_<ROLE>`           | `SRV_PROD_ADMIN`, `SRV_DB_READ`   |
| Shared Drive Access      | `DRIVE_<NAME>_<ROLE>`         | `DRIVE_HR_DOCS_WRITE`               |
| Distribution List (DL)   | `<DEPT>_DL` or `<TOPIC>_DL` | `FINANCE_DL`, `IT_ALERTS_DL`      |
| Security Group           | `SEC_<PURPOSE>`               | `SEC_VPN_USERS`, `SEC_MFA_EXEMPT` |
| GitHub Team              | Managed separately              | See KB Article 013                    |

---

## 3. Requesting Group Membership

### 3.1 Via SailPoint IdentityNow (Preferred)

1. Log in to `identity.karansystems.in`.
2. Click **"Request Access"** on the dashboard.
3. Search for the group name (e.g., "FINANCE_APP_USERS").
4. Click **"Add to Cart"** → **Checkout**.
5. Provide **Business Justification** (mandatory field):
   - Example: *"Joining the Finance Reporting team as of May 2026. Need access to Finance App to run monthly P&L reports."*
6. Set **Access Duration**:
   - **Permanent** — for role-based access.
   - **Temporary** — specify an end date (for project or contract-based needs).
7. Submit. The request routes to:
   - Your direct manager (for standard groups).
   - Application/Data Owner (for sensitive groups like HR or Finance).
   - IT Security (for privileged/admin groups).

### 3.2 Via IT Helpdesk Portal

1. Go to `helpdesk.karansystems.in` → New Request → Access Management → Group Membership.
2. Fill in:
   - Your Employee ID
   - Group Name (exact name or closest description)
   - Justification
   - Duration
3. Submit and note the ticket number for tracking.

---

## 4. Distribution List Membership

### 4.1 Joining a Distribution List (DL)

- **Team DLs** (e.g., `FINANCE_TEAM_DL`): Managed by HR during onboarding or team change.
- **Project DLs** (e.g., `PROJECT_AURORA_DL`): Request via SailPoint or IT Helpdesk.
- **All-Staff DLs** (e.g., `ALLSTAFF_DL`): Automatic for all active employees.

### 4.2 Creating a New Distribution List

New DLs can be requested for teams of 5 or more with a legitimate business need:

1. Submit request at `helpdesk.karansystems.in` → Access Management → Create Distribution List.
2. Provide:
   - Proposed DL name and email alias (e.g., `project-nova@karansystems.in`)
   - List of initial members (Employee IDs)
   - DL Owner (responsible person for managing membership)
3. IT will provision the DL within **1 business day**.

---

## 5. Approval Workflow for Group Membership

```
Employee submits group request
        ↓
Direct Manager Approval
        ↓ (if data-sensitive group)
Group/Data Owner Approval
        ↓ (if privileged group)
IT Security Review
        ↓
IAM Team provisions AD membership
        ↓
SailPoint propagates to downstream apps
        ↓
Employee receives confirmation email
```

**SLAs:**

- Standard groups: Provisioned within **4 business hours** of full approval.
- Sensitive/privileged groups: Provisioned within **1–2 business days**.

---

## 6. Removing Group Membership

### 6.1 Self-Initiated Removal

If you no longer need access to a group:

1. Log in to SailPoint → **My Access** → Find the group → **Request Removal**.
2. Provide a brief note (e.g., "Project completed; no longer need Finance App access").
3. Removal is processed within 4 hours (no approval needed for self-initiated removals from non-critical groups).

### 6.2 Manager-Initiated Removal

Managers can remove group memberships for their direct reports:

1. SailPoint → **Manage My Team** → Select employee → **Manage Access** → Remove group.
2. Or submit a helpdesk ticket: `helpdesk.karansystems.in` → Access Management → Remove Group Membership.

### 6.3 Automatic Removal via Access Certification

During quarterly **Access Certification** (SailPoint certification campaigns):

- Managers review all group memberships for their team.
- Any membership not certified/approved is automatically revoked.
- Employees are notified 5 days before revocation via email.

---

## 7. Emergency Group Membership Removal

In cases of suspected security incidents (e.g., employee suspected of data exfiltration):

1. **IT Security or HR** contacts the IT Helpdesk directly: Ext. 2000 (Priority 1).
2. Group membership is removed within **30 minutes** by the IAM on-call team.
3. Removal is logged with a security incident ticket reference.
4. The incident is investigated per the Karan Security Incident Response Procedure.

> This is the scenario documented in **Incident INC001 — Incorrect Group Removal** (see incident case files).

---

## 8. Nested Groups and Inherited Access

Some groups are nested within parent groups. Membership in a parent group grants access to all child group resources.

Example:

```
FINANCE_DEPT_GROUP (parent)
  └── FINANCE_APP_USERS (child — app access)
  └── FINANCE_DRIVE_READ (child — shared drive)
  └── FINANCE_REPORTS_WRITE (child — report tool)
```

- Requesting `FINANCE_DEPT_GROUP` grants all nested access.
- Individual child group access can also be requested separately.
- Nested group membership is visible in SailPoint under **My Access → Group Details**.

---

## 9. Group Membership for SailPoint (IIQ / IdentityNow)

For questions about group management within SailPoint itself (role assignments, entitlement management), refer to:

- **KB Article 011 — SailPoint Access Request**
- **KB Article 012 — SailPoint Group Removal**

---

## 10. Related Articles

- KB Article 003 — Access Request Process
- KB Article 011 — SailPoint Access Request
- KB Article 012 — SailPoint Group Removal
- KB Article 013 — GitHub Setup

---

*IAM Team: `iam@karansystems.in` | IT Helpdesk: Ext. 2000 | SailPoint Portal: `identity.karansystems.in`*

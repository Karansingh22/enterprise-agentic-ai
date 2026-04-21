# KB Article 003 — Access Request Process
**Organization:** Karan Systems Pvt. Ltd.
**Department:** IT Support / Identity & Access Management (IAM)
**Version:** 2.4
**Last Updated:** April 2026
**Access Level:** All Employees

---

## 1. Overview

This article describes the end-to-end process for requesting access to Karan Systems applications, shared drives, databases, and internal tools. All access requests are governed by the **Principle of Least Privilege** — employees are granted only the minimum level of access required to perform their job functions.

Access requests are managed through **SailPoint IdentityNow**, the central Identity Governance and Administration (IGA) platform used by Karan Systems.

---

## 2. Types of Access Requests

| Access Type               | Examples                                      | SLA         |
|---------------------------|-----------------------------------------------|-------------|
| Application Access        | Salesforce, JIRA, GitHub, HRMS, SAP           | 1 business day |
| Shared Drive / Folder     | Finance Drive, HR Docs, Project Repos         | 1 business day |
| Group / Distribution List | IT_Alerts, Finance_Team, Managers_DL          | 4 hours     |
| Database Access           | Production DB, Analytics DB, DWH              | 2–3 business days |
| Privileged Access         | Admin access, Root credentials, Server access | 3–5 business days |
| Temporary Access          | Project-based access, Vendor/Contractor       | 1 business day |

---

## 3. How to Submit an Access Request

### 3.1 Via SailPoint IdentityNow (Recommended)

1. Log in to **SailPoint** at `identity.karansystems.in` using your Karan SSO credentials.
2. Click on **"Request Access"** from the dashboard.
3. Search for the application or role using the search bar (e.g., "Salesforce", "GitHub Org Read").
4. Click **"Add to Cart"** for each access item required.
5. In the checkout screen, provide:
   - **Business Justification** (e.g., "Required for Q2 Finance audit project")
   - **Access Duration** (Permanent or Temporary — specify end date for temporary)
6. Click **Submit Request**.
7. The system routes the request to the appropriate approver(s) automatically.

### 3.2 Via IT Helpdesk Portal (Alternative)

If SailPoint is unavailable:
1. Navigate to `helpdesk.karansystems.in`.
2. Click **"New Request" → "Access Management"**.
3. Fill in the Access Request Form with:
   - Employee Name & ID
   - System/Application Name
   - Required Access Level (Read / Write / Admin)
   - Business Justification
   - Manager Name for Approval
4. Submit the form. You will receive a ticket number for tracking.

---

## 4. Approval Workflow

Access requests at Karan Systems follow a **multi-level approval workflow** based on the sensitivity of the access:

```
Employee Submits Request
        ↓
Direct Manager Approval (All requests)
        ↓ (for sensitive/privileged access)
Application/Data Owner Approval
        ↓ (for privileged/admin access)
IT Security Team Approval
        ↓
IT/IAM Team Provisions Access
        ↓
Employee Receives Confirmation Email
```

### 4.1 Approval Notifications

- Approvers receive an email with a direct link to approve or reject.
- Approvers can also manage requests via the SailPoint dashboard.
- If an approver does not act within the SLA window, a reminder is sent automatically.
- After 3 reminders, the request is escalated to the approver's manager.

---

## 5. Access Levels Explained

| Level      | Permissions                                   | Who Can Request                |
|------------|-----------------------------------------------|--------------------------------|
| Read       | View data and files only                      | All employees                  |
| Write      | Create, modify, delete data                   | Employees with business need   |
| Contribute | Push code, upload files, submit forms         | Developers, Analysts           |
| Admin      | Full control, user management in the system   | Team Leads, System Owners only |
| Privileged | Server root, DB superuser, infra admin        | Pre-approved roles only        |

---

## 6. Temporary Access Requests

For project-based or contractor access:

1. Temporary access must have a defined **start date** and **end date**.
2. Access is automatically **revoked** on the end date by SailPoint.
3. Extensions require a new request submitted at least **2 business days** before expiry.
4. All temporary access is logged and reviewed quarterly by the IT Security team.

---

## 7. Access Request for New Joiners

New joiner access is provisioned automatically based on the role defined in the HRMS by HR. Standard access provisioned on Day 1 includes:

- Active Directory account
- Company email (Microsoft 365)
- Karan Intranet access
- HRMS portal access
- Role-based application access (defined by job profile)

Any additional access beyond the standard role profile requires a separate request by the employee or manager.

---

## 8. Bulk Access Requests (Teams / Projects)

For team-wide access provisioning (e.g., a new project team needing access to a set of systems):

1. The Team Lead or Project Manager submits a **Bulk Access Request Form** via SailPoint.
2. Attach a list of employee IDs and required access items.
3. Approval by the Team Lead's Manager and Data/Application Owner is required.
4. Processing time: 2–3 business days depending on the number of users.

---

## 9. Tracking Your Request

- Log in to SailPoint at `identity.karansystems.in` → **My Requests** → View status.
- Status indicators: **Pending Approval**, **In Progress**, **Provisioned**, **Rejected**.
- For helpdesk tickets: `helpdesk.karansystems.in` → **My Tickets**.

---

## 10. Access Review and Certification

Karan Systems conducts **quarterly access reviews (Access Certification)** via SailPoint:
- Managers are asked to certify or revoke access for their direct reports.
- Employees who no longer need access will have it automatically revoked after the certification period.
- Employees should proactively request access removal when no longer needed via `helpdesk.karansystems.in → Revoke Access`.

---

## 11. Related Articles

- KB Article 011 — SailPoint Access Request (Detailed SailPoint Guide)
- KB Article 012 — SailPoint Group Removal
- KB Article 008 — Group Membership Request
- KB Article 010 — Offboarding Process

---

*For questions or escalations, contact the IAM Team at `iam@karansystems.in`.*

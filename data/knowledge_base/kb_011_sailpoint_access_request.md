# KB Article 011 — SailPoint IdentityNow — Access Request Guide
**Organization:** Karan Systems Pvt. Ltd.
**Department:** IT Support / Identity & Access Management (IAM)
**Version:** 4.0
**Last Updated:** April 2026
**Access Level:** All Employees

---

## 1. Overview

**SailPoint IdentityNow** is the Identity Governance and Administration (IGA) platform used at Karan Systems. It is the single source of truth for who has access to what. SailPoint manages:

- Employee identity lifecycle (joiner, mover, leaver)
- Access requests and approvals
- Role-Based Access Control (RBAC)
- Access certifications and reviews
- Password management (self-service)
- Audit and compliance reporting

This article provides a comprehensive guide to submitting, tracking, and managing access requests in SailPoint IdentityNow.

---

## 2. Accessing SailPoint

| Method           | URL / Instructions                                   |
|------------------|------------------------------------------------------|
| Web Browser      | `https://identity.karansystems.in`                     |
| SSO Login        | Use your Karan corporate SSO credentials               |
| Mobile           | SailPoint mobile app (iOS/Android) — search "SailPoint Identity" |
| MFA Required     | Yes — approve Microsoft Authenticator push on login  |

> **First-time login:** You will be prompted to set up 3 security questions. These are used for MFA backup and helpdesk-assisted resets.

---

## 3. SailPoint Dashboard Overview

After logging in, the SailPoint dashboard shows:

| Section                  | Purpose                                                  |
|--------------------------|----------------------------------------------------------|
| **My Access**            | View all your current entitlements, roles, and group memberships |
| **Request Access**       | Submit access requests for yourself or others            |
| **My Requests**          | Track status of submitted requests                       |
| **Pending Actions**      | Items awaiting your approval (for managers/owners)       |
| **My Certifications**    | Access reviews assigned to you                           |
| **Password Management**  | Change password, unlock account, manage MFA              |

---

## 4. How to Request Access for Yourself

### Step 1 — Navigate to Request Access

1. Log in to `identity.karansystems.in`.
2. From the dashboard, click **"Request Access"**.
3. Select **"For Myself"** (default).

### Step 2 — Search for the Access Item

Use the search bar to find the access item. You can search by:
- **Application name** (e.g., "Salesforce", "JIRA", "SAP")
- **Role name** (e.g., "Finance Analyst Role", "GitHub Developer Read")
- **Group name** (e.g., "FINANCE_APP_USERS", "HR_RECORDS_ACCESS")
- **Entitlement name** (e.g., "Production DB Read")

**Tips for searching:**
- Use partial names (e.g., "Finance" returns all Finance-related items).
- Filter by **Source** (Active Directory, Salesforce, GitHub) to narrow results.
- Use the **Recommended** tab to see access items commonly requested by peers in your role.

### Step 3 — Review Access Item Details

Before adding to cart, click the access item to view:
- Description of what access is granted.
- Who currently has this access (count).
- Required approvals.
- Sensitivity classification (General, Sensitive, Privileged).

### Step 4 — Add to Cart and Check Out

1. Click **"Add to Cart"** for each required item.
2. Click the **Cart icon (🛒)** at the top right.
3. Review all items in the cart.
4. For each item, complete:
   - **Business Justification** (required for all requests): Be specific — explain the business need and project context.
   - **Access Duration**: Permanent or Temporary (if temporary, select end date).
5. Click **"Submit Request"**.

### Step 5 — Confirmation

- A request ID is generated (e.g., `REQ-2026-004821`).
- Confirmation email sent to your Karan email.
- Approvers receive notification immediately.

---

## 5. How to Request Access for Someone Else (Delegate Request)

Managers can submit access requests on behalf of their direct reports:

1. SailPoint Dashboard → **"Request Access"** → Switch to **"For Others"** tab.
2. Search and select the employee by name or Employee ID.
3. Follow the same steps as Sections 4.2–4.5 above.
4. Note: The manager's own approval is still required for the request.

---

## 6. SailPoint Access Request Approval Workflow

When you submit a request, SailPoint routes it through a defined approval chain:

```
Request Submitted by Employee
        ↓
Level 1: Direct Manager Approval
        ↓ (for sensitive access)
Level 2: Application Owner / Data Custodian Approval
        ↓ (for privileged access)
Level 3: IT Security Team Approval
        ↓
IAM Provisioning (automated)
        ↓
Employee Notified — Access Active
```

### Approval Timeouts

| Level               | Auto-Reminder Sent  | Escalation (If No Action) |
|---------------------|---------------------|---------------------------|
| Manager Approval    | After 24 hours      | Escalated to skip-level manager after 48 hours |
| App Owner Approval  | After 24 hours      | Escalated to IT Security after 48 hours |
| IT Security Review  | After 24 hours      | Escalated to CISO after 48 hours |

---

## 7. Tracking Your Request

1. SailPoint Dashboard → **"My Requests"** tab.
2. View all requests with their current status:
   - 🟡 **Pending Approval** — Awaiting approver action.
   - 🔵 **In Progress** — Approved; provisioning underway.
   - 🟢 **Provisioned** — Access active.
   - 🔴 **Rejected** — Request denied (reason shown in request details).
   - ⚫ **Cancelled** — Withdrawn by requester.
3. Click any request to see the full approval trail and comments.

---

## 8. Common SailPoint Access Request Scenarios

### 8.1 Requesting Application Access (e.g., Salesforce)

- Search: "Salesforce"
- Items: "Salesforce — Sales User", "Salesforce — Manager"
- Select appropriate role based on your function.
- Justification example: *"Joining the Sales Operations team on May 1. Need Salesforce Sales User access to manage client pipeline."*

### 8.2 Requesting Active Directory Group

- Search the group name: "FINANCE_APP_USERS"
- Source filter: "Active Directory"
- Justification: *"Finance Manager approval obtained. Need access to Finance App for Q2 reporting."*

### 8.3 Requesting Temporary Access (Project-Based)

- Add item to cart → Set duration: **Temporary** → End Date: *Project end date*.
- Access will auto-expire on the set date via SailPoint's lifecycle management.
- Extension requires a new request submitted before expiry.

### 8.4 Requesting Privileged Access (Admin/Root)

- Privileged access items are marked with a 🔐 shield icon.
- Additional requirements:
  - Mandatory justification with project code or manager pre-approval email attached.
  - IT Security review (SLA: 2–3 business days).
  - Access is typically granted for a maximum of 90 days; renewal required thereafter.

---

## 9. Access Certifications in SailPoint

Quarterly, SailPoint runs **Access Certification Campaigns**:

- Managers receive a certification task: **"My Certifications"** tab.
- For each direct report, managers must **Certify (keep)** or **Revoke** each access item.
- Deadline: 10 business days from campaign start.
- Uncertified items are **automatically revoked** after the deadline.

**Employees:** If you receive an email saying "Your access to [App] has been revoked due to certification," contact your manager to re-request if the access is still required.

---

## 10. SailPoint Self-Service Password Features

From the SailPoint dashboard:
- **Change Password:** Password Management → Change Password.
- **Unlock Account:** Password Management → Unlock Account.
- **Reset Forgotten Password:** From the login page → "Forgot Password."
- **Manage MFA:** Password Management → Manage Authentication Factors.

See **KB Article 002 — Password Reset** for full details.

---

## 11. Troubleshooting SailPoint Issues

| Issue                                  | Resolution                                           |
|----------------------------------------|------------------------------------------------------|
| Cannot log in to SailPoint             | Reset password via `identity.karansystems.in` login page |
| Access item not visible in search      | Contact IAM team — item may not be catalogued        |
| Request stuck in "Pending Approval"    | Check approver via My Requests; escalate if >48 hrs  |
| Access provisioned but not working     | Allow 15 min for AD sync; contact IT Helpdesk         |
| MFA push not received                  | Use backup code or contact IT Helpdesk               |
| Certification emails received in error | Contact IAM Team: `iam@karansystems.in`                |

---

## 12. Related Articles

- KB Article 003 — Access Request Process
- KB Article 008 — Group Membership Request
- KB Article 012 — SailPoint Group Removal
- KB Article 002 — Password Reset Process
- KB Article 010 — Offboarding Process

---

*IAM Team: `iam@karansystems.in` | SailPoint Portal: `identity.karansystems.in` | IT Helpdesk: Ext. 2000*

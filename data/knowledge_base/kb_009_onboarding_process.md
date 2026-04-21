# KB Article 009 — Employee Onboarding Process

**Organization:** Karan Systems Pvt. Ltd.
**Department:** Human Resources / IT Operations
**Version:** 3.2
**Last Updated:** April 2026
**Access Level:** HR, IT, Managers, New Employees

---

## 1. Overview

The Karan Systems onboarding process ensures that every new employee is set up for success from Day 1. This process covers pre-joining activities, Day 1 setup, first-week orientation, access provisioning, and the 90-day integration plan. All onboarding activities are tracked in the **HRMS Portal** and **IT Onboarding Tracker**.

---

## 2. Onboarding Checklist Overview

| Phase                    | Owner        | Timeline                          |
| ------------------------ | ------------ | --------------------------------- |
| Pre-Joining Setup        | HR + IT      | 5–7 business days before joining |
| Day 1 — IT Setup        | IT Support   | Day 1, 9 AM–12 PM                |
| Day 1 — HR Induction    | HR           | Day 1, 1 PM–5 PM                 |
| Week 1 — Access & Tools | IT + Manager | Days 2–5                         |
| 30-Day Check-In          | HR + Manager | Day 30                            |
| 90-Day Review            | Manager + HR | Day 90                            |

---

## 3. Pre-Joining (HR and IT Actions — T-5 Days)

### 3.1 HR Actions

- [ ] Offer letter and joining formalities completed.
- [ ] Employee profile created in **HRMS** with Employee ID, designation, department, and reporting manager.
- [ ] Background verification (BGV) initiated with third-party vendor.
- [ ] Offer confirmation sent to new hire with joining date, reporting location, and contact details.
- [ ] New hire added to the pre-joining portal: `preboarding.karansystems.in` for document submission.
- [ ] Laptop/device request raised with IT (specify: Windows/Mac preference, standard/developer config).

### 3.2 IT Actions (Triggered by HRMS New Hire Record)

- [ ] **Active Directory account created** (format: `firstname.lastname@karansystems.in`).
- [ ] **Microsoft 365 mailbox provisioned** (accessible by Day 1 morning).
- [ ] **SailPoint IdentityNow identity created** (role-based entitlements assigned per job profile).
- [ ] **HRMS access provisioned** (for leave management, payroll, expense claims).
- [ ] **Laptop imaged and configured** (OS, endpoint protection, DLP, MDM enrollment).
- [ ] **MFA pre-enrollment link** sent to personal email for pre-setup.
- [ ] **Welcome email** drafted with Day 1 credentials and instructions.

---

## 4. Day 1 — IT Setup (9 AM – 12 PM)

The IT Support team meets the new hire at the onboarding bay (Floor 3, Karan HQ) or virtually:

### 4.1 Account Setup

1. IT Support hands over the laptop and walks the new hire through:
   - First login with temporary credentials.
   - Mandatory password change (must comply with Karan Password Policy).
   - MFA enrollment (Microsoft Authenticator).
2. New hire verifies:
   - Email (Outlook) is accessible.
   - VPN (Cisco AnyConnect) is installed and connected.
   - HRMS portal is accessible.
   - SailPoint identity portal is accessible.

### 4.2 Standard Tools Installed on Day 1

| Tool                                       | Purpose                                |
| ------------------------------------------ | -------------------------------------- |
| Microsoft 365 (Outlook, Teams, SharePoint) | Communication, collaboration           |
| Cisco AnyConnect                           | VPN                                    |
| Microsoft Authenticator                    | MFA                                    |
| Chrome / Edge                              | Web browsing                           |
| Endpoint Protector (DLP)                   | Data Loss Prevention agent             |
| CrowdStrike Falcon                         | Endpoint security                      |
| Karan HRMS Web App                         | HR portal (web-based)                  |
| SailPoint IdentityNow                      | Identity and access portal (web-based) |

### 4.3 Developer-Specific Tools (For Tech Roles)

- Git + GitHub Desktop
- Docker Desktop
- VS Code + recommended extensions
- JetBrains IDE (IntelliJ / PyCharm)
- Python 3.x / Node.js
- Karan Dev Portal access (`dev.karansystems.in`)
- See KB Article 013 — GitHub Setup for GitHub Org access.

---

## 5. Day 1 — HR Induction (1 PM – 5 PM)

HR conducts a structured induction covering:

1. **Company Overview** — Karan Systems history, mission, values, products.
2. **Organizational Structure** — Leadership team, departments, reporting hierarchy.
3. **HR Policies Overview:**
   - Leave Policy (KB Article 001)
   - Code of Conduct
   - Anti-Harassment Policy
   - Work-from-Home Policy
4. **Benefits Overview** — Health insurance, provident fund, meal allowance, wellness programs.
5. **Payroll & Expense** — Pay cycle, expense claim process (SAP Concur).
6. **IT & Security Awareness** — Password policy, phishing awareness, data classification.
7. **HRMS Demo** — Leave application, payslip download, attendance management.

---

## 6. Week 1 — Access and Tool Setup (Days 2–5)

| Day   | Activity                                               | Owner             |
| ----- | ------------------------------------------------------ | ----------------- |
| Day 2 | Manager introduces team; project overview meeting      | Manager           |
| Day 2 | Role-specific application access requests submitted    | Employee + IT     |
| Day 3 | SailPoint access provisioned (role-based standard set) | IAM Team          |
| Day 3 | GitHub Org invite sent (for tech roles)                | IT / GitHub Admin |
| Day 4 | Tool-specific training (JIRA, Confluence, SAP, etc.)   | Manager / L&D     |
| Day 5 | End of Week 1 check-in with Manager and HR             | HR + Manager      |

---

## 7. Standard Access Provisioned Based on Role

| Role          | Standard Access Provisioned                             |
| ------------- | ------------------------------------------------------- |
| All Employees | Email, HRMS, VPN, Intranet, Teams                       |
| Finance       | SAP Finance module, Finance Drive, FINANCE_APP_USERS    |
| HR            | HRMS full access, employee records, ATS                 |
| IT Support    | Helpdesk portal, AD read, SailPoint operator role       |
| Developer     | GitHub Org, dev servers, CI/CD (Jenkins/GitHub Actions) |
| Manager       | HRMS manager view, approval workflows, team reports     |

Additional access beyond this standard set requires a request via SailPoint or IT Helpdesk.

---

## 8. 30-Day and 90-Day Check-Ins

### 8.1 30-Day Check-In (HR + Manager)

- Review onboarding experience.
- Identify any pending access or tool gaps.
- HR collects feedback on induction quality.
- Manager sets 30-day goals.

### 8.2 90-Day Review (Manager-Led)

- Formal performance discussion.
- Confirm probation completion (if applicable).
- Finalize permanent access based on demonstrated role requirements.
- Identify training and development needs.

---

## 9. Onboarding for Remote Employees

For employees joining remotely:

- Laptop is couriered to the home address 2 days before joining.
- IT conducts a **virtual setup call** (1 hour) on Day 1 morning via Microsoft Teams.
- Digital signing of all joining documents via **DocuSign**.
- HR Induction conducted via Teams (recorded and available on the Intranet for 30 days).
- New hire buddy program: A senior employee is assigned to guide the new hire for 30 days.

---

## 10. Contacts for Onboarding Issues

| Issue                    | Contact                          |
| ------------------------ | -------------------------------- |
| Missing laptop/equipment | IT Helpdesk: Ext. 2000           |
| Access not provisioned   | IAM Team:`iam@karansystems.in` |
| HRMS onboarding issues   | HR Helpdesk: Ext. 1001           |
| Policy questions         | HR Business Partner              |
| Manager/team questions   | Assigned buddy or direct manager |

---

## 11. Related Articles

- KB Article 001 — Leave Policy
- KB Article 002 — Password Reset
- KB Article 003 — Access Request
- KB Article 004 — VPN Setup
- KB Article 010 — Offboarding Process
- KB Article 013 — GitHub Setup

---

*Welcome to Karan Systems! For any onboarding support, reach out to `onboarding@karansystems.in`.*

# KB Article 010 — Employee Offboarding Process

**Organization:** Karan Systems Pvt. Ltd.
**Department:** Human Resources / IT Operations / Security
**Version:** 2.6
**Last Updated:** April 2026
**Access Level:** HR, IT Administrators, Managers

---

## 1. Overview

The Karan Systems Offboarding Process ensures that when an employee leaves the organization — through resignation, termination, retirement, or end of contract — all access is securely revoked, assets are returned, and compliance requirements are met. Proper offboarding is critical to protecting company data and systems.

> ⚠️ **Security Priority:** Incomplete offboarding is a significant security risk. All steps in this process must be completed within defined SLAs.

---

## 2. Types of Departures

| Departure Type          | Notice Period              | Offboarding Timeline                   |
| ----------------------- | -------------------------- | -------------------------------------- |
| Voluntary Resignation   | 30–90 days (per contract) | Begin on last working day confirmation |
| Involuntary Termination | Immediate                  | Immediate access revocation            |
| End of Contract         | Defined in contract        | 5 days before contract end             |
| Retirement              | 3 months advance           | Gradual transition over 30 days        |
| Mutual Separation       | Negotiated                 | Per separation agreement               |

---

## 3. Offboarding Initiation

### 3.1 Resignation (Employee-Initiated)

1. Employee submits resignation letter to manager (and HR via email to `hr@karansystems.in`).
2. Manager acknowledges and forwards to HR Business Partner.
3. HR raises an **Offboarding Request** in HRMS → **Offboarding Management → Initiate Offboarding**.
4. This automatically:
   - Sets the employee's last working day in HRMS.
   - Notifies IT, IT Security, Payroll, and Admin teams.
   - Creates an offboarding checklist in the system.

### 3.2 Termination (HR/Manager-Initiated)

1. HR Business Partner initiates offboarding in HRMS immediately upon management decision.
2. **Immediate (T+0) actions triggered automatically:**
   - All Active Directory accounts disabled.
   - VPN access revoked.
   - All SailPoint entitlements revoked.
   - Email access set to read-only (for 30-day data preservation period).
3. HR notifies manager to facilitate asset collection.

---

## 4. IT Offboarding Checklist

### 4.1 Day of Last Working Day (or Immediately for Termination)

**IT Security / IAM Actions (Automated via HRMS → SailPoint Integration):**

- [ ] **Active Directory account disabled** (not deleted — retained for 90 days).
- [ ] **SailPoint entitlements revoked** — all group memberships and app access removed.
- [ ] **VPN access revoked** — user removed from VPN security group.
- [ ] **Microsoft 365 license revoked** — mailbox converted to shared mailbox (retained 30 days).
- [ ] **Email auto-forward set** (if applicable) to manager or team DL.
- [ ] **Out-of-Office message set** on the departing employee's mailbox.
- [ ] **GitHub Org membership removed** (see KB Article 013).
- [ ] **SSH keys revoked** (if applicable — for developers).
- [ ] **API keys and tokens deactivated** (developer accounts, CI/CD tokens).
- [ ] **Mobile device MDM wipe triggered** (if company-owned device is not returned).

> **Trigger Alert:** Any access removal from sensitive groups (FINANCE_APP_USERS, HR_RECORDS_ACCESS, PROD_DB_ADMIN) generates a **Security Alert** logged in the SIEM. This is reviewed by IT Security within 4 hours.

### 4.2 Within 5 Business Days

- [ ] User's data (OneDrive, shared files) transferred to manager or archived.
- [ ] Shared mailbox access audited and external delegates removed.
- [ ] Service accounts owned by departing employee reassigned.
- [ ] Shared credentials (if any) rotated.
- [ ] Active Directory account scheduled for deletion (90 days post-departure).

---

## 5. HR Offboarding Checklist

### 5.1 During Notice Period

- [ ] Knowledge transfer plan created and signed off by manager.
- [ ] Handover documentation completed.
- [ ] Pending leaves cleared (paid out or adjusted in final settlement).
- [ ] Expense claims submitted and approved.
- [ ] NDA, IP assignment, and non-solicitation reminders signed (if applicable).

### 5.2 On Last Working Day

- [ ] Exit interview conducted by HR (via Teams or in-person).
- [ ] HRMS access withdrawn at EOD.
- [ ] Final settlement statement issued.
- [ ] Experience letter and relieving letter prepared (issued within 15 business days).
- [ ] PF and gratuity processing initiated.

---

## 6. Asset Return Checklist

Departing employees must return all company assets:

| Asset                         | Return To          | Deadline         |
| ----------------------------- | ------------------ | ---------------- |
| Laptop / MacBook              | IT Support Desk    | Last working day |
| Mobile Phone (company-issued) | IT Support Desk    | Last working day |
| Access card / Badge           | Admin / Facilities | Last working day |
| USB tokens / RSA keys         | IT Security        | Last working day |
| Physical documents / files    | Manager            | Last working day |

**Asset return confirmation** is mandatory before the final settlement is processed.

---

## 7. Data Handling After Departure

- **Employee's OneDrive/shared files:** Transferred to manager or archived by IT within 5 business days.
- **Email:** Converted to shared mailbox, accessible by manager for 30 days, then archived for 1 year.
- **Personal data:** Removed from HRMS active records, retained in archive as per data retention policy (7 years for statutory compliance).
- **IT logs and audit trails:** Retained for 1 year minimum.

---

## 8. Offboarding for Contractors / Vendors

Contractor offboarding follows a similar process but with tighter timelines:

- All access revoked on the contract end date (or immediately upon early termination).
- Equipment returned within 24 hours.
- VPN and guest network access removed.
- The sponsoring Karan employee is notified and responsible for confirming asset return.

Submit contractor offboarding request at: `helpdesk.karansystems.in` → HR Services → Contractor Offboarding.

---

## 9. Common Offboarding Errors and Their Impact

| Error                                            | Risk                           | Reference Incident |
| ------------------------------------------------ | ------------------------------ | ------------------ |
| Access not revoked on last day                   | Unauthorized data access       | INC001             |
| Group membership removed incorrectly (premature) | Loss of access before last day | INC001 (related)   |
| Manager not notified of departure                | Pending approvals orphaned     | —                 |
| Laptop not wiped before reallocation             | Data leakage to next user      | —                 |

> 📌 **Incident INC001 Reference:** In April 2026, user Adam Fox lost access to FINANCE_APP one day before his last working day due to an incorrect offboarding trigger. The group `FINANCE_APP_USERS` was removed prematurely by an automated workflow misconfiguration. Resolution: group membership was restored by the IAM team within 2 hours.

---

## 10. Offboarding Checklist Summary (Printable)

```
EMPLOYEE NAME: ________________   EMPLOYEE ID: ________________
LAST WORKING DAY: ______________  DEPARTMENT: _________________

IT ACTIONS:
[ ] AD account disabled
[ ] SailPoint entitlements revoked
[ ] VPN access removed
[ ] M365 license revoked
[ ] GitHub org removed
[ ] Email auto-forward set
[ ] SSH keys revoked

HR ACTIONS:
[ ] Exit interview completed
[ ] Handover documents signed
[ ] HRMS access withdrawn
[ ] Final settlement initiated
[ ] Relieving letter prepared

ASSETS:
[ ] Laptop returned
[ ] Badge returned
[ ] Mobile returned

SIGNATURES:
Manager: ________________  HR BP: ________________  IT Lead: ________________
```

---

## 11. Related Articles

- KB Article 003 — Access Request Process
- KB Article 007 — Manager Change Process
- KB Article 008 — Group Membership Request
- KB Article 012 — SailPoint Group Removal

---

*HR Helpdesk: `hr@karansystems.in` | IT Security: `security@karansystems.in` | IT Helpdesk: Ext. 2000*

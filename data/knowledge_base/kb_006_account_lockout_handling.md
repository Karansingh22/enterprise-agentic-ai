# KB Article 006 — Account Lockout Handling
**Organization:** Karan Systems Pvt. Ltd.
**Department:** IT Support / Identity & Access Management
**Version:** 1.5
**Last Updated:** April 2026
**Access Level:** All Employees

---

## 1. Overview

An account lockout occurs when a user exceeds the maximum number of failed login attempts for any Karan Systems service (Windows workstation, VPN, Microsoft 365, SailPoint, or any integrated SSO application). This is a security control to protect accounts from brute-force attacks. This article explains the lockout policy, how to identify a lockout, and how to resolve it quickly.

---

## 2. Karan Systems Lockout Policy

| Parameter                  | Value                                     |
|----------------------------|-------------------------------------------|
| Max Failed Attempts         | 5 consecutive failed attempts             |
| Lockout Duration (Auto)    | 15 minutes (for non-critical systems)     |
| Admin Reset Required       | For critical systems (AD, VPN, SailPoint) |
| Observation Window          | 10 minutes                                |
| Threshold Source           | Active Directory Group Policy             |

> **Critical Systems (require manual unlock):** Active Directory (Windows login), VPN, SailPoint IdentityNow, SAP, Production Applications.

---

## 3. How to Identify an Account Lockout

### 3.1 Windows Workstation Lockout

- Login screen shows: **"The referenced account is currently locked out and may not be logged on to."**
- Error Code: `0xC0000234`

### 3.2 Microsoft 365 / Outlook Lockout

- Browser shows: **"Your account has been locked. Contact your admin."**
- Error Code: `AADSTS50053`

### 3.3 SailPoint / SSO Application Lockout

- SailPoint portal shows: **"Account is locked. Please contact your administrator or use self-service."**

### 3.4 VPN Lockout

- Cisco AnyConnect shows: **"Login Failed — Account Locked."**

---

## 4. Resolution — Self-Service Unlock

### 4.1 Via SailPoint Self-Service (Fastest)

1. Navigate to `identity.karansystems.in` from a mobile browser or a colleague's computer.
2. Click **"Need Help Signing In?"**.
3. Select **"Unlock My Account"**.
4. Enter your Karan Employee ID.
5. Verify your identity using MFA (SMS OTP or Authenticator).
6. Your account will be unlocked within 60 seconds.
7. Wait 2–3 minutes before attempting to log in again.

### 4.2 Via IT Helpdesk (If Self-Service Not Available)

1. Contact IT Helpdesk:
   - Phone: Ext. 2000 (fastest)
   - Email: `it-helpdesk@karansystems.in`
   - Portal: `helpdesk.karansystems.in` → New Ticket → Account Management → Unlock Account
2. Provide your **Employee ID** and the system you are locked out of.
3. IT agent will verify your identity (Employee ID + last 4 digits of registered mobile).
4. Unlock is performed within **15 minutes** during business hours.

---

## 5. Common Causes of Account Lockout

Understanding the root cause helps prevent repeat lockouts:

| Root Cause                              | How to Fix                                      |
|-----------------------------------------|--------------------------------------------------|
| Forgotten new password after reset     | Use self-service to reset password again         |
| Old password cached on mobile/tablet   | Update saved password on all devices             |
| Scheduled tasks using old credentials  | Update service account credentials               |
| Multiple devices logging in simultaneously | Ensure all devices use the same current password |
| Mapped network drives with old credentials | Re-map drives with updated credentials          |
| Browser cached credentials             | Clear browser saved passwords                   |

---

## 6. Preventing Future Lockouts

### After a Password Change

When you change your password, update it **everywhere immediately**:
- ✅ Windows laptop
- ✅ Mobile phone (Outlook app, VPN client, Authenticator)
- ✅ Tablet / secondary devices
- ✅ Mapped network drives
- ✅ Any saved passwords in browsers (Chrome, Edge, Firefox)
- ✅ Desktop email clients (Outlook, Thunderbird)

### Pro Tip

If you are changing your password, disconnect from VPN, change the password, then reconnect VPN. This prevents cached credential conflicts.

---

## 7. Repeated Lockouts (Pattern Behavior)

If an employee is experiencing lockouts repeatedly (more than 2 times per week), the IT Security team will:

1. Perform an **Active Directory Lockout Investigation**.
2. Review event logs to identify the source machine triggering failed logins.
3. Remediate the root cause (stale credentials on a device or scheduled task).

To request an investigation: `security@karansystems.in` with subject line: **"Repeated Account Lockout — [Employee ID]"**

---

## 8. Account Lockout Investigation for IT Admins

*(For IT/Security staff reference)*

```powershell
# Check lockout status
Search-ADAccount -LockedOut | Select-Object Name, SamAccountName, LockedOut

# Find lockout source (run on domain controller)
Get-WinEvent -ComputerName <DC_NAME> -FilterHashtable @{
    LogName = 'Security'
    Id = 4740
} | Select-Object TimeCreated, Message | Where-Object {$_.Message -like "*<username>*"}

# Unlock account
Unlock-ADAccount -Identity "<SamAccountName>"
```

**Key Event IDs:**
- `4740` — Account was locked out
- `4625` — Failed login attempt (source machine visible)
- `4776` — Credential validation failed

---

## 9. Related Articles

- KB Article 002 — Password Reset Process
- KB Article 003 — Access Request Process
- KB Article 011 — SailPoint Access Request

---

*IT Security Team: `security@karansystems.in` | IT Helpdesk: Ext. 2000*

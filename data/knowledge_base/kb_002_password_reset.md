# KB Article 002 — Password Reset Process
**Organization:** Karan Systems Pvt. Ltd.
**Department:** IT Support / Identity & Access Management
**Version:** 3.0
**Last Updated:** April 2026
**Access Level:** All Employees

---

## 1. Overview

This article describes the standard process for resetting your Karan Systems network password. Password resets may be required when you have forgotten your password, your account has been locked after multiple failed login attempts, or your password has expired as per the organization's password policy. All password-related requests are handled through the **Karan Identity Portal** (powered by SailPoint IdentityNow) or via the IT Helpdesk.

---

## 2. Password Policy — Karan Systems

Before resetting your password, familiarize yourself with the required password standards:

| Requirement         | Rule                                        |
|---------------------|---------------------------------------------|
| Minimum Length      | 12 characters                               |
| Uppercase Letters   | At least 1 uppercase letter (A–Z)           |
| Lowercase Letters   | At least 1 lowercase letter (a–z)           |
| Numbers             | At least 1 digit (0–9)                      |
| Special Characters  | At least 1 special character (e.g., @, #, $, !) |
| Password History    | Cannot reuse the last 10 passwords          |
| Expiry              | Passwords expire every 90 days              |
| Dictionary Words    | Passwords must not contain dictionary words |
| Username            | Password must not contain your username     |

**Examples of compliant passwords:**
- `Karan@Secure#2026!`
- `MyD0g$Fluffy99`

**Examples of non-compliant passwords:**
- `password123` (dictionary word, no special character)
- `Admin2026` (too predictable, no special character)

---

## 3. Self-Service Password Reset (SSPR)

### 3.1 Prerequisites

To use self-service password reset, employees must have previously set up their **Multi-Factor Authentication (MFA)** and registered at least one recovery method:

- Mobile phone (OTP via SMS)
- Authenticator app (Microsoft Authenticator / Google Authenticator)
- Alternate email address

MFA setup is mandatory during onboarding. Contact the IT Helpdesk if you have not completed MFA setup.

### 3.2 Steps to Reset Password via Self-Service

1. Navigate to `https://identity.karansystems.in` or click **"Forgot Password?"** on the Windows/VPN login screen.
2. Enter your **Karan Employee ID** (e.g., `EMP101`) or registered email address.
3. Select your preferred verification method (OTP via SMS or Authenticator App).
4. Enter the 6-digit OTP received within 60 seconds.
5. You will be prompted to enter your **new password** and **confirm the new password**.
6. Ensure the new password meets all Karan password policy requirements (see Section 2).
7. Click **Submit**. The system will validate and confirm the password change.
8. Your session will be reset. Log in to all systems (laptop, VPN, email) using the new password.

> ⚠️ **Note:** After a password reset, it may take up to **5 minutes** for the change to propagate across all Karan systems including Active Directory, email, VPN, and application SSO.

---

## 4. IT Helpdesk-Assisted Password Reset

If you are unable to use SSPR (e.g., lost MFA device, no registered recovery method), contact the IT Helpdesk:

### 4.1 Contact Channels

| Channel         | Details                          | Availability        |
|-----------------|----------------------------------|---------------------|
| Phone           | Ext. 2000 / +91-22-XXXX-XXXX    | 8 AM – 8 PM, Mon–Fri |
| Email           | `it-helpdesk@karansystems.in`       | 24/7 (response in 2 hrs) |
| Service Portal  | `helpdesk.karansystems.in` → Raise Ticket | 24/7           |
| Walk-In         | IT Support Desk — Floor 3, HQ   | 9 AM – 6 PM, Mon–Fri |

### 4.2 Identity Verification Process

For helpdesk-assisted resets, the IT agent will verify your identity by:

1. Confirming your **Employee ID** and **registered mobile number**.
2. Asking 2 of the 5 security questions you set during onboarding.
3. If neither is available: HR verification will be initiated (processing time: up to 4 business hours).

### 4.3 Temporary Password Process

1. IT Helpdesk verifies identity.
2. A temporary password is generated and shared via your **registered personal email** or SMS.
3. Temporary passwords are valid for **24 hours** and must be changed on first login.
4. The system will force you to set a permanent password that complies with the Karan password policy.

---

## 5. Account Lockout and Unlock

Your Karan Systems account will be **automatically locked** after **5 consecutive failed login attempts**. Lockouts are separate from password resets.

- **Self-Unlock:** Wait 15 minutes for automatic unlock (applies to non-critical systems).
- **Immediate Unlock:** Contact IT Helpdesk (Ext. 2000) for immediate unlocking.
- **SailPoint Self-Service:** Go to `identity.karansystems.in` → **Manage My Account** → **Unlock Account**.

See **KB Article 006 — Account Lockout Handling** for full details.

---

## 6. Password Reset for Service/Shared Accounts

Shared or service accounts (e.g., team mailboxes, application service accounts) follow a separate process:

1. Submit a request through `helpdesk.karansystems.in` with:
   - Service Account Name
   - Justification
   - Approval from the account owner's manager
2. The IT Security team will process the request within **1 business day**.
3. New credentials will be shared via Karan Vault (encrypted credential store).

---

## 7. Troubleshooting Common Issues

| Issue                              | Resolution                                      |
|------------------------------------|--------------------------------------------------|
| OTP not received                   | Check spam folder; retry after 60 sec; contact IT |
| MFA device lost                    | Contact IT Helpdesk with alternate ID proof     |
| Password reset link expired        | Request a new link from `identity.karansystems.in` |
| New password not accepted          | Ensure compliance with password policy (Section 2) |
| VPN still asking for old password  | Disconnect and reconnect; may take 5 min to sync |
| Outlook prompting for password     | Sign out and re-enter credentials              |

---

## 8. Related Articles

- KB Article 006 — Account Lockout Handling
- KB Article 003 — Access Request Process
- KB Article 011 — SailPoint Access Request

---

*For escalations, contact the IT Security Team at `security@karansystems.in`.*

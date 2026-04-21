# KB Article 005 — Email Access Issue
**Organization:** Karan Systems Pvt. Ltd.
**Department:** IT Support / Microsoft 365 Administration
**Version:** 2.0
**Last Updated:** April 2026
**Access Level:** All Employees

---

## 1. Overview

Karan Systems uses **Microsoft 365 (Outlook)** as its official email platform. This article covers common email access issues employees may encounter — including login failures, mailbox not loading, Outlook configuration problems, and shared mailbox access — and their step-by-step resolutions.

---

## 2. Common Email Access Issues and Resolutions

### 2.1 Cannot Log In to Outlook / Microsoft 365

**Symptoms:** Login page shows error; credentials not accepted; redirected to error page.

**Possible Causes and Fixes:**

| Cause                               | Resolution                                                             |
|-------------------------------------|------------------------------------------------------------------------|
| Incorrect password                  | Reset password via `identity.karansystems.in` (KB Article 002)           |
| Account locked                      | Unlock via SailPoint or contact IT Helpdesk (KB Article 006)           |
| MFA prompt failing                  | Re-register MFA device; contact IT Helpdesk                            |
| Browser compatibility issue         | Try a different browser (Chrome, Edge recommended) or clear cache      |
| Microsoft 365 service outage        | Check `status.office365.com` for active incidents                      |

**Steps to resolve login issue:**
1. Go to `https://outlook.office365.com`.
2. Click **"Sign In"** and enter your Karan email (e.g., `adam.fox@karansystems.in`).
3. Enter your Karan network password.
4. Approve the MFA prompt on your phone.
5. If login fails with "Invalid Credentials": reset password via KB Article 002.
6. If login fails with "Account Disabled": contact IT Helpdesk immediately.

---

### 2.2 Outlook Desktop App Not Loading / Prompting for Password Repeatedly

**Symptoms:** Outlook opens but keeps asking for password; "Trying to connect..." indefinitely.

**Step-by-Step Fix:**

1. **Remove and re-add the account:**
   - Open Outlook → File → Account Settings → Account Settings.
   - Select your email account → Remove.
   - Restart Outlook → Add Account → enter your Karan email.
   - Follow the auto-configuration wizard.

2. **Clear saved credentials:**
   - Windows: Control Panel → Credential Manager → Windows Credentials.
   - Remove all entries related to `MicrosoftOffice`, `outlook`, or `kaisystems`.
   - Restart Outlook and re-login.

3. **Reset the Outlook profile:**
   - Open Run (Win+R) → type `outlook.exe /resetnavpane` → Enter.
   - If issue persists: Control Panel → Mail → Show Profiles → Add a new profile.

4. **Repair Office Installation:**
   - Control Panel → Programs → Microsoft 365 → Change → Quick Repair.
   - If Quick Repair fails, run Online Repair (requires internet).

---

### 2.3 Mailbox Not Found / Provisioning Delay

**Symptoms:** Newly joined employee cannot access email; mailbox shows as non-existent.

**Expected Behavior:** New employee mailboxes are provisioned within **4 business hours** of account creation. If the mailbox is not available after 4 hours:

1. Check with your manager that the onboarding request was submitted in HRMS.
2. Contact IT Helpdesk at `it-helpdesk@karansystems.in` with your Employee ID.
3. IT will manually trigger mailbox provisioning.
4. Estimated resolution: 1–2 business hours after ticket creation.

---

### 2.4 Email Not Syncing on Mobile

**Symptoms:** Mobile Outlook not receiving new emails; calendar not syncing.

**Fix Steps:**

1. Open **Outlook Mobile App** → Settings (profile icon) → Select account.
2. Scroll down → Tap **"Reset Account"**.
3. Sign in again with Karan credentials and approve MFA.
4. If sync is still failing:
   - Delete the account from the Outlook mobile app.
   - Re-add it by entering `adam.fox@karansystems.in` (your Karan email).
   - Outlook Mobile will auto-detect Exchange settings.
5. Ensure mobile device is not in **battery saver mode** (restricts background sync).

---

### 2.5 Cannot Access Shared Mailbox

**Symptoms:** Shared mailbox not visible in Outlook; "Permission denied" when opening shared mailbox.

**Resolution:**

- Shared mailbox access is managed through **SailPoint** and **Active Directory groups**.
- If you need access to a shared mailbox, submit an access request:
  1. Go to `identity.karansystems.in` → Request Access.
  2. Search for the shared mailbox name (e.g., `support@karansystems.in`).
  3. Submit request with business justification.
  4. Manager approval → IT provisions access within 4 hours.

**If access was recently granted and mailbox is not appearing:**
1. Close and reopen Outlook.
2. File → Account Settings → Download Address Book → update.
3. If still not visible after 30 minutes, contact IT Helpdesk.

---

### 2.6 Email Being Blocked / Marked as Spam

**Symptoms:** Outgoing emails to external domains are blocked; recipients not receiving emails.

**Cause:** Microsoft Defender for Office 365 may flag emails based on content or recipient behavior.

**Resolution:**
1. Do **not** send bulk emails from your personal mailbox — use the approved mass mailing tool (Mailchimp via IT-managed account).
2. If a legitimate email was blocked, submit a ticket at `helpdesk.karansystems.in` with the message ID (found in sent items).
3. IT will whitelist the domain if appropriate.

---

### 2.7 Mailbox Storage Full

**Warning:** "Your mailbox is almost full" notification in Outlook.

| Mailbox Size Limits (Karan Standard) |            |
|------------------------------------|------------|
| Standard Employee Mailbox          | 50 GB      |
| Manager / Director Mailbox         | 100 GB     |
| Archive Mailbox (auto-enabled)     | Unlimited  |

**Steps to free up space:**
1. Empty the **Deleted Items** and **Junk Email** folders.
2. Archive older emails: File → Cleanup Tools → Archive.
3. Move large attachments to **SharePoint or OneDrive** and replace with a link.
4. Request mailbox size increase via `helpdesk.karansystems.in` (Managers+ only).

---

## 3. Email Configuration Settings (Manual Setup)

If manual Outlook configuration is needed:

| Setting             | Value                            |
|---------------------|----------------------------------|
| Account Type        | Microsoft 365 / Exchange         |
| Incoming Server     | `outlook.office365.com`          |
| Outgoing Server     | `smtp.office365.com`             |
| Port (SMTP)         | 587 (TLS)                        |
| Port (IMAP)         | 993 (SSL)                        |
| Authentication      | Modern Authentication (OAuth2)   |

---

## 4. Escalation Path

| Level     | Contact                       | When to Use                          |
|-----------|-------------------------------|--------------------------------------|
| Level 1   | IT Helpdesk — Ext. 2000       | General Outlook issues               |
| Level 2   | M365 Admin Team — `m365@karansystems.in` | Account provisioning, policy issues |
| Level 3   | IT Security — `security@karansystems.in` | Suspected compromise, phishing       |

---

## 5. Related Articles

- KB Article 002 — Password Reset Process
- KB Article 006 — Account Lockout Handling
- KB Article 003 — Access Request Process

---

*Karan Systems IT Helpdesk: `it-helpdesk@karansystems.in` | Ext. 2000 | Available Mon–Fri, 8 AM–8 PM*

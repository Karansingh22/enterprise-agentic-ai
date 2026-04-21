# Karan Systems Pvt. Ltd. — Information Security Policy
**Version:** 3.1 | **Last Updated:** April 2026
**Classification:** Internal | All Employees Must Comply

---

## 1. Purpose

This policy establishes the security requirements that all Karan Systems employees, contractors, and vendors must follow to protect the confidentiality, integrity, and availability of company information and systems.

## 2. Scope

Applies to all employees, contractors, and third-party vendors who access Karan Systems systems, data, or networks — regardless of location.

## 3. Password and Authentication Policy

- All employees must follow the Karan password policy: 12+ characters, uppercase, number, special character.
- Passwords expire every 90 days. Reuse of last 10 passwords is prohibited.
- Multi-Factor Authentication (MFA) is mandatory for all system access.
- Sharing of credentials is strictly prohibited and is grounds for disciplinary action.
- Service accounts must have unique passwords stored in Karan Vault.

## 4. Access Control Policy

- Access is granted on the Principle of Least Privilege.
- All access requests must go through SailPoint IdentityNow (identity.karansystems.in).
- Access is approved by the direct manager and data owner.
- Privileged access (admin, root) requires IT Security approval.
- Access is automatically reviewed quarterly via SailPoint certification campaigns.
- Access to sensitive data (HR records, financial data) is restricted to authorized roles only:
  - HR data: HR department only
  - Financial data: Finance department + Managers
  - Production systems: DevOps/IT Admin only

## 5. Data Classification and Handling

| Classification | Examples                          | Handling Requirements                        |
|----------------|-----------------------------------|----------------------------------------------|
| Public         | Marketing materials, job posts    | No restrictions                              |
| Internal       | Process docs, KB articles         | Do not share externally without approval     |
| Confidential   | Employee data, financials, contracts | Encrypt at rest and in transit; no personal email |
| Restricted     | Source code, prod credentials     | Strict access controls; audit trail required |

- Confidential and Restricted data must never be stored on personal devices.
- Confidential data must not be shared via WhatsApp, personal email, or USB drives.
- All confidential documents must be stored on approved KaranDrive (SharePoint).

## 6. Incident Reporting

- All suspected security incidents must be reported immediately to security@karansystems.in or Ext. 2911.
- Incidents include: unauthorized access, phishing, data loss, lost devices, suspicious logins.
- Employees must NOT attempt to investigate incidents themselves — report and let IT Security handle.
- Failure to report a known incident is a policy violation.

## 7. Device and Endpoint Policy

- Only company-managed (MDM-enrolled) devices may access corporate resources.
- Full disk encryption (BitLocker/FileVault) is mandatory on all company laptops.
- CrowdStrike Falcon EDR must be active at all times — do not disable.
- Auto-lock must be configured: screen locks after 5 minutes of inactivity.
- Lost or stolen devices must be reported to IT Helpdesk within 1 hour.

## 8. Remote Work and VPN Policy

- VPN (Cisco AnyConnect) must be used for all access to internal systems from remote locations.
- VPN credentials must not be shared.
- Public Wi-Fi (cafes, airports, hotels) must only be used with VPN connected.
- VPN logs are retained for 90 days for security audit purposes.

## 9. Acceptable Use Policy

- Company systems are for business use. Limited personal use is acceptable but must not violate this policy.
- Accessing, storing, or transmitting illegal, offensive, or unauthorized content is prohibited.
- Installing unauthorized software on company devices is prohibited.
- Disabling security tools (antivirus, DLP, MFA) is a policy violation subject to immediate disciplinary action.

## 10. Consequences of Violation

- Minor violations: Formal written warning + remedial security training.
- Moderate violations: Suspension pending investigation.
- Severe violations (data theft, intentional breach, credential sharing with external parties): Immediate termination + legal action.

---
*Policy Owner: CISO — security@karansystems.in | Review cycle: Annual*

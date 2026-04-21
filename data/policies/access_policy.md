# Karan Systems Pvt. Ltd. — Access Management Policy
**Version:** 2.5 | **Last Updated:** April 2026
**Classification:** Internal

---

## 1. Overview

This policy governs how access to Karan Systems applications, systems, data, and infrastructure is requested, approved, provisioned, reviewed, and revoked.

## 2. Identity Platform

All identity and access is managed via **SailPoint IdentityNow** at `identity.karansystems.in`.

## 3. Access Request Rules

- All access requests must be submitted via SailPoint or IT Helpdesk Portal.
- Business justification is mandatory for all requests.
- Access cannot be self-approved — manager sign-off is required.
- Employees can only request access at or below their authorized level.
- Requests are tracked and audited; retroactive access grants are not permitted.

## 4. Role-Based Access Entitlements

### Standard Entitlements (Auto-provisioned on Joining)
All employees receive on Day 1:
- Active Directory account
- Microsoft 365 (Email, Teams, SharePoint, OneDrive)
- HRMS portal access (personal data only)
- SailPoint portal (self-service)
- Corporate Intranet
- VPN (Cisco AnyConnect)

### Role-Specific Entitlements
Role-based entitlements are defined in the HR Job Catalog. Examples:
- Finance: SAP Finance, FINANCE_APP_USERS, Finance Drive
- HR: HRMS full access, HR_RECORDS_ACCESS, ATS
- Developer: GitHub Org, dev/staging server access, CI/CD tools
- Manager: Team reports, approval workflows, HRMS manager view

### Privileged Access
Privileged access (server admin, database, network) requires:
1. Manager approval
2. IT Security approval
3. Documented business justification with project code
4. Maximum 90-day grant; renewal requires fresh approval

## 5. Segregation of Duties (SoD)

The following role combinations are prohibited:
- SAP_PAYMENT_CREATOR + SAP_PAYMENT_APPROVER (financial fraud prevention)
- HR_RECORDS_ACCESS + FINANCE_APP_ADMIN (data isolation)
- PROD_DB_WRITE + PROD_DEPLOY_ADMIN (change control)

SailPoint enforces SoD rules automatically; conflicting access requests are blocked.

## 6. Access Review (Certification)

- Quarterly access certification campaigns are run via SailPoint.
- Managers must certify or revoke all access for their direct reports.
- Deadline: 10 business days from campaign launch.
- Uncertified access is automatically revoked.

## 7. Access Revocation

### Standard Revocation
- Employee resignation: All access revoked on last working day.
- Role change: Old role access revoked; new role access provisioned.
- Project end: Temporary access auto-expires.

### Emergency Revocation
In security incidents, access can be revoked immediately:
- Contact IAM on-call: iam-oncall@karansystems.in or Ext. 2911
- AD account can be disabled by IT Security in < 30 minutes
- SailPoint revocation: < 30 minutes for emergency cases

## 8. Vendor and Contractor Access

- All vendor access requires a KAI employee sponsor.
- Vendor access is restricted to the KAI-Vendor VPN group.
- Maximum duration: 12 months; renewal requires fresh approval.
- Vendor access is in a separate AD OU and monitored with enhanced logging.

---
*Policy Owner: IAM Team — iam@karansystems.in | IT Security — security@karansystems.in*

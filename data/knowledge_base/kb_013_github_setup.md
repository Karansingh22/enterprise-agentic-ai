# KB Article 013 — GitHub Organization Setup Guide

**Organization:** Karan Systems Pvt. Ltd.
**Department:** IT Support / Engineering / DevOps
**Version:** 2.5
**Last Updated:** April 2026
**Access Level:** Developers, DevOps, Tech Leads, IT Admins

---

## 1. Overview

Karan Systems uses **GitHub Enterprise Cloud** as its central platform for source code management, version control, code reviews, CI/CD workflows, and technical documentation. All engineers, developers, and technical staff are expected to work within the **Karan Systems GitHub Organization** (`github.com/karan-systems`).

This article covers: how to get access to the GitHub Organization, repository access, team membership, SSH key setup, security configurations, and best practices.

---

## 2. GitHub Access Prerequisites

Before requesting GitHub access, ensure:

| Prerequisite            | Details                                                          |
| ----------------------- | ---------------------------------------------------------------- |
| Personal GitHub Account | Create one at `github.com` if you don't have one               |
| Work Email on GitHub    | Add `yourname@karansystems.in` to your GitHub account settings |
| Karan SSO Configured    | GitHub Org uses SAML SSO via Microsoft Entra ID (Azure AD)       |
| Manager Approval        | GitHub access requires manager sign-off in SailPoint             |
| Device Compliance       | Only MDM-enrolled devices should be used for GitHub              |

---

## 3. Requesting GitHub Organization Access

### 3.1 Via SailPoint (Recommended)

1. Log in to SailPoint at `identity.karansystems.in`.
2. Navigate to **Request Access**.
3. Search for **"GitHub"** — You will see the following access items:
   - `GitHub — Org Member (Read)` — View public/internal repos
   - `GitHub — Developer (Write)` — Push code, open PRs
   - `GitHub — Team: [Team Name]` — Access to specific team repos
4. Select the appropriate access item, add it to cart.
5. **Justification example:** *"Joining the Platform Engineering team. Need Developer write access to karan-systems/platform-infra and karan-systems/backend-services repositories."*
6. Submit. Manager approval required. SLA: 1 business day.

### 3.2 Via IT Helpdesk (Alternative)

1. Raise a ticket at `helpdesk.karansystems.in` → Access Management → GitHub Access.
2. Provide:
   - Your GitHub username
   - Your Karan work email
   - Required access level (Org Member / Developer / Team)
   - Team name(s) if applicable
   - Manager email for approval

### 3.3 Once Request is Approved

1. You will receive a GitHub organization invitation at your GitHub-registered email.
2. **Accept the invitation within 7 days** (it expires after 7 days; a new one must be requested).
3. After joining the org, **configure SAML SSO**:
   - Go to `github.com/orgs/karan-systems/sso`
   - Click **"Authorize"** and log in with your Karan Microsoft SSO credentials.
   - SAML SSO authorization is **mandatory** — repositories will be inaccessible without it.

---

## 4. GitHub Teams and Repository Access

At Karan Systems, repository access is managed through **GitHub Teams** (not individual assignments):

| Team Name            | Access Level           | Members                |
| -------------------- | ---------------------- | ---------------------- |
| `kai-platform-eng` | Write (Platform repos) | Platform Engineers     |
| `kai-backend`      | Write (Backend repos)  | Backend Developers     |
| `kai-frontend`     | Write (Frontend repos) | Frontend Developers    |
| `kai-devops`       | Admin (Infra repos)    | DevOps/SRE Engineers   |
| `kai-security`     | Read (All repos)       | Security Team          |
| `kai-tech-leads`   | Maintain (Key repos)   | Tech Leads, Architects |
| `kai-contractors`  | Read (Specific repos)  | External Contractors   |

### Requesting Team Membership

1. Identify the team you need to join (ask your manager or Tech Lead).
2. Submit a request via SailPoint or IT Helpdesk with the team name.
3. The GitHub Organization Admin or the Team Maintainer approves the request.
4. Once added, you can see the team's repositories under `github.com/orgs/karan-systems/teams`.

---

## 5. Setting Up SSH Keys for GitHub

SSH keys are the recommended authentication method for Git operations at Karan Systems. Password-based authentication is disabled.

### 5.1 Generate an SSH Key

Open Terminal (macOS/Linux) or Git Bash (Windows):

```bash
# Generate a new ED25519 SSH key (recommended)
ssh-keygen -t ed25519 -C "yourname@karansystems.in" -f ~/.ssh/kai_github

# Follow the prompts:
# Passphrase: Set a strong passphrase (mandatory per Karan security policy)
```

> **Note:** RSA keys are also accepted but use 4096-bit minimum: `ssh-keygen -t rsa -b 4096 -C "yourname@karansystems.in"`

### 5.2 Add SSH Key to SSH Agent

```bash
# Start the SSH agent
eval "$(ssh-agent -s)"

# Add your key to the agent
ssh-add ~/.ssh/kai_github
```

For **macOS**, add to `~/.ssh/config` for persistence:

```
Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/kai_github
```

### 5.3 Add SSH Key to GitHub Account

1. Copy the public key:
   ```bash
   cat ~/.ssh/kai_github.pub
   ```
2. Go to GitHub → **Settings → SSH and GPG Keys → New SSH Key**.
3. Title: "Karan MacBook 2026" (descriptive name).
4. Paste the public key content.
5. Click **Add SSH Key**.
6. **Important:** You must also authorize the key for Karan Systems SAML SSO:
   - After adding the key, click **"Configure SSO"** next to the key.
   - Click **"Authorize"** next to `karan-systems` organization.

### 5.4 Test the SSH Connection

```bash
ssh -T git@github.com
# Expected output: Hi yourname! You've successfully authenticated...

# Test with the Karan org (verifies SSO authorization)
ssh -T git@github.com -i ~/.ssh/kai_github
```

---

## 6. Cloning Repositories

### 6.1 Clone via SSH (Recommended)

```bash
git clone git@github.com:karan-systems/repo-name.git
```

### 6.2 Clone via HTTPS + PAT

If SSH is not available (e.g., firewall restrictions):

1. Create a **Personal Access Token (PAT):**
   - GitHub → Settings → Developer Settings → Personal Access Tokens → Tokens (Classic).
   - Click **"Generate new token"**.
   - Scope: `repo`, `read:org`, `workflow`.
   - Expiry: Maximum 90 days (Karan security policy — no non-expiring tokens).
   - **Important:** Authorize the PAT for SAML SSO (Configure SSO → Authorize karan-systems).
2. Clone using HTTPS:
   ```bash
   git clone https://github.com/karan-systems/repo-name.git
   # Username: your GitHub username
   # Password: your PAT (not your GitHub password)
   ```
3. Store PAT securely using Git credential manager:
   ```bash
   git config --global credential.helper store
   # or on macOS:
   git config --global credential.helper osxkeychain
   ```

---

## 7. GitHub Actions and CI/CD

Karan Systems uses **GitHub Actions** for CI/CD pipelines. Key practices:

### 7.1 Secrets Management

- Never hardcode credentials in code or workflow files.
- Store secrets in **GitHub Actions Secrets** (org-level or repo-level).
- Access org-level secrets: `github.com/orgs/karan-systems/settings/secrets/actions`.
- Requesting a new secret: Submit a ticket to `devops@karansystems.in`.

### 7.2 Required Status Checks

All repositories have mandatory status checks before merging to `main`:

- Unit tests (pass rate ≥ 95%)
- Code quality scan (SonarQube)
- Security scan (Snyk / GitHub Advanced Security)
- Peer review (minimum 1 approval from codeowner)

### 7.3 Branch Protection Rules

Karan repos enforce the following on `main` and `release/*` branches:

- Direct push to `main` is **disabled** for all except DevOps admins.
- All changes must go through a **Pull Request (PR)**.
- PRs require at least **1 approved review** from a CODEOWNER.
- Force push is **blocked**.

---

## 8. GitHub Security and Compliance at Karan

| Policy                | Requirement                                       |
| --------------------- | ------------------------------------------------- |
| SAML SSO              | Mandatory for all org members                     |
| MFA on GitHub account | Mandatory (enforced by org policy)                |
| SSH key passphrase    | Mandatory                                         |
| PAT expiry            | Maximum 90 days                                   |
| Code scanning         | Enabled on all repos (GitHub Advanced Security)   |
| Secret scanning       | Enabled — auto-blocks secret leaks in commits    |
| Dependabot            | Enabled — auto-alerts on vulnerable dependencies |
| CODEOWNERS file       | Required in all production repositories           |

---

## 9. Removing GitHub Access (Offboarding)

When an employee leaves Karan Systems:

1. Automated offboarding (via SailPoint) removes the user from the GitHub Organization.
2. User loses access to all private and internal repositories immediately.
3. Any **forks** the user created of Karan repositories are reviewed by the DevOps team.
4. PATs and SSH keys associated with the departed user are revoked from the org level.

Managers can also manually remove a team member:

- GitHub → `github.com/orgs/karan-systems/teams/[team-name]` → Members → Remove.
- Or via SailPoint: Submit a group removal request for the GitHub team (KB Article 012).

---

## 10. Troubleshooting GitHub Issues

| Issue                                 | Resolution                                                 |
| ------------------------------------- | ---------------------------------------------------------- |
| "Organization not found" when cloning | Configure SAML SSO (Section 3.3) and authorize SSH key     |
| SSH key not working                   | Verify SSO authorization on the key (Section 5.3)          |
| 403 error on push                     | Check team membership and repo write permissions           |
| PR blocked from merging               | Check required status checks — ensure all pass            |
| PAT expired                           | Generate a new PAT and re-authorize for Karan SSO          |
| GitHub invitation expired             | Contact IT Helpdesk for a re-invite                        |
| Cannot see org repositories           | Ensure you've joined via SSO (`/orgs/karan-systems/sso`) |

---

## 11. GitHub Org Admin Contacts

| Role                       | Contact                                     |
| -------------------------- | ------------------------------------------- |
| GitHub Org Admin           | `github-admin@karansystems.in`            |
| DevOps / CI-CD Support     | `devops@karansystems.in`                  |
| Security (Secret Scanning) | `security@karansystems.in`                |
| IT Helpdesk                | `it-helpdesk@karansystems.in` / Ext. 2000 |

---

## 12. Related Articles

- KB Article 003 — Access Request Process
- KB Article 008 — Group Membership Request
- KB Article 011 — SailPoint Access Request
- KB Article 012 — SailPoint Group Removal
- KB Article 009 — Onboarding Process

---

*DevOps Team: `devops@karansystems.in` | GitHub Org: `github.com/karan-systems` | IT Helpdesk: Ext. 2000*

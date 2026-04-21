# KB Article 004 — VPN Access Setup
**Organization:** Karan Systems Pvt. Ltd.
**Department:** IT Infrastructure / Network Security
**Version:** 1.8
**Last Updated:** April 2026
**Access Level:** All Employees

---

## 1. Overview

Karan Systems uses a **corporate VPN (Virtual Private Network)** to provide employees secure remote access to internal systems, applications, and file servers. All employees working remotely — from home, client sites, or travel — **must** connect to the Karan VPN before accessing any internal resource.

Karan Systems uses **Cisco AnyConnect Secure Mobility Client** as its VPN solution. This article covers installation, initial setup, connection steps, and troubleshooting.

---

## 2. VPN Access Prerequisites

Before setting up the VPN, ensure the following:

| Requirement              | Details                                        |
|--------------------------|------------------------------------------------|
| Karan Employee Account     | Active Windows/Mac login credentials           |
| MFA Enrolled             | Microsoft Authenticator or Google Authenticator |
| Device Compliance        | Company-managed or MDM-enrolled personal device |
| OS Version               | Windows 10/11, macOS 12+, Ubuntu 20.04+        |
| IT Security Clearance    | VPN access auto-provisioned for full-time employees; contractors must submit a request |

---

## 3. Installing Cisco AnyConnect

### 3.1 Windows Installation

1. Go to `vpn.karansystems.in` in your browser.
2. Log in with your **Karan Employee ID** and **password**.
3. Click **"Download AnyConnect"** for Windows.
4. Run the downloaded `.exe` installer as Administrator.
5. Accept the license agreement and select **"VPN"** in the component selection screen.
6. Complete the installation. Cisco AnyConnect will appear in your system tray.

### 3.2 macOS Installation

1. Go to `vpn.karansystems.in` in Safari or Chrome.
2. Log in with your Karan credentials.
3. Download the `.dmg` installer for macOS.
4. Open the `.dmg` and run `AnyConnect.pkg`.
5. Follow the installation wizard. You may need to approve the system extension in **System Preferences → Security & Privacy**.
6. AnyConnect will appear in the menu bar after installation.

### 3.3 Linux (Ubuntu) Installation

```bash
# Install dependencies
sudo apt update && sudo apt install -y libpangox-1.0-0 libgtk2.0-0

# Download the AnyConnect Linux installer from vpn.karansystems.in
# Run the installer
sudo ./anyconnect-linux64-<version>-predeploy-k9.sh

# Start the VPN UI
/opt/cisco/anyconnect/bin/vpnui &
```

### 3.4 Mobile (iOS / Android)

1. Install **Cisco AnyConnect** from the App Store or Google Play Store.
2. Open the app → Tap **"+" (Add Connection)**.
3. Server Address: `vpn.karansystems.in`
4. Save the connection and log in with Karan credentials + MFA.

---

## 4. Connecting to the Karan VPN

### 4.1 Initial Connection

1. Open **Cisco AnyConnect** from your taskbar/menu bar.
2. In the server field, enter: `vpn.karansystems.in`
3. Click **Connect**.
4. Enter your **Karan Employee ID** (e.g., `emp101`) and **network password**.
5. An MFA push notification will be sent to your registered **Microsoft Authenticator** app.
6. Approve the push notification within 60 seconds.
7. You are now connected. The AnyConnect icon will show a lock icon (🔒) in your taskbar.

### 4.2 VPN Groups

During login, you may be asked to select a group. Select the appropriate group:

| Group Name        | Purpose                                             |
|-------------------|-----------------------------------------------------|
| `Karan-Employee`    | Standard employee access — internal apps, shared drives |
| `Karan-Developer`   | Additional access to dev/test servers, CI/CD tools  |
| `Karan-Admin`       | IT Admin access — network, server management        |
| `Karan-Vendor`      | Restricted access for vendors and contractors       |

> Default group for most employees: **Karan-Employee**

---

## 5. Disconnecting from VPN

1. Click the AnyConnect icon in the taskbar.
2. Click **Disconnect**.
3. Always disconnect from VPN when not working to free up bandwidth and network resources.

---

## 6. Split Tunneling Policy

Karan Systems uses **Split Tunneling**:
- **Corporate traffic** (internal apps, file shares, HRMS) goes through the VPN tunnel.
- **Internet traffic** (browsing, streaming) bypasses the VPN.
- This ensures optimal performance while maintaining security for company data.

> Note: Certain high-risk internet categories (gambling, malware domains) are blocked by Karan's DNS security layer regardless of VPN status.

---

## 7. Troubleshooting VPN Issues

### 7.1 Cannot Connect to VPN Server

| Symptom                           | Action                                              |
|-----------------------------------|-----------------------------------------------------|
| "Unable to contact server"        | Check internet connectivity; try a different network |
| "Certificate error"               | Ensure system date/time is correct                  |
| VPN loads but internal sites fail | Restart AnyConnect; flush DNS: `ipconfig /flushdns` |
| MFA push not received             | Check phone internet; retry push; use OTP instead   |

### 7.2 VPN Disconnecting Frequently

- Ensure your internet connection is stable (try wired instead of Wi-Fi).
- Disable power-saving mode on your network adapter:
  - Windows: Device Manager → Network Adapters → Properties → Power Management → Uncheck "Allow computer to turn off this device."
- Update Cisco AnyConnect to the latest version from `vpn.karansystems.in`.

### 7.3 VPN Connected but Cannot Access Resources

- Ensure you selected the correct VPN group (see Section 4.2).
- Verify access permissions: some resources require additional group membership.
- Submit an access request if you receive a 403/Permission Denied error (see KB Article 003).

### 7.4 Error: "VPN Establishment Capability Prohibited"

This error occurs on non-compliant devices. Ensure:
- Your device is enrolled in **Microsoft Intune** (MDM).
- Required security patches are installed.
- Contact IT Helpdesk if device compliance status is unclear.

---

## 8. VPN for Vendors and Contractors

Vendors/Contractors require a separate VPN access provisioning:

1. The Karan employee sponsoring the vendor submits a **Vendor VPN Access Request** on `helpdesk.karansystems.in`.
2. Required: Vendor name, contact email, purpose, access duration.
3. Approval: Sponsoring employee's manager + IT Security Team.
4. Processing Time: 2–3 business days.
5. Vendor receives credentials and setup guide via email.
6. Vendor access is restricted to the `Karan-Vendor` group (limited access).

---

## 9. VPN Usage Policy

- VPN should **only be used for work purposes**.
- Sharing VPN credentials is **strictly prohibited** and is a security policy violation.
- Any suspicious activity on the VPN will be investigated by the IT Security team.
- VPN logs are retained for **90 days** for security audit purposes.

---

## 10. Related Articles

- KB Article 002 — Password Reset Process
- KB Article 003 — Access Request Process
- KB Article 005 — Email Access Issue

---

*For VPN support, contact IT Infrastructure: `infra-support@karansystems.in` | Ext. 2100*

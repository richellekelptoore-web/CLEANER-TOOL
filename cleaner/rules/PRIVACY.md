# Privacy Policy

**Last Updated:** August 15, 2024  
**Effective Date:** August 15, 2024

## 1. Introduction

Memory Clearer ("Software") is committed to protecting your privacy. This Privacy Policy explains what data we collect, how we use it, and your rights regarding your information.

## 2. Data Collection Philosophy

### ✅ What We DO NOT Do
- 🚫 Collect personal information
- 🚫 Track user behavior or usage patterns
- 🚫 Send telemetry or analytics data
- 🚫 Create user accounts or profiles
- 🚫 Store usage history externally
- 🚫 Share data with third parties
- 🚫 Require internet connection for core functionality
- 🚫 Monitor file contents during cleanup

### ✅ What We DO Do
- ✅ Store configuration locally in `config.ini`
- ✅ Create activity logs in `clear/logs/`
- ✅ Use system memory information for cleanup operations
- ✅ Operate entirely on your machine

## 3. Local Data Storage

### 3.1 Configuration Data

**Location:** `config.ini`

**Contains:**
- Memory threshold settings
- Cleanup preferences
- Monitoring intervals
- Log level settings

**Retention:** Stored locally on your machine until deleted by you

**Access:** Only accessible to users with local file access

### 3.2 Activity Logs

**Location:** `clear/logs/memory_clearer.log`

**Contains:**
- Cleanup operations performed
- Memory statistics over time
- Error messages
- Timestamps of activities

**Retention:** Kept for 7-30 days (configurable)

**Access:** Local only, never transmitted

### 3.3 Temporary Files

**Location:** `clear/cache/`, System temp directories

**Contains:**
- Temporary cleanup metadata
- Runtime cache data
- Session information

**Retention:** Automatically cleaned based on configuration

**Access:** Local access only

## 4. Information We Process

### 4.1 System Information

The Software accesses and processes:
- Total system memory
- Used memory
- Available memory
- CPU usage percentage
- Temporary file locations
- Cache directory contents

**Use:** Only for cleanup and monitoring purposes  
**Storage:** Never stored externally  
**Retention:** Memory values updated in real-time, historical data kept locally only

### 4.2 File System Access

The Software may access:
- Windows temp directories (`%TEMP%`, `%LOCALAPPDATA%\Temp`)
- Linux temp directories (`/tmp`, `/var/tmp`)
- macOS temp directories (`/tmp`, `/var/tmp`)
- Browser cache directories
- User-specified cleanup paths

**Use:** To identify and clean unnecessary files  
**Content Inspection:** File names and sizes only, not contents  
**Deletion:** Only files matching safe cleanup patterns

## 5. Third-Party Dependencies

The Software uses these open-source libraries:

### 5.1 psutil
- **License:** BSD
- **Data Access:** System metrics, process information
- **Privacy:** No external data transmission
- **Repository:** https://github.com/giampaolo/psutil

### 5.2 pywin32 (Windows only)
- **License:** Python Software Foundation
- **Data Access:** Windows API calls for system operations
- **Privacy:** No external data transmission
- **Repository:** https://github.com/pywin32/pywin32

### 5.3 tkinter (GUI)
- **License:** Python Software Foundation
- **Data Access:** User interface interaction
- **Privacy:** No external data transmission

## 6. Data Sharing

**Memory Clearer DOES NOT:**
- Share data with third parties
- Send data to remote servers
- Use cloud services
- Create backups in external locations
- Transmit any information over the internet

**Exception:** Initial package installation via pip may communicate with PyPI servers only for dependency download.

## 7. Data Security

### 7.1 Local Encryption

Configuration and log files are stored with your operating system's default file permissions. To enhance security:

```bash
# Windows: Right-click file > Properties > Advanced > Encrypt
# Linux: Use full-disk encryption or LUKS
# macOS: Enable FileVault
```

### 7.2 Access Control

Logs and configuration are readable by:
- The local user who ran the application
- System administrators (with elevated privileges)
- Anyone with file system access to your machine

### 7.3 Recommendations

- Keep your system passwords secure
- Use full-disk encryption
- Regularly review and delete old log files
- Configure Safe Mode (enabled by default)

## 8. Your Rights

### 8.1 Right to Access

You have the right to:
- Access all local data stored by the Software
- View contents of `config.ini` and log files
- Export or backup your configuration

### 8.2 Right to Delete

You have the right to:
- Delete configuration files
- Clear log files
- Uninstall the Software completely
- Remove all traces from your system

### 8.3 Data Portability

All data is stored in plain text formats:
- `config.ini` - Standard INI format
- `memory_clearer.log` - Plain text logs

You can easily transfer this data to another system or application.

## 9. Children's Privacy

Memory Clearer is not intended for children under 13. We do not knowingly collect data from children. If you believe a child has provided information, please contact us immediately.

## 10. International Compliance

### 10.1 GDPR (European Union)

Memory Clearer complies with GDPR because:
- No personal data collection
- No data processing of personal information
- No data storage in external databases
- All processing is local and user-controlled

### 10.2 CCPA (California)

Memory Clearer complies with CCPA because:
- No sale of personal information
- No sharing of information with third parties
- Users have complete control of local data
- No tracking or profiling

### 10.3 Other Regulations

Memory Clearer is compliant with:
- HIPAA (no health information)
- FERPA (no educational records)
- COPPA (no children's data)
- LGPD (Brazil - no data transmission)

## 11. Log Retention Policy

### Default Settings
- Log files kept for 30 days
- Oldest logs automatically rotated
- Maximum log file size: 10 MB

### Recommended Settings
```ini
[Logging]
max_file_size = 10485760  # 10 MB
backup_count = 3          # Keep 3 old logs
```

### Manual Cleanup
```bash
# Delete logs older than 30 days
# Linux/Mac: find clear/logs -mtime +30 -delete
# Windows: Use File Explorer to manually delete old logs
```

## 12. Data Breach Notification

While Memory Clearer stores data locally and cannot transmit data:
- If your system is compromised, your logs may be exposed
- This is a local security issue, not a Software issue
- Ensure your system security is properly maintained
- Use encryption and access controls

## 13. Changes to Privacy Policy

We may update this Privacy Policy to reflect:
- Changes in regulations
- Updates to the Software
- Improvements in data protection

Changes will be noted with an updated "Last Updated" date. Continued use after changes constitutes acceptance.

## 14. Contact & Inquiries

For privacy-related questions:
- **GitHub Issues:** Submit via repository
- **Email:** [Contact email if applicable]
- **Documentation:** See [docs/](../docs/) folder

## 15. Policy Acknowledgment

By using Memory Clearer, you acknowledge that you have:
- Read this Privacy Policy
- Understood our data practices
- Accepted that local data is stored on your device
- Accept responsibility for securing your system

---

## Summary

**Memory Clearer is private-by-design:**
- ✅ No data collection
- ✅ No telemetry
- ✅ No external transmission
- ✅ No third-party sharing
- ✅ Complete local control

Your data stays on your machine. Period.

---

**Memory Clearer © 2024 - All Rights Reserved**

**License:** MIT License

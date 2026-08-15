# Security Policy

## Safe Mode

Memory Clearer runs in **Safe Mode by default**, which means:

- ✅ Never deletes system-critical files
- ✅ Only cleans user temp and cache directories
- ✅ Requires explicit permission to proceed
- ✅ Creates backup logs of all cleanup operations

## Enabling Safe Mode

Safe Mode is enabled by default in `config.ini`:

```ini
[Cleanup]
safe_mode = true
```

We **strongly recommend** keeping this enabled.

## Reporting Security Issues

If you discover a security vulnerability, **DO NOT** create a public GitHub issue.

Instead:
1. Email security details to your project maintainer
2. Include reproduction steps
3. Do not disclose publicly until a fix is available

## Security Best Practices

### For Users

1. **Run from trusted location**
   - Clone only from official repository
   - Verify file hashes if downloading releases

2. **Keep dependencies updated**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

3. **Review logs regularly**
   - Check `clear/logs/memory_clearer.log`
   - Verify only expected files were deleted

4. **Use Safe Mode**
   - Keep default settings
   - Don't disable protections without understanding risks

5. **Run with minimal privileges**
   - Don't use admin/sudo unless necessary
   - Use regular user account for normal operation

### For Developers

1. **Input validation**
   - Validate all config file entries
   - Sanitize file paths

2. **Error handling**
   - Never silently ignore cleanup failures
   - Log all operations with full details

3. **Testing**
   - Test edge cases and invalid inputs
   - Include security-focused tests

4. **Dependencies**
   - Review third-party packages
   - Keep dependencies minimal
   - Monitor for security advisories

## File Deletion Policy

Memory Clearer will ONLY delete from approved locations:

### Safe Locations (Always Safe)
- Windows: `%TEMP%`, `%LOCALAPPDATA%\Temp`
- Linux: `/tmp`, `/var/tmp`
- macOS: `/tmp`, `/var/tmp`
- Browser caches (Chrome, Firefox, Edge)

### Protected Locations (Never Deleted)
- System directories
- Program files
- User documents
- Desktop
- Home directory (except caches)

### Configurable Locations
- Set in `config.ini` under `[Paths]`
- User must explicitly enable
- Always logged before deletion

## Audit Trail

Every cleanup operation is logged:

```
2024-01-15 10:30:45 [INFO] Cleanup started
2024-01-15 10:30:46 [INFO] Deleted: C:\Windows\Temp\file1.tmp (1.2 MB)
2024-01-15 10:30:47 [INFO] Deleted: C:\Windows\Temp\file2.tmp (0.8 MB)
2024-01-15 10:30:48 [INFO] Cleanup completed: 2.0 MB freed
```

## Known Limitations

### False Positives
- May detect files that look like cache but are needed
- Use `exclude_dirs` in config to prevent deletion

### Permissions
- Cannot clean system-protected folders (by design)
- May need admin/sudo for some locations

### Edge Cases
- Open files cannot be cleaned
- Network drive support is limited
- Some antivirus software may interfere

## Version Security

| Version | Status | End of Support |
|---------|--------|-----------------|
| 2.0.x   | ✅ Active | 2025-01-15 |
| 1.0.x   | ⚠️ Maintenance | 2024-06-01 |

Update to latest version for security patches.

## Compliance

Memory Clearer:
- ✅ Does not collect personal data
- ✅ Does not send telemetry
- ✅ Does not require internet connection
- ✅ Open source for security auditing
- ✅ Compatible with GDPR, CCPA regulations

## Additional Resources

- [OWASP Security Guidelines](https://owasp.org/)
- [CWE Top 25](https://cwe.mitre.org/top25/)
- [Python Security Best Practices](https://python.readthedocs.io/en/latest/library/security_warnings.html)

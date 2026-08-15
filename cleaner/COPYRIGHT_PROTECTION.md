# Copyright Protection & Verification Guide

**Last Updated:** August 15, 2026

## Overview

Memory Clearer includes multiple copyright verification mechanisms to ensure users are running the official version with all security updates and proper licensing compliance.

## What Gets Checked?

### 1. Official Marker File (`.official_marker`)

**Location:** Root directory  
**Purpose:** Identifies official installations  
**Status:** ✅ Present in official distributions

**Check Points:**
- ✓ `run.bat` checks for this file on startup
- ✓ GUI (`memory_clearer.py`) verifies during launch
- ✓ CLI (`cli.py`) displays warning if missing

### 2. Copyright Notice File (`COPYRIGHT_NOTICE.txt`)

**Location:** Root directory  
**Purpose:** Required by MIT License  
**Status:** ✅ Included in all distributions

**Content:**
- MIT License terms
- Official repository information
- Copyright attribution
- User acknowledgment

### 3. License File (`LICENSE`)

**Location:** Root directory  
**Purpose:** MIT License terms  
**Status:** ✅ Included in all distributions

## Verification Process

### When Running `run.bat`

```batch
[0/7] Verifying installation source...

If .official_marker is MISSING:
⚠️  WARNING: UNOFFICIAL INSTALLATION DETECTED

If COPYRIGHT_NOTICE.txt is MISSING:
⚠️  WARNING: COPYRIGHT_NOTICE.txt missing
```

**User Must:**
- Acknowledge the warning
- Choose to continue or cancel
- Understand the risks

### When Starting GUI

```python
if not os.path.exists('.official_marker'):
    # Show warning dialog
    # Ask user to confirm continuation
    # Display recommendation to download official version
```

**Dialog Shows:**
- ⚠️ Unofficial installation warning
- Recommendation to use official version
- Legal notice about MIT License
- Option to continue or exit

### When Using CLI

```bash
python cli.py --status

⚠️  WARNING: UNOFFICIAL INSTALLATION DETECTED

This folder does not appear to be from the official source.

RECOMMENDED:
  • Clone from: https://github.com/[official-repo]
  • Install via pip: pip install memory-clearer
```

**New Commands:**
```bash
python cli.py --copyright    # Show copyright info
```

## Official vs Unofficial

### ✅ Official Installation

Signs you have the official version:
- ✓ `.official_marker` file present
- ✓ `COPYRIGHT_NOTICE.txt` included
- ✓ `LICENSE` file present
- ✓ All documentation files included
- ✓ Latest security updates
- ✓ Proper attributions everywhere
- ✓ No modifications to source

**Where to Get:**
```bash
# Clone from GitHub
git clone https://github.com/[official-repo]
cd memory-clearer

# Or install via pip
pip install memory-clearer

# Or download from official website
https://[official-website]
```

### ❌ Unofficial Installation

Warning signs of unofficial/copied version:
- ❌ Missing `.official_marker` file
- ❌ Missing `COPYRIGHT_NOTICE.txt`
- ❌ Missing `LICENSE` file
- ❌ Outdated files
- ❌ Source file modifications
- ❌ Removed copyright notices
- ❌ Unknown origin

**Risks:**
- ⚠️ Missing security patches
- ⚠️ Could contain malware
- ⚠️ Violates MIT License (if modified)
- ⚠️ No official support
- ⚠️ Outdated features

## Copyright Protection Locations

### run.bat (Startup Verification)
```batch
:: COPYRIGHT VERIFICATION
echo [0/6] Verifying installation source...

if not exist ".official_marker" (
    color 0E
    echo ⚠️  WARNING: UNOFFICIAL INSTALLATION DETECTED
    ...
)
```

### memory_clearer.py (GUI Verification)
```python
def check_official_installation():
    """Verify this is an official installation"""
    if not os.path.exists('.official_marker'):
        result = messagebox.showwarning(...)
```

### cli.py (CLI Verification)
```python
def check_official_installation():
    """Check if this is an official installation"""
    if not os.path.exists('.official_marker'):
        print("⚠️  WARNING: UNOFFICIAL INSTALLATION DETECTED")
```

### GUI Menu
```
Help → License & Copyright
```

Shows:
- Copyright notice
- License terms
- Official source information
- Verification instructions

## License Compliance

### MIT License Requires:

✅ **You MUST include:**
1. Copy of MIT License text
2. Copyright notice
3. List of significant changes (if modified)

❌ **You CANNOT:**
1. Remove copyright notices
2. Claim you wrote the software
3. Hold authors liable for damages
4. Use authors' names for endorsement

### If Redistributing:

```
Required files to include:
✓ LICENSE (full MIT text)
✓ COPYRIGHT_NOTICE.txt
✓ README.md with attribution
✓ CHANGELOG.md (if modified)
```

## Security Considerations

### Why These Checks Matter

1. **Authenticity:** Ensures you have official version
2. **Security:** Official version has latest patches
3. **Trust:** Verifies no unauthorized modifications
4. **Legal:** Maintains MIT License compliance
5. **Support:** Official version gets bug fixes

### What to Do If Warnings Appear

**Step 1: Identify Source**
```bash
# Check if cloned from GitHub
cd memory-clearer
git remote -v

# Should show: https://github.com/[official-repo]
```

**Step 2: Verify Files**
```bash
# Check for required files
ls -la COPYRIGHT_NOTICE.txt    # Must exist
ls -la LICENSE                  # Must exist
ls -la .official_marker         # Must exist
```

**Step 3: If Unofficial**
```bash
# Delete and reinstall
rm -rf memory-clearer
git clone https://github.com/[official-repo]
# Or
pip uninstall memory-clearer
pip install memory-clearer
```

**Step 4: Report Issue**
```bash
# If you found unauthorized copy
# Report to official repository
# GitHub Issues → Report Unauthorized Distribution
```

## For Developers

### Adding Official Marker

If creating official release:
```bash
# Create .official_marker file
echo "OFFICIAL_VERSION=2.0" > .official_marker
echo "RELEASE_DATE=2024-08-15" >> .official_marker
echo "LICENSE=MIT" >> .official_marker
```

### Updating Copyright

If modifying and redistributing:
```bash
# 1. Keep original copyright
# 2. Add your modifications notice
# 3. Include LICENSE file
# 4. Document changes in CHANGELOG.md
```

### Example Modified Distribution

```
Original: Copyright © 2024 Memory Clearer Contributors

Modified: 
Copyright © 2024 Memory Clearer Contributors
Modifications © 2024 Your Name/Organization
Licensed under MIT License
```

## Troubleshooting

### Q: Why am I getting copyright warnings?

**A:** 
- Your version is not from official source
- Files may be missing or modified
- Action: Get official version from GitHub

### Q: Can I modify the software?

**A:** 
- ✅ Yes, MIT License allows modifications
- ⚠️ Must include original copyright
- ⚠️ Must include LICENSE file
- ⚠️ Must document changes

### Q: Can I redistribute my modified version?

**A:** 
- ✅ Yes, MIT License allows redistribution
- ⚠️ Must follow all license requirements
- ⚠️ Must clearly mark as modified
- ⚠️ Must link to original project

### Q: How do I verify authenticity?

**A:** 
1. Check `.official_marker` exists
2. Verify `COPYRIGHT_NOTICE.txt` content
3. Confirm `LICENSE` file
4. Clone fresh from GitHub
5. Compare checksums with official release

## Contact & Reporting

### Report Unauthorized Distribution

If you find an unauthorized copy:

1. **GitHub Issues:** Report via official repository
2. **Email:** Contact maintainers
3. **Describe:**
   - Where you found it
   - How it differs from official
   - Whether it appears to have malware

### Get Official Version

```
GitHub: https://github.com/[official-repo]
Website: https://[official-website]
PyPI: https://pypi.org/project/memory-clearer/
```

---

**Remember:** Always verify the source before installing!

**Memory Clearer © 2024 - All Rights Reserved**

**License:** MIT License

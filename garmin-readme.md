# Garmin Connect Activity Downloader

A Python script to download all your activities from Garmin Connect, with support for date ranges, multiple file formats, and batch downloading.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
  - [macOS](#macos)
  - [Windows](#windows)
  - [Linux](#linux)
- [Usage](#usage)
  - [Basic Examples](#basic-examples)
  - [Command Line Options](#command-line-options)
- [File Formats](#file-formats)
- [Troubleshooting](#troubleshooting)

## Features

- 🔐 Secure login to Garmin Connect
- 📅 Download activities by date range
- 📁 Multiple file format support (GPX, TCX, FIT)
- 🚀 Batch download with progress tracking
- ⏭️ Skip already downloaded files
- 🎯 Limit downloads for testing
- 📊 Download summary statistics

## Installation

### macOS

#### Step 1: Install Python (if needed)

Check if Python 3 is installed:
```bash
python3 --version
```

If not installed, install via Homebrew:
```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python
```

#### Step 2: Set up Virtual Environment

Navigate to where you saved the script:
```bash
cd /path/to/your/script
```

Create and activate a virtual environment:
```bash
# Create virtual environment
python3 -m venv garmin_env

# Activate it
source garmin_env/bin/activate
```

You should see `(garmin_env)` in your terminal prompt.

#### Step 3: Install Dependencies

```bash
pip install garminconnect
```

#### Step 4: Run the Script

```bash
python garmindl.py -u your@email.com -f fit
```

**Important:** Each time you want to run the script, activate the virtual environment first:
```bash
source garmin_env/bin/activate
python garmindl.py -u your@email.com -f fit
```

When done, deactivate:
```bash
deactivate
```

### Windows

#### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important:** Check "Add Python to PATH" during installation

#### Step 2: Set up Virtual Environment

Open Command Prompt or PowerShell and navigate to your script location:
```cmd
cd C:\path\to\your\script
```

Create and activate virtual environment:
```cmd
# Create virtual environment
python -m venv garmin_env

# Activate it (Command Prompt)
garmin_env\Scripts\activate

# Or for PowerShell
garmin_env\Scripts\Activate.ps1
```

#### Step 3: Install Dependencies

```cmd
pip install garminconnect
```

#### Step 4: Run the Script

```cmd
python garmindl.py -u your@email.com -f fit
```

### Linux

#### Step 1: Install Python (if needed)

Most Linux distributions include Python 3. Verify:
```bash
python3 --version
```

If not installed:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-venv python3-pip

# Fedora
sudo dnf install python3 python3-pip

# Arch
sudo pacman -S python python-pip
```

#### Step 2: Set up Virtual Environment

```bash
cd /path/to/your/script

# Create virtual environment
python3 -m venv garmin_env

# Activate it
source garmin_env/bin/activate
```

#### Step 3: Install Dependencies

```bash
pip install garminconnect
```

#### Step 4: Run the Script

```bash
python garmindl.py -u your@email.com -f fit
```

## Usage

### Basic Examples

**Download last year's activities (default):**
```bash
python garmindl.py -u your@email.com
```

**Download FIT files:**
```bash
python garmindl.py -u your@email.com -f fit
```

**Download to specific folder:**
```bash
python garmindl.py -u your@email.com -o ./my_activities
```

**Download specific date range:**
```bash
python garmindl.py -u your@email.com -s 2020-01-01 -e 2024-12-31
```

**Download all activities (entire history):**
```bash
python garmindl.py -u your@email.com -f fit -s 2010-01-01
```

**Test with limited downloads:**
```bash
python garmindl.py -u your@email.com -f fit -l 5
```

**Complete example with all options:**
```bash
python garmindl.py -u your@email.com -p yourpassword -o ./garmin_fit_files -s 2020-01-01 -e 2024-12-31 -f fit -l 100
```

### Command Line Options

| Option | Short | Description | Example |
|--------|-------|-------------|---------|
| `--username` | `-u` | **Required.** Your Garmin Connect email | `-u john@example.com` |
| `--password` | `-p` | Your Garmin password (will prompt if omitted) | `-p mypassword` |
| `--output` | `-o` | Output directory for downloads | `-o ./activities` |
| `--start-date` | `-s` | Start date (YYYY-MM-DD) | `-s 2020-01-01` |
| `--end-date` | `-e` | End date (YYYY-MM-DD) | `-e 2024-12-31` |
| `--format` | `-f` | File format (gpx, tcx, fit, original) | `-f fit` |
| `--limit` | `-l` | Max number of activities to download | `-l 10` |

#### Option Details

**`--username` / `-u`** (Required)
- Your Garmin Connect login email address
- Example: `-u myemail@gmail.com`

**`--password` / `-p`** (Optional)
- Your Garmin Connect password
- If omitted, you'll be prompted to enter it securely (recommended)
- Example: `-p MySecurePass123`

**`--output` / `-o`** (Optional)
- Directory where files will be saved
- Default: `./garmin_activities`
- Directory will be created if it doesn't exist
- Example: `-o ~/Documents/Garmin`

**`--start-date` / `-s`** (Optional)
- Beginning of date range for activities
- Format: YYYY-MM-DD
- Default: One year ago from today
- Example: `-s 2020-01-01`

**`--end-date` / `-e`** (Optional)
- End of date range for activities
- Format: YYYY-MM-DD
- Default: Today
- Example: `-e 2024-12-31`

**`--format` / `-f`** (Optional)
- File format to download
- Choices: `gpx`, `tcx`, `fit`, `original`
- Default: `gpx`
- `fit` is recommended for most training platforms
- Example: `-f fit`

**`--limit` / `-l`** (Optional)
- Maximum number of activities to download
- Useful for testing before downloading entire history
- Downloads most recent activities first
- Example: `-l 5`

## File Formats

### GPX (GPS Exchange Format)
- **Best for:** General GPS data, mapping applications
- **Compatible with:** Most fitness apps, Google Earth, Strava
- **File extension:** `.gpx`

### TCX (Training Center XML)
- **Best for:** Training data with heart rate, cadence
- **Compatible with:** TrainingPeaks, Golden Cheetah
- **File extension:** `.tcx`

### FIT (Flexible and Interoperable Data Transfer)
- **Best for:** Complete activity data from Garmin devices
- **Compatible with:** intervals.icu, TrainingPeaks, Garmin Connect
- **Contains:** All sensor data, laps, HR zones, power, etc.
- **File extension:** `.fit`
- **Recommended for most users**

### Original
- **Best for:** Getting the exact file from your device
- **Note:** May be compressed (ZIP format)
- **File extension:** Varies

## File Naming Convention

Downloaded files are named with the following pattern:
```
YYYYMMDD_ActivityID_Activity_Name.extension
```

Examples:
- `20241021_12345678_Morning_Run.fit`
- `20230615_87654321_Evening_Ride.gpx`
- `20220810_11223344_Lunch_Swim.tcx`

## Troubleshooting

### "externally-managed-environment" Error

This is a security feature in newer Python versions. Solution: Use a virtual environment (see installation instructions above).

### "garminconnect not found" Error

Make sure you've:
1. Activated your virtual environment: `source garmin_env/bin/activate`
2. Installed the package: `pip install garminconnect`

### Authentication Failed

Double-check your:
- Username (email address)
- Password
- Internet connection

If using 2-factor authentication, you may need to generate an app-specific password in Garmin Connect settings.

### FIT Files Won't Upload to intervals.icu

The script now properly extracts FIT files from ZIP archives. If you downloaded files before this fix, re-download them with:
```bash
python garmindl.py -u your@email.com -f fit
```

### "No activities found"

- Check your date range with `-s` and `-e`
- Verify activities exist in Garmin Connect for that period
- Try expanding the date range

### Script Runs But No Files Downloaded

- Check if files already exist (script skips existing files)
- Verify the output directory path
- Check file permissions on the output directory

### Download Limit Reached

Garmin may rate-limit requests. If downloads stop:
- Wait a few minutes and try again
- Use smaller date ranges
- Contact Garmin support if the issue persists

## Tips

- **Test first:** Use `-l 5` to download just 5 activities and verify everything works
- **Secure password:** Omit `-p` to be prompted for password (more secure than typing it in command)
- **Resume interrupted downloads:** The script automatically skips files that already exist
- **Regular backups:** Run periodically to keep your backup up-to-date
- **Date ranges:** For large histories, consider downloading in yearly chunks

## Support

For issues with:
- **This script:** Check the troubleshooting section above
- **Garmin Connect API:** Visit [Garmin Support](https://support.garmin.com)
- **Python/pip issues:** Consult Python documentation at [python.org](https://python.org)

## License

This script is provided as-is for personal use. Garmin Connect is a trademark of Garmin Ltd.
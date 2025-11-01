#!/usr/bin/env python3
"""
Garmin Connect Activity Downloader
Downloads activities from Garmin Connect account with date range filtering
"""

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
import argparse
from getpass import getpass

try:
    from garminconnect import Garmin, GarminConnectAuthenticationError
except ImportError:
    print("Error: garminconnect library not found.")
    print("Please install it with: pip install garminconnect")
    sys.exit(1)


def parse_date(date_string):
    """Parse date string in YYYY-MM-DD format"""
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: {date_string}. Use YYYY-MM-DD")


def download_activities(username, password, output_dir, start_date=None, end_date=None, file_format="gpx", limit=None):
    """
    Download activities from Garmin Connect
    
    Args:
        username: Garmin Connect username (email)
        password: Garmin Connect password
        output_dir: Directory to save downloaded files
        start_date: Start date for activity range (datetime object)
        end_date: End date for activity range (datetime object)
        file_format: File format to download (gpx, tcx, fit, or original)
        limit: Maximum number of activities to download (None for all)
    """
    
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    print(f"Logging into Garmin Connect as {username}...")
    
    try:
        # Initialize Garmin client and login
        client = Garmin(username, password)
        client.login()
        print("Login successful!\n")
        
    except GarminConnectAuthenticationError as e:
        print(f"Authentication failed: {e}")
        print("Please check your username and password.")
        return
    except Exception as e:
        print(f"Login error: {e}")
        return
    
    # Set default date range if not provided
    if end_date is None:
        end_date = datetime.now()
    if start_date is None:
        start_date = end_date - timedelta(days=365)  # Default to last year
    
    print(f"Fetching activities from {start_date.date()} to {end_date.date()}...")
    
    try:
        # Get activities list
        activities = client.get_activities_by_date(
            start_date.strftime("%Y-%m-%d"),
            end_date.strftime("%Y-%m-%d")
        )
        
        if not activities:
            print("No activities found in the specified date range.")
            return
        
        print(f"Found {len(activities)} activities to download.\n")
        
        # Apply limit if specified
        if limit and limit < len(activities):
            activities = activities[:limit]
            print(f"Limiting download to {limit} activities.\n")
        
        downloaded = 0
        skipped = 0
        errors = 0
        
        for i, activity in enumerate(activities, 1):
            activity_id = activity['activityId']
            activity_name = activity.get('activityName', 'Unnamed')
            activity_date = activity.get('startTimeLocal', 'Unknown')
            activity_type = activity.get('activityType', {}).get('typeKey', 'activity')
            
            # Create filename
            # Clean the activity name for filename
            safe_name = "".join(c for c in activity_name if c.isalnum() or c in (' ', '-', '_')).strip()
            safe_name = safe_name.replace(' ', '_')
            
            # Parse date for filename
            try:
                date_obj = datetime.strptime(activity_date[:10], "%Y-%m-%d")
                date_str = date_obj.strftime("%Y%m%d")
            except:
                date_str = "unknown_date"
            
            filename = f"{date_str}_{activity_id}_{safe_name}.{file_format}"
            filepath = os.path.join(output_dir, filename)
            
            # Skip if file already exists
            if os.path.exists(filepath):
                print(f"[{i}/{len(activities)}] Skipping (already exists): {filename}")
                skipped += 1
                continue
            
            try:
                print(f"[{i}/{len(activities)}] Downloading: {activity_name} ({activity_date[:10]})...")
                
                # Download activity in specified format
                if file_format.lower() == "gpx":
                    data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.GPX)
                elif file_format.lower() == "tcx":
                    data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.TCX)
                elif file_format.lower() == "fit":
                    # For FIT files, try to get the original/zip format and extract
                    zip_data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.ORIGINAL)
                    
                    # Check if it's a ZIP file
                    if zip_data[:2] == b'PK':  # ZIP file signature
                        import zipfile
                        import io
                        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_ref:
                            # Find the .fit file in the zip
                            fit_files = [f for f in zip_ref.namelist() if f.lower().endswith('.fit')]
                            if fit_files:
                                data = zip_ref.read(fit_files[0])
                            else:
                                print(f"    ⚠ No FIT file found in archive, saving as-is")
                                data = zip_data
                    else:
                        # Already a FIT file
                        data = zip_data
                else:
                    data = client.download_activity(activity_id, dl_fmt=client.ActivityDownloadFormat.ORIGINAL)
                
                # Save to file
                with open(filepath, 'wb') as f:
                    f.write(data)
                
                downloaded += 1
                print(f"    ✓ Saved to: {filename}")
                
            except Exception as e:
                print(f"    ✗ Error downloading activity {activity_id}: {e}")
                errors += 1
        
        print(f"\n{'='*60}")
        print(f"Download Summary:")
        print(f"  Total activities: {len(activities)}")
        print(f"  Successfully downloaded: {downloaded}")
        print(f"  Skipped (already exist): {skipped}")
        print(f"  Errors: {errors}")
        print(f"  Output directory: {os.path.abspath(output_dir)}")
        print(f"{'='*60}")
        
    except Exception as e:
        print(f"Error fetching activities: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Download activities from Garmin Connect",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download all activities from last year to current directory
  python garmin_downloader.py -u your@email.com
  
  # Download activities to specific folder
  python garmin_downloader.py -u your@email.com -o ./garmin_activities
  
  # Download activities within date range
  python garmin_downloader.py -u your@email.com -s 2024-01-01 -e 2024-12-31
  
  # Download in TCX format instead of GPX
  python garmin_downloader.py -u your@email.com -f tcx
        """
    )
    
    parser.add_argument('-u', '--username', required=True, help='Garmin Connect username (email)')
    parser.add_argument('-p', '--password', help='Garmin Connect password (will prompt if not provided)')
    parser.add_argument('-o', '--output', default='./garmin_activities', 
                        help='Output directory for downloaded files (default: ./garmin_activities)')
    parser.add_argument('-s', '--start-date', type=parse_date,
                        help='Start date for activities (YYYY-MM-DD format)')
    parser.add_argument('-e', '--end-date', type=parse_date,
                        help='End date for activities (YYYY-MM-DD format)')
    parser.add_argument('-f', '--format', default='gpx', choices=['gpx', 'tcx', 'fit', 'original'],
                        help='File format to download (default: gpx)')
    parser.add_argument('-l', '--limit', type=int,
                        help='Maximum number of activities to download (useful for testing)')
    
    args = parser.parse_args()
    
    # Get password securely if not provided
    password = args.password
    if not password:
        password = getpass(f"Enter password for {args.username}: ")
    
    # Download activities
    download_activities(
        username=args.username,
        password=password,
        output_dir=args.output,
        start_date=args.start_date,
        end_date=args.end_date,
        file_format=args.format,
        limit=args.limit
    )


if __name__ == "__main__":
    main()
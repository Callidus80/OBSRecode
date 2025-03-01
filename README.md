OBSRecode Help File
1. Introduction
Overview of the Software
OBSRecode is a graphical user interface (GUI) tool designed to simplify the re-encoding of OBS (Open Broadcaster Software) video recordings using HandbrakeCLI. It allows users to batch process video files (.mkv, .mp4, .mov) from a specified source directory into a more efficient format, leveraging NVIDIA's NVenc AV1 encoder for high-quality compression.

Purpose and Key Features
Purpose: To streamline the process of re-encoding OBS recordings, reducing file size while maintaining quality, without requiring manual command-line usage of HandbrakeCLI.
Key Features:
Batch processing of video files based on filename prefixes or all videos in a directory.
Configurable bitrate for output files.
Renames re-encoded files with an "RE " prefix for clarity.
Options to overwrite existing files, delete original files, and enable debug logging.
Real-time progress tracking with a progress bar and detailed log output.
User-friendly settings interface stored in a JSON file.
System Requirements
Operating System: Windows 10 or 11.
Hardware:
NVIDIA GPU supporting NVenc (e.g., GTX 16-series or newer, RTX series recommended for AV1 encoding).
Minimum 4GB RAM (8GB+ recommended for smooth operation).
Disk space dependent on video file sizes.
Dependencies:
Python 3.6 or higher (available from python.org).
HandbrakeCLI installed and accessible (download from handbrake.fr).
tkinter (included with standard Python installation; verify with python -m tkinter).
2. Installation & Setup
How to Download and Install the Application
Download:
Obtain the script (OBSRecode.py) from the GitHub repository: https://github.com/Callidus80/OBSRecode.
Install Python:
Download and install Python from python.org.
Ensure "Add Python to PATH" is checked during installation.
Install HandbrakeCLI:
Download HandbrakeCLI from handbrake.fr.
Install it to a known location (default: C:\Program Files\HandBrake\HandBrakeCLI.exe).
Run the Application:
Place OBSRecode.py in your desired directory (e.g., E:\Recorded Gaming).
Open Command Prompt, navigate to the directory, and run:
text
Wrap
Copy
python OBSRecode.py
Initial Configuration
On first run, OBSRecode creates a settings file at C:\Users\<Username>\AppData\Roaming\OBSRecode\OBSRecodeSettings.json.
Open the "Settings" menu to configure:
HandbrakeCLI Executable: Path to HandBrakeCLI.exe (e.g., C:\Program Files\HandBrake\HandBrakeCLI.exe).
Source Directory: Where OBS recordings are stored (e.g., E:\Recorded Gaming).
Output Directory: Where re-encoded files will be saved (e.g., E:\Reencoded Videos).
Filename starts with: Optional prefix to filter files (e.g., "OBS"; leave blank for all video files).
Bitrate (kbps): Optional output bitrate, defaults to 6000 kbps (e.g., set to 8000 for higher quality).
Click "Save" to store settings.
Troubleshooting Installation Issues
Python Not Found: Ensure Python is added to PATH; restart Command Prompt.
HandbrakeCLI Not Found: Verify the path in settings matches the installed location.
Syntax Error: Ensure the script file is not corrupted; re-download from GitHub.
3. User Interface (UI) Overview
Explanation of the Main Interface
Menu Bar:
"Settings" > "Configure Settings": Opens the settings window.
Main Window:
Header: "OBSRecode" in electric blue.
Status Labels:
"Settings loaded successfully" (green) or "Settings not set or invalid" (red).
"Files found for processing: X" (shows count of eligible video files).
"X of Y processed" (progress update).
"HandbrakeCLI found at: [path]" (green) or "not found" (red).
Progress Bar: Visual progress indicator.
File List: Shows files being processed with status icons (⌛ awaiting, ▶ processing, ✓ completed).
Buttons: "Start", "Cancel", "Processing" (completion), "Exit".
Tick Boxes: "Debug", "Automatically Overwrite", "Delete Original Files", "Write to Logfile".
Log Area: Displays processing logs.
Screenshots or Diagrams
(Note: Placeholder for actual screenshots/diagrams—consider adding these to the GitHub repo.)

Main Window: Displays all elements listed, with a sample file list (e.g., "⌛ OBS_Game1.mkv") and log output.
Settings Window: Shows input fields (e.g., "HandbrakeCLI Executable", "Bitrate (kbps)") and save/close buttons.
Navigation Instructions
Click "Settings" > "Configure Settings" to adjust options.
Use "Start" to begin processing, "Cancel" to stop, and "Exit" to close (after cancelling if processing).
Tick boxes toggle options instantly, saved to OBSRecodeSettings.json.
4. Core Functionality & Features
Step-by-Step Guide for Primary Functions
Re-encoding OBS Recordings
Configure Settings:
Open "Settings" > "Configure Settings".
Set "HandbrakeCLI Executable" (e.g., C:\Program Files\HandBrake\HandBrakeCLI.exe).
Set "Source Directory" (e.g., E:\Recorded Gaming).
Set "Output Directory" (e.g., E:\Reencoded Videos).
Optionally set "Filename starts with" (e.g., "OBS") or leave blank for all videos.
Optionally set "Bitrate (kbps)" (e.g., 8000) or leave as 6000.
Click "Save".
Start Processing:
Verify "Files found for processing" shows the correct count.
Click "Start".
If "Filename starts with" is blank, confirm the "Process All Files" prompt with "Yes".
Monitor Progress:
Watch the progress bar and file list updates (e.g., "▶ OBS_Game1.mkv - Processing").
Logs appear in the text area (enable "Debug" for detailed output).
Completion:
"Processing" button turns to "COMPLETED - Click to Close" (green) or "Process Cancelled - Click to Close" (red).
Re-encoded files are prefixed with "RE " (e.g., RE OBS_Game1.mkv).
Click to close when done.
Explanation of Settings and Options
HandbrakeCLI Executable: Path to HandbrakeCLI; must exist.
Source Directory: Directory containing .mkv, .mp4, .mov files to process.
Filename starts with: Filters files by prefix; blank processes all video files in the source directory.
Output Directory: Where re-encoded files (prefixed "RE ") are saved.
Bitrate (kbps): Output bitrate; defaults to 6000 kbps if unset.
Debug: Enables detailed logging in the GUI and log file.
Automatically Overwrite: Skips overwrite confirmation if ticked.
Delete Original Files: Deletes source files after successful encoding if ticked.
Write to Logfile: Saves logs to reencode_log.txt in the output directory.
Example Workflows
Re-encode Specific OBS Files:
In OBS, go to File > Settings > Advanced > Filename Formatting, set to "OBS%CCYY-%MM-%DD %hh-%mm-%ss" (e.g., outputs OBS2025-03-01 12-00-00.mkv).
In OBSRecode, set "Filename starts with" to "OBS", source to E:\Recordings, output to E:\Compressed, bitrate to 4000.
Start processing; only files starting with "OBS" (e.g., OBS2025-03-01 12-00-00.mkv) are re-encoded to RE OBS2025-03-01 12-00-00.mkv.
Compress All Videos:
Leave "Filename starts with" blank, set source to E:\Recordings, output to E:\Compressed.
Confirm processing all files; all .mkv, .mp4, .mov files (e.g., Game1.mkv) are re-encoded to RE Game1.mkv.
5. Troubleshooting & FAQs
Common Error Messages and Solutions
"HandbrakeCLI not found at: [path]": Verify the path in settings; reinstall HandbrakeCLI if missing.
"Settings not set or invalid": Configure all required fields in "Settings" and save.
"Bitrate must be a valid integer": Ensure "Bitrate (kbps)" is a number (e.g., 6000, not "6000kbps").
"No video files found": Check source directory for .mkv, .mp4, or .mov files matching the prefix (if set).
Performance Optimization Tips
Use a lower bitrate (e.g., 4000 kbps) for smaller files, balancing quality and size.
Enable "Automatically Overwrite" to skip prompts for faster batch processing.
Run on an SSD for quicker file access.
Contact/Support Information
Support: Submit issues or questions via the GitHub repository: https://github.com/Callidus80/OBSRecode.
Bug Reports: Include logs (enable "Debug" and "Write to Logfile") when reporting issues on GitHub.
6. Shortcuts & Advanced Features
Keyboard Shortcuts or Hotkeys
None implemented (GUI relies on mouse interaction).
Advanced Settings and Custom Configurations
Edit OBSRecodeSettings.json in C:\Users\<Username>\AppData\Roaming\OBSRecode for manual tweaks (e.g., adjust bitrate).
Modify reencode_file in OBSRecode.py for custom HandbrakeCLI options (requires Python knowledge).
API or Automation Features
None; OBSRecode is a standalone GUI application.
7. Legal & Licensing Information
Terms of Use and Privacy Policy
OBSRecode is provided "as is" under the GNU General Public License v3 (GPLv3).
No user data is collected beyond settings in OBSRecodeSettings.json and optional logs in the output directory.
Open-Source or Third-Party Software Acknowledgments
Python: PSF License (python.org).
HandbrakeCLI: GNU GPL v2 (handbrake.fr).
tkinter: PSF License (part of Python).
OBSRecode: GNU GPL v3 (https://github.com/Callidus80/OBSRecode).

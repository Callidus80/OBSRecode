# OBSRecode
![OBSRecode Logo](https://github.com/user-attachments/assets/b916f309-9070-411b-8f17-263f9b8d083c)


OBSRecode is a Python-based GUI tool that simplifies re-encoding OBS (Open Broadcaster Software) video recordings using HandbrakeCLI. It leverages NVIDIA's NVenc AV1 encoder to batch process `.mkv`, `.mp4`, and `.mov` files, reducing file sizes while maintaining quality.

OBSRecode is an essential tool for archiving and storing OBS-recorded content, making it ideal for gamers, streamers, and creators who need to manage their footage efficiently. On-the-fly recordings in OBS often prioritize fast, GPU-efficient encoding to capture video in real-time, producing large file sizes that can overwhelm storage capacity. OBSRecode addresses this by re-encoding your recordings with HandbrakeCLI’s slower, more optimized presets, utilizing advanced compression like NVIDIA’s NVenc AV1 encoder after you're finished gaming. This significantly reduces file sizes for archiving and long-term storage purposes, while maintaining high-quality visuals. With its user-friendly GUI, OBSRecode simplifies the process, ensuring your most valued clips remain compact and preserved without cluttering your drives.

## Windows OS Only

## Overview

OBSRecode streamlines the re-encoding process for OBS recordings, eliminating the need for manual command-line usage. Key features include:

* Batch processing with optional filename prefix filtering (e.g., "OBS").
* Fire and forget. Option to auto shutdown OS once processing complete.
* Customizable bitrate settings.
* Automatic "RE " prefix for re-encoded files to distinguish them from originals.
* Real-time progress tracking and detailed logging.



# **Standalone executable available.**
Running OBSRecode as an Executable
1. Download: Get ([OBSRecode.exe](https://github.com/Callidus80/OBSRecode/blob/main/OBSRecode.exe)) from GitHub Releases.
2. Requirements: Install HandbrakeCLI ([Download](https://handbrake.fr/downloads2.php)) from handbrake.fr and note its path (e.g., C:\Program Files\HandBrake\HandBrakeCLI.exe).
3. Run: Double-click OBSRecode.exe, configure settings, and start processing.

 <br />
  <br />
   <br />
      <br />


## Manual Python Installation.
Not required if you are using **Standalone executable available** above.


### Prerequisites

* **OS:** Windows 10 or 11
* **Hardware:** NVIDIA GPU with NVenc support (e.g., GTX 16-series or newer)
* **Software:**

  - Python 3.6+ ([Download](https://www.python.org/downloads/))
  - HandbrakeCLI ([Download](https://handbrake.fr/downloads2.php))
 

### Steps

1. **Clone the Repository:**

```
git clone https://github.com/Callidus80/OBSRecode.git
cd OBSRecode
```
2. **Install Python:**
Ensure "Add Python to PATH" is checked during installation.
3. **Install HandbrakeCLI:**
Install to a known location (e.g., `C:\Program Files\HandBrake\HandBrakeCLI.exe`).
4. **Run OBSRecode:**

```
python OBSRecode.py
```

## Usage

<img width="425" alt="2025-03-01 17_26_34-OBSRecode" src="https://github.com/user-attachments/assets/4b364e4c-295c-45a1-9a62-c4cfc66cc2c3" />


### Initial Setup

On first run, a settings file is created at `C:\Users\<Username>\AppData\Roaming\OBSRecode\OBSRecodeSettings.json`.

1. Go to "Settings" > "Configure Settings":
2. Set:

  - **HandbrakeCLI Executable:** Path to `HandBrakeCLI.exe`.
  - **Source Directory:** Where OBS recordings are stored.
  - **Output Directory:** Where re-encoded files will be saved.
  - **Filename starts with:** Optional prefix (e.g., "OBS") or blank for all videos.
  - **Bitrate (kbps):** Optional, defaults to 6000 kbps.
3. Click "Save".
<img width="370" alt="2025-03-01 17_25_57-Settings" src="https://github.com/user-attachments/assets/98632a13-6d8a-4299-9292-4db55b53a9e1" />



### Re-encoding

1. Check "Files found for processing" count.
2. Click "Start".
3. Confirm "Process All Files" if no prefix is set.
4. Re-encoded files are prefixed with "RE " (e.g., `RE OBS_Game1.mkv`).

## Features

* **Batch Processing:** Re-encode multiple `.mkv`, `.mp4`, `.mov` files.
* **Filename Filtering:** Target files with a prefix (e.g., "OBS").
* **Re-encoding Indicator:** "RE " prefix on output files.
* **Configurable Bitrate:** Adjust compression quality (default: 6000 kbps).
* **Options:** Overwrite, delete originals, debug logging, and log file output.
* **Progress Tracking:** Real-time progress bar and logs.

## Configuration Tips

* **OBS Integration:** In OBS, set File > Settings > Advanced > Filename Formatting to "OBS%CCYY-%MM-%DD %hh-%mm-%ss" (e.g., `OBS2025-03-01 12-00-00.mkv`). Use "OBS" in "Filename starts with" to target these files.
* Screenshot below.
<img width="830" alt="2025-03-01 16_16_45-Settings" src="https://github.com/user-attachments/assets/632df914-d992-4d4b-86fb-9f488fba7c53" />

To target the files prefixed with OBS enter it here under Settings in OBSRecode

<img width="371" alt="2025-03-01 17_31_46-2025-03-01 17_25_49-OBSRecode png ‎- Photos" src="https://github.com/user-attachments/assets/8de5e95c-17fd-47cd-b85f-f974206ad4fc" />


* **Performance:** Lower bitrate (e.g., 4000 kbps) for smaller files; use an SSD for speed.

## Troubleshooting

* **"HandbrakeCLI not found":** Verify path in settings; reinstall if missing.
* **"Settings not set":** Fill required fields and save.
* **"No video files found":** Ensure source directory has `.mkv`, `.mp4`, or `.mov` files.

## Contributing

Report bugs or suggest features via [GitHub Issues](https://github.com/Callidus80/OBSRecode/issues).

If you would like to support my work: [Buy me a beer](https://www.paypal.com/donate/?hosted_button_id=KDGESDGHAJGLN).

## License

Default copyright laws apply.

### Acknowledgments

* **Python:** PSF License
* **HandbrakeCLI:** GNU GPL v2
* **tkinter:** PSF License

## Support

For help or bug reports, use [GitHub Issues](https://github.com/Callidus80/OBSRecode/issues).

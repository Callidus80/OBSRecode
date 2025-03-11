import os
import subprocess
import logging
from datetime import datetime
import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
import json
import webbrowser
import platform

# Define settings file location in AppData\Roaming\OBSRecode
SETTINGS_DIR = os.path.join(os.getenv('APPDATA'), 'OBSRecode')
os.makedirs(SETTINGS_DIR, exist_ok=True)
SETTINGS_FILE = os.path.join(SETTINGS_DIR, 'OBSRecodeSettings.json')
LOG_FILE = "reencode_log.txt"
VALID_EXTENSIONS = {".mkv", ".mp4", ".mov"}
PAYPAL_LINK = "https://www.paypal.com/donate/?hosted_button_id=KDGESDGHAJGLN"
HELP_LINK = "https://github.com/Callidus80/OBSRecode"

class OBSRecodeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OBSRecode")
        self.root.geometry("1070x500")
        self.root.minsize(500, 600)

        # Load and validate settings
        self.settings, self.settings_valid = self.load_and_validate_settings()

        # Toggle states with persistence from settings
        self.debug_mode = tk.BooleanVar(value=self.settings.get("debug_mode", False))
        self.auto_overwrite = tk.BooleanVar(value=self.settings.get("auto_overwrite", False))
        self.delete_original = tk.BooleanVar(value=self.settings.get("delete_original", True))
        self.write_logfile = tk.BooleanVar(value=self.settings.get("write_logfile", False))
        self.shutdown_after_completion = tk.BooleanVar(value=self.settings.get("shutdown_after_completion", False))

        # Setup menu
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        
        # Settings menu
        self.settings_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Settings", menu=self.settings_menu)
        self.settings_menu.add_command(label="Configure Settings", command=self.open_settings_window)
        
        # Support My Work menu
        self.support_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Support My Work", menu=self.support_menu)
        self.support_menu.add_command(label="Buy Me a Beer", command=self.open_support_window)

        # Help menu
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Documentation", command=lambda: webbrowser.open(HELP_LINK))

        # Header
        self.header_label = tk.Label(root, text="OBSRecode", font=("Helvetica", 14, "bold"), fg="#00B7EB")
        self.header_label.pack(pady=5)

        # Main frame for dynamic content
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(side=tk.TOP, fill="both", expand=True)

        # Note label for settings status
        self.note_label = tk.Label(self.main_frame, font=("Helvetica", 10, "bold"))
        self.update_note_label()
        self.note_label.pack(pady=5)

        # Files found frame
        self.files_found_frame = tk.Frame(self.main_frame)
        self.files_found_frame.pack(pady=5)
        self.files_found_label = tk.Label(self.files_found_frame, text="Files found for processing: 0")
        self.files_found_label.pack(side=tk.LEFT, padx=5)
        self.refresh_button = tk.Button(self.files_found_frame, text="Refresh", command=self.update_files_found)
        self.refresh_button.pack(side=tk.LEFT, padx=5)
        self.view_button = tk.Button(self.files_found_frame, text="View", command=self.view_files_to_process)
        self.view_button.pack(side=tk.LEFT, padx=5)
        self.update_files_found()

        # Progress label
        self.progress_label = tk.Label(self.main_frame, text="0 of 0 processed")
        self.progress_label.pack(pady=5)

        # HandbrakeCLI status label
        self.cli_status_label = tk.Label(self.main_frame, text="")
        self.update_cli_status()
        self.cli_status_label.pack(pady=5)

        # Progress bar
        self.progress = ttk.Progressbar(self.main_frame, length=1000, mode="determinate")
        self.progress.pack(pady=5)

        # File list frame
        self.file_frame = tk.Frame(self.main_frame)
        self.file_frame.pack(pady=5, fill="x")
        self.file_labels = {}

        # Button frame (above log area)
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(pady=5, fill="x")

        # Start button
        self.start_button = tk.Button(self.button_frame, text="Start", command=self.start_processing)
        self.start_button.pack(side=tk.LEFT, padx=5)

        # Cancel button
        self.cancel_button = tk.Button(self.button_frame, text="Cancel", command=self.cancel_processing, state="disabled")
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        # Close button (for processing completion)
        self.close_button = tk.Button(self.button_frame, text="Processing", state="disabled", command=self.close_gui)
        self.close_button.pack(side=tk.LEFT, padx=5)

        # Exit button
        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.close_gui)
        self.exit_button.pack(side=tk.LEFT, padx=5)

        # Options frame (below buttons)
        self.options_frame = tk.Frame(self.main_frame)
        self.options_frame.pack(pady=5, fill="x")

        # Debug tick box
        self.debug_check = tk.Checkbutton(self.options_frame, text="Debug", variable=self.debug_mode, command=self.toggle_debug)
        self.debug_check.pack(side=tk.LEFT, padx=5)

        # Automatically Overwrite tick box
        self.overwrite_check = tk.Checkbutton(self.options_frame, text="Automatically Overwrite", variable=self.auto_overwrite, command=self.save_options)
        self.overwrite_check.pack(side=tk.LEFT, padx=5)

        # Delete Original Files tick box
        self.delete_check = tk.Checkbutton(self.options_frame, text="Delete Original Files", variable=self.delete_original, command=self.save_options)
        self.delete_check.pack(side=tk.LEFT, padx=5)

        # Write to Logfile tick box
        self.logfile_check = tk.Checkbutton(self.options_frame, text="Write to Logfile", variable=self.write_logfile, command=self.toggle_logfile)
        self.logfile_check.pack(side=tk.LEFT, padx=5)

        # Shutdown After Completion tick box
        self.shutdown_check = tk.Checkbutton(self.options_frame, text="Shutdown PC After Completion", variable=self.shutdown_after_completion, command=self.save_options)
        self.shutdown_check.pack(side=tk.LEFT, padx=5)

        # Log text area
        self.log_text = scrolledtext.ScrolledText(self.main_frame, width=130, height=20)
        self.log_text.pack(pady=5, fill="x", expand=True)

        self.files_to_process = []
        self.total_files = 0
        self.processed_files = 0
        self.current_process = None
        self.cancel_flag = threading.Event()
        self.current_flashing_label = None
        self.flash_state = True
        self.is_processing = False
        self.settings_window = None
        self.support_window = None
        self.view_window = None  # Track view window instance
        self.logger = None  # Initialize logger as None

        # Initial logfile setup
        self.toggle_logfile()

    def load_and_validate_settings(self):
        defaults = {
            "source_dir": "",
            "search_text": "",
            "output_dir": "",
            "bitrate": 6000,
            "handbrake_cli_path": r"C:\Handbrake\HandBrakeCLI.exe",
            "debug_mode": False,
            "auto_overwrite": False,
            "delete_original": True,
            "write_logfile": False,
            "shutdown_after_completion": False
        }
        if not os.path.exists(SETTINGS_FILE):
            return defaults, False
        
        try:
            with open(SETTINGS_FILE, "r") as f:
                settings = json.load(f)
            required = ["source_dir", "output_dir", "handbrake_cli_path"]
            for key in required:
                if key not in settings or not settings[key]:
                    return defaults, False
            for key in ["search_text", "bitrate", "debug_mode", "auto_overwrite", "delete_original", "write_logfile", "shutdown_after_completion"]:
                if key not in settings:
                    settings[key] = defaults[key]
            return settings, True
        except (json.JSONDecodeError, Exception):
            return defaults, False

    def save_settings(self):
        with open(SETTINGS_FILE, "w") as f:
            json.dump(self.settings, f, indent=4)
        self.settings_valid = True
        self.update_note_label()
        self.update_cli_status()
        self.update_files_found()

    def save_options(self):
        self.settings["debug_mode"] = self.debug_mode.get()
        self.settings["auto_overwrite"] = self.auto_overwrite.get()
        self.settings["delete_original"] = self.delete_original.get()
        self.settings["write_logfile"] = self.write_logfile.get()
        self.settings["shutdown_after_completion"] = self.shutdown_after_completion.get()
        self.save_settings()

    def toggle_debug(self):
        self.save_options()
        self.log_message(f"Debug mode {'enabled' if self.debug_mode.get() else 'disabled'}.")

    def toggle_logfile(self):
        """Enable or disable logging to file based on write_logfile toggle."""
        self.save_options()
        if self.write_logfile.get() and self.settings_valid and self.settings["output_dir"]:
            # Enable logging to file
            log_path = os.path.normpath(os.path.join(self.settings["output_dir"], LOG_FILE))
            level = logging.DEBUG if self.debug_mode.get() else logging.INFO
            logging.basicConfig(
                filename=log_path,
                level=level,
                format="%(asctime)s - %(levelname)s - %(message)s"
            )
            self.logger = logging.getLogger()
            self.log_message("Logging to file enabled.")
        else:
            # Disable logging to file by setting a null handler
            if self.logger:
                self.logger.handlers = []  # Remove file handlers
                self.logger.addHandler(logging.NullHandler())  # Use null handler to prevent logging
            self.log_message("Logging to file disabled.")

    def update_note_label(self):
        if self.settings_valid:
            self.note_label.config(text="Settings loaded successfully", fg="green")
        else:
            self.note_label.config(text="Settings not set or invalid", fg="red")

    def update_cli_status(self):
        cli_path = self.settings.get("handbrake_cli_path", "")
        if cli_path and os.path.exists(cli_path):
            self.cli_status_label.config(text=f"HandbrakeCLI found at: {cli_path}", fg="green")
        else:
            self.cli_status_label.config(text=f"HandbrakeCLI not found at: {cli_path or 'Not set'}. Configure Settings.", fg="red")

    def update_files_found(self):
        """Recheck the source directory for files to process and update the label."""
        if not self.settings_valid or not self.settings["source_dir"]:
            self.files_found_label.config(text="Files found for processing: 0")
            self.files_to_process = []
            return
        
        if not os.path.exists(self.settings["source_dir"]):
            self.files_found_label.config(text="Files found for processing: 0 (Source directory not found)")
            self.files_to_process = []
            return

        search_text = self.settings["search_text"]
        if not search_text:
            video_files = [
                f for f in os.listdir(self.settings["source_dir"])
                if os.path.isfile(os.path.join(self.settings["source_dir"], f)) and
                os.path.splitext(f)[1].lower() in VALID_EXTENSIONS
            ]
        else:
            video_files = [
                f for f in os.listdir(self.settings["source_dir"])
                if f.startswith(search_text) and
                os.path.isfile(os.path.join(self.settings["source_dir"], f)) and
                os.path.splitext(f)[1].lower() in VALID_EXTENSIONS
            ]
        
        self.files_to_process = [os.path.normpath(os.path.join(self.settings["source_dir"], f)) for f in video_files]
        count = len(self.files_to_process)
        self.files_found_label.config(text=f"Files found for processing: {count}")
        self.log_message(f"Refreshed file list: {count} files found.", "DEBUG")

    def view_files_to_process(self):
        """Open a popup window showing all files to be processed."""
        if self.view_window and self.view_window.winfo_exists():
            self.view_window.lift()
            self.view_window.focus_force()
            return

        if not self.files_to_process:
            messagebox.showinfo("No Files", "No files found to process. Please check your settings and source directory.")
            return

        self.view_window = tk.Toplevel(self.root)
        self.view_window.title("Files to Process")
        self.view_window.geometry("600x400")
        self.view_window.minsize(600, 400)
        self.view_window.grab_set()

        # Header
        tk.Label(self.view_window, text="Files to be Processed", font=("Helvetica", 12, "bold")).pack(pady=5)

        # Scrolled text area for file list
        file_list_text = scrolledtext.ScrolledText(self.view_window, width=80, height=20)
        file_list_text.pack(pady=5, fill="both", expand=True)

        # Populate the file list
        for file_path in self.files_to_process:
            file_list_text.insert(tk.END, f"{file_path}\n")
        file_list_text.config(state="disabled")  # Make read-only

        # Close button
        tk.Button(self.view_window, text="Close", command=self.view_window.destroy).pack(pady=5)

    def open_settings_window(self):
        if self.is_processing:
            messagebox.showinfo("Processing", "Cannot configure settings while processing.")
            return

        if self.settings_window and self.settings_window.winfo_exists():
            self.settings_window.lift()
            self.settings_window.focus_force()
            return

        self.settings_window = tk.Toplevel(self.root)
        self.settings_window.title("Settings")
        self.settings_window.geometry("500x450")
        self.settings_window.minsize(500, 450)
        self.settings_window.grab_set()

        temp_settings = self.settings.copy()

        tk.Label(self.settings_window, text="* HandbrakeCLI Executable:", fg="red").pack(pady=2)
        cli_frame = tk.Frame(self.settings_window)
        cli_frame.pack(fill="x", pady=2)
        self.cli_entry = tk.Entry(cli_frame, width=50, fg="gray")
        cli_placeholder = r"C:\Handbrake\HandBrakeCLI.exe"
        self.cli_entry.insert(0, cli_placeholder if not temp_settings["handbrake_cli_path"] else temp_settings["handbrake_cli_path"])
        self.cli_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, cli_placeholder))
        self.cli_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, cli_placeholder))
        self.cli_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(cli_frame, text="Browse", command=lambda: self.browse_file(self.cli_entry, "*.exe")).pack(side=tk.LEFT)

        tk.Label(self.settings_window, text="* Source Directory:", fg="red").pack(pady=2)
        source_frame = tk.Frame(self.settings_window)
        source_frame.pack(fill="x", pady=2)
        self.source_entry = tk.Entry(source_frame, width=50, fg="gray")
        source_placeholder = r"E:\Recorded Gaming"
        self.source_entry.insert(0, source_placeholder if not temp_settings["source_dir"] else temp_settings["source_dir"])
        self.source_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, source_placeholder))
        self.source_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, source_placeholder))
        self.source_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(source_frame, text="Browse", command=lambda: self.browse_dir(self.source_entry, self.settings_window)).pack(side=tk.LEFT)

        tk.Label(self.settings_window, text="Filename starts with:").pack(pady=2)
        tk.Label(self.settings_window, text="Optional, searches for filenames starting with text string.").pack()
        tk.Label(self.settings_window, text="If not specified all video files (.mkv, .mp4, .mov) in source directory will be re-encoded.", fg="gray").pack()
        search_frame = tk.Frame(self.settings_window)
        search_frame.pack(fill="x", pady=2)
        self.search_entry = tk.Entry(search_frame, width=50, fg="gray")
        search_placeholder = "example OBS e.g: \"OBS Game Name.mkv\""
        self.search_entry.insert(0, search_placeholder if not temp_settings["search_text"] else temp_settings["search_text"])
        self.search_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, search_placeholder))
        self.search_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, search_placeholder))
        self.search_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(self.settings_window, text="* Output Directory:", fg="red").pack(pady=2)
        output_frame = tk.Frame(self.settings_window)
        output_frame.pack(fill="x", pady=2)
        self.output_entry = tk.Entry(output_frame, width=50, fg="gray")
        output_placeholder = r"E:\Recorded Gaming"
        self.output_entry.insert(0, output_placeholder if not temp_settings["output_dir"] else temp_settings["output_dir"])
        self.output_entry.bind("<FocusIn>", lambda event: self.clear_placeholder(event, output_placeholder))
        self.output_entry.bind("<FocusOut>", lambda event: self.add_placeholder(event, output_placeholder))
        self.output_entry.pack(side=tk.LEFT, padx=5)
        tk.Button(output_frame, text="Browse", command=lambda: self.browse_dir(self.output_entry, self.settings_window)).pack(side=tk.LEFT)

        tk.Label(self.settings_window, text="Bitrate (kbps):").pack(pady=2)
        tk.Label(self.settings_window, text="Optional, defaults to ~6000kbps ~230MB per 5 minutes", fg="gray").pack()
        bitrate_frame = tk.Frame(self.settings_window)
        bitrate_frame.pack(fill="x", pady=2)
        self.bitrate_entry = tk.Entry(bitrate_frame, width=50, fg="gray")
        self.bitrate_entry.insert(0, str(temp_settings["bitrate"]))
        self.bitrate_entry.pack(side=tk.LEFT, padx=5)

        button_frame = tk.Frame(self.settings_window)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Save", command=lambda: self.save_settings_from_window(self.settings_window)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Close", command=self.settings_window.destroy).pack(side=tk.LEFT, padx=5)

        legend_frame = tk.Frame(self.settings_window)
        legend_frame.pack(side=tk.BOTTOM, pady=5, fill="x")
        tk.Label(legend_frame, text="* = Required Field", fg="red").pack()

    def open_support_window(self):
        """Open a support window with a Buy Me a Beer explanation and PayPal link."""
        if self.support_window and self.support_window.winfo_exists():
            self.support_window.lift()
            self.support_window.focus_force()
            return

        self.support_window = tk.Toplevel(self.root)
        self.support_window.title("Support My Work")
        self.support_window.geometry("400x200")
        self.support_window.minsize(400, 200)
        self.support_window.grab_set()

        # Support message
        tk.Label(self.support_window, text="Support My Work", font=("Helvetica", 12, "bold")).pack(pady=10)
        tk.Label(self.support_window, text="If you find OBSRecode useful and want to support its development,", wraplength=350).pack()
        tk.Label(self.support_window, text="consider buying me a beer! Your support helps keep this project going.", wraplength=350).pack()

        # Button to PayPal
        tk.Button(self.support_window, text="Buy Me a Beer", command=lambda: webbrowser.open(PAYPAL_LINK)).pack(pady=10)
        
        # Close button
        tk.Button(self.support_window, text="Close", command=self.support_window.destroy).pack(pady=5)

    def clear_placeholder(self, event, placeholder):
        if event.widget.get() == placeholder:
            event.widget.delete(0, tk.END)
            event.widget.config(fg="black")

    def add_placeholder(self, event, placeholder):
        if not event.widget.get():
            event.widget.insert(0, placeholder)
            event.widget.config(fg="gray")

    def browse_dir(self, entry, window):
        dir_path = filedialog.askdirectory()
        if dir_path:
            entry.delete(0, tk.END)
            entry.insert(0, os.path.normpath(dir_path))
            entry.config(fg="black")
            window.lift()
            window.focus_force()

    def browse_file(self, entry, file_type):
        file_path = filedialog.askopenfilename(filetypes=[(f"{file_type} files", file_type)])
        if file_path:
            entry.delete(0, tk.END)
            entry.insert(0, os.path.normpath(file_path))
            entry.config(fg="black")
            if self.settings_window:
                self.settings_window.lift()
                self.settings_window.focus_force()

    def save_settings_from_window(self, window):
        cli_text = self.cli_entry.get()
        self.settings["handbrake_cli_path"] = os.path.normpath(cli_text) if cli_text else ""
        
        source_text = self.source_entry.get()
        self.settings["source_dir"] = os.path.normpath(source_text) if source_text else ""
        
        search_text = self.search_entry.get()
        search_placeholder = "example OBS e.g: \"OBS Game Name.mkv\""
        self.settings["search_text"] = search_text if search_text and search_text != search_placeholder else ""
        
        output_text = self.output_entry.get()
        self.settings["output_dir"] = os.path.normpath(output_text) if output_text else ""
        
        bitrate_text = self.bitrate_entry.get()
        try:
            self.settings["bitrate"] = int(bitrate_text) if bitrate_text else 6000
        except ValueError:
            messagebox.showerror("Error", "Bitrate must be a valid integer.")
            return
        
        if not self.settings["source_dir"] or not self.settings["output_dir"] or not self.settings["handbrake_cli_path"]:
            messagebox.showerror("Error", "HandbrakeCLI executable, source directory, and output directory are required.")
            return
        self.save_settings()
        self.toggle_logfile()  # Update logging state after saving settings
        self.log_message("Settings saved successfully.")
        window.destroy()

    def start_processing(self):
        if not self.settings_valid:
            messagebox.showerror("Error", "Please configure and save valid settings before starting.")
            return
        self.clear_gui()
        self.check_overwrites_and_start()

    def check_overwrites_and_start(self):
        search_text = self.settings["search_text"]
        if not search_text:
            self.files_to_process = [
                os.path.normpath(os.path.join(self.settings["source_dir"], f))
                for f in os.listdir(self.settings["source_dir"])
                if os.path.isfile(os.path.join(self.settings["source_dir"], f)) and
                os.path.splitext(f)[1].lower() in VALID_EXTENSIONS
            ]
            confirm_msg = "No 'Filename starts with' specified. All video files (.mkv, .mp4, .mov) in the source directory will be re-encoded.\nDo you want to proceed?"
            if not messagebox.askyesno("Confirm Processing All Files", confirm_msg):
                self.log_message("Processing cancelled by user.")
                return
        else:
            self.files_to_process = [
                os.path.normpath(os.path.join(self.settings["source_dir"], f))
                for f in os.listdir(self.settings["source_dir"])
                if f.startswith(search_text) and
                os.path.isfile(os.path.join(self.settings["source_dir"], f)) and
                os.path.splitext(f)[1].lower() in VALID_EXTENSIONS
            ]
        
        self.total_files = len(self.files_to_process)
        
        if self.total_files == 0:
            self.log_message(f"No video files (.mkv, .mp4, .mov) found in {self.settings['source_dir']} to process.", "WARNING")
            self.enable_close_button(cancelled=False)
            return

        if not self.auto_overwrite.get():
            existing_files = []
            for input_file in self.files_to_process:
                base_name = os.path.basename(input_file)
                output_file = os.path.normpath(os.path.join(self.settings["output_dir"], f"RE {base_name}"))
                if os.path.exists(output_file):
                    existing_files.append(output_file)

            if existing_files:
                overwrite_msg = f"The following output files already exist:\n{', '.join(existing_files[:5])}{', ...' if len(existing_files) > 5 else ''}\n\nDo you want to overwrite them?"
                if not messagebox.askyesno("File Overwrite Warning", overwrite_msg):
                    self.log_message("Processing stopped due to existing output files.")
                    return

        self.setup_and_start()

    def clear_gui(self):
        for label in self.file_labels.values():
            label.destroy()
        self.file_labels.clear()
        self.log_text.delete(1.0, tk.END)
        self.progress["value"] = 0
        self.processed_files = 0
        self.total_files = 0
        self.progress_label.config(text="0 of 0 processed")
        self.close_button.config(text="Processing", state="disabled")
        self.cancel_flag.clear()
        self.cancel_button.config(state="disabled")

    def log_message(self, message, level="INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - {level} - {message}"
        # Always log to GUI text area if valid settings
        if self.settings_valid and self.settings["output_dir"]:
            current_level = logging.DEBUG if self.debug_mode.get() else logging.INFO
            if logging.getLevelName(level) >= current_level:
                self.log_text.insert(tk.END, log_entry + "\n")
                self.log_text.see(tk.END)
                # Log to file only if write_logfile is enabled and logger is set
                if self.write_logfile.get() and self.logger:
                    getattr(self.logger, level.lower())(message)

    def update_progress(self):
        if self.total_files > 0:
            progress_value = (self.processed_files / self.total_files) * 100
            self.progress["value"] = progress_value
            self.progress_label.config(text=f"{self.processed_files} of {self.total_files} processed")

    def flash_label(self, label):
        if label == self.current_flashing_label and not self.cancel_flag.is_set():
            self.flash_state = not self.flash_state
            bg_color = "yellow" if self.flash_state else "SystemButtonFace"
            label.config(bg=bg_color)
            self.root.after(500, self.flash_label, label)

    def update_file_status(self, input_file, status):
        if input_file in self.file_labels:
            label = self.file_labels[input_file]
            base_name = os.path.basename(input_file)
            if status == "processing":
                text = f"▶ {base_name} - Processing"
                font = ("Helvetica", 10, "bold")
                label.config(bg="yellow")
                self.current_flashing_label = label
                self.flash_state = True
                self.flash_label(label)
            elif status == "completed":
                text = f"✓ {base_name} - Completed"
                font = ("Helvetica", 10)
                label.config(bg="green")
                if self.current_flashing_label == label:
                    self.current_flashing_label = None
            else:  # awaiting
                text = f"⌛ {base_name}"
                font = ("Helvetica", 10)
                label.config(bg="SystemButtonFace")
                if self.current_flashing_label == label:
                    self.current_flashing_label = None
            label.config(text=text, font=font)

    def reencode_file(self, input_file):
        if self.cancel_flag.is_set():
            return

        base_name = os.path.basename(input_file)
        output_file = os.path.normpath(os.path.join(self.settings["output_dir"], f"RE {base_name}"))

        self.update_file_status(input_file, "processing")
        self.log_message(f"Starting processing: {input_file} -> {output_file}")

        bitrate = str(self.settings["bitrate"])
        command = [
            self.settings["handbrake_cli_path"],
            "-v",
            "-i", input_file,
            "-o", output_file,
            "-e", "nvenc_av1",
            "-b", bitrate,
            "--rate", "60",
            "-f", "mkv",
            "-m",
            "-E", "opus",
            "-B", "160",
            "--mixdown", "stereo"
        ]

        self.log_message(f"Executing command: {' '.join(command)}", "DEBUG")

        try:
            self.current_process = subprocess.Popen(
                command, 
                text=True, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            stdout, stderr = self.current_process.communicate()

            self.log_message(f"HandBrakeCLI stdout: {stdout}", "DEBUG")
            self.log_message(f"HandBrakeCLI stderr: {stderr}", "DEBUG")

            if self.cancel_flag.is_set():
                self.log_message(f"Processing of {input_file} was cancelled.", "WARNING")
                self.update_file_status(input_file, "awaiting")
                return

            if self.current_process.returncode == 0:
                self.log_message(f"Successfully encoded {input_file}")
                if os.path.exists(output_file):
                    if self.delete_original.get():
                        self.log_message(f"Output file {output_file} exists, deleting original.", "DEBUG")
                        os.remove(input_file)
                        self.log_message(f"Deleted original file: {input_file}")
                    else:
                        self.log_message(f"Output file {output_file} exists, original file retained.", "DEBUG")
                else:
                    self.log_message(f"Output file {output_file} was not created.", "ERROR")
                    self.log_message(f"Directory writable: {os.access(self.settings['output_dir'], os.W_OK)}", "DEBUG")
                self.processed_files += 1
                self.update_progress()
                self.update_file_status(input_file, "completed")
            else:
                self.log_message(f"Error encoding {input_file}: Process returned {self.current_process.returncode}", "ERROR")
                self.update_file_status(input_file, "awaiting")

        except Exception as e:
            self.log_message(f"Unexpected error with {input_file}: {e}", "ERROR")
            self.update_file_status(input_file, "awaiting")
        finally:
            self.current_process = None

    def process_files(self):
        if not os.path.exists(self.settings["handbrake_cli_path"]):
            self.log_message(f"HandBrakeCLI not found at {self.settings['handbrake_cli_path']}", "ERROR")
            self.enable_close_button()
            self.start_button.config(state="normal")
            self.exit_button.config(state="normal")
            self.is_processing = False
            self.settings_menu.entryconfig("Configure Settings", state="normal")
            self.help_menu.entryconfig("Documentation", state="normal")
            self.enable_tick_boxes()
            return

        self.log_message("Starting re-encoding process.")
        self.start_button.config(state="disabled")
        self.cancel_button.config(state="normal")
        self.exit_button.config(state="disabled")
        self.is_processing = True
        self.settings_menu.entryconfig("Configure Settings", state="disabled")
        self.help_menu.entryconfig("Documentation", state="disabled")
        self.disable_tick_boxes()

        for input_file in self.files_to_process:
            if self.cancel_flag.is_set():
                break
            self.reencode_file(input_file)

        if self.cancel_flag.is_set():
            self.log_message("Processing cancelled by user.", "WARNING")
            self.enable_close_button(cancelled=True)
        else:
            self.log_message("Processing complete.")
            self.enable_close_button(cancelled=False)
        self.start_button.config(state="normal")
        self.cancel_button.config(state="disabled")
        self.exit_button.config(state="normal")
        self.is_processing = False
        self.settings_menu.entryconfig("Configure Settings", state="normal")
        self.help_menu.entryconfig("Documentation", state="normal")
        self.enable_tick_boxes()

    def cancel_processing(self):
        self.cancel_flag.set()
        if self.current_process:
            self.current_process.terminate()
            self.log_message("Terminating current encoding process.", "INFO")
        self.cancel_button.config(state="disabled")
        self.start_button.config(state="normal")
        self.exit_button.config(state="normal")
        self.is_processing = False
        self.settings_menu.entryconfig("Configure Settings", state="normal")
        self.help_menu.entryconfig("Documentation", state="normal")
        self.enable_tick_boxes()

    def enable_tick_boxes(self):
        self.debug_check.config(state="normal")
        self.overwrite_check.config(state="normal")
        self.delete_check.config(state="normal")
        self.logfile_check.config(state="normal")
        self.shutdown_check.config(state="normal")

    def disable_tick_boxes(self):
        self.debug_check.config(state="disabled")
        self.overwrite_check.config(state="disabled")
        self.delete_check.config(state="disabled")
        self.logfile_check.config(state="disabled")
        self.shutdown_check.config(state="disabled")

    def enable_close_button(self, cancelled=False):
        if cancelled:
            self.close_button.config(text="Process Cancelled - Click to Close", state="normal", bg="red", fg="white")
        else:
            self.close_button.config(text="COMPLETED - Click to Close", state="normal", bg="green", fg="white")
            if self.shutdown_after_completion.get():
                self.log_message("Shutdown PC option enabled. System will shut down after closing.")
                self.root.after(2000, self.shutdown_pc)  # Delay shutdown by 2 seconds

    def shutdown_pc(self):
        """Shutdown the PC based on the operating system."""
        system = platform.system()
        try:
            if system == "Windows":
                os.system("shutdown /s /t 5")  # Shutdown in 5 seconds
                self.log_message("Initiating Windows shutdown in 5 seconds.")
            elif system == "Linux" or system == "Darwin":  # Darwin is macOS
                os.system("shutdown -h now")  # Immediate shutdown for Linux/macOS
                self.log_message("Initiating shutdown now.")
            else:
                self.log_message(f"Shutdown not supported on {system}. Please shut down manually.", "WARNING")
        except Exception as e:
            self.log_message(f"Failed to initiate shutdown: {e}", "ERROR")
        finally:
            self.close_gui()  # Close the GUI after initiating shutdown

    def close_gui(self):
        if self.is_processing:
            messagebox.showwarning("Processing", "Cannot exit while processing. Please cancel processing first.")
            return
        self.root.quit()
        self.root.destroy()

    def setup_and_start(self):
        self.files_to_process = [
            os.path.normpath(os.path.join(self.settings["source_dir"], f))
            for f in os.listdir(self.settings["source_dir"])
            if (not self.settings["search_text"] or f.startswith(self.settings["search_text"])) and
            os.path.isfile(os.path.join(self.settings["source_dir"], f)) and
            os.path.splitext(f)[1].lower() in VALID_EXTENSIONS
        ]
        self.total_files = len(self.files_to_process)
        self.processed_files = 0
        self.progress["maximum"] = 100
        self.update_progress()

        if self.total_files == 0:
            self.log_message(f"No video files (.mkv, .mp4, .mov) found in {self.settings['source_dir']} to process.", "WARNING")
            self.enable_close_button(cancelled=False)
            return

        self.log_message(f"Found {self.total_files} video files to process in {self.settings['source_dir']}.")
        for i, input_file in enumerate(self.files_to_process):
            base_name = os.path.basename(input_file)
            label = tk.Label(self.file_frame, text=f"⌛ {base_name}", anchor="w", font=("Helvetica", 10))
            label.pack(fill="x")
            self.file_labels[input_file] = label

        threading.Thread(target=self.process_files, daemon=True).start()

def main():
    root = tk.Tk()
    app = OBSRecodeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
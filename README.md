# Sticky Notes

A simple sticky note application for Linux Ubuntu desktops. It provides a small, yellow notepad that stays on your desktop for quick note-taking.

## Features

- A simple, lightweight sticky note on your desktop.
- Stays on top of other windows and is visible on all workspaces (if supported by your system).
- Notes are automatically saved as you type.
- Notes are reloaded when you start the application.
- System tray icon for easy access and management.
- Can be run as a systemd user service.

## Getting Started

### 1. Clone the Repository

First, clone this repository to your local machine:

```bash
git clone https://github.com/samer-aw/Sticky_notes.git
cd Sticky_notes
```

### 2. Create a Virtual Environment (Optional)

It's recommended to create a virtual environment to manage the project's dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install System Dependencies

This application requires some system libraries to be installed. On Ubuntu/Debian, you can install them with `apt`:

```bash
# Core dependencies
sudo apt-get update
sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0

# Optional, for the best tray icon experience
sudo apt-get install -y gir1.2-appindicator3-0.1
```

## Usage

You can run the application in several ways:

### Direct Execution

You can run the application directly from the command line:

```bash
/usr/bin/python3 sticky_note.py
```

### Running as a Service (systemd)

For the best experience, you can run the application as a background service that starts automatically when you log in.

1.  **Edit the service file:**

    Open the `sticky-note.service` file and replace `/path/to/your/project/sticky_note.py` with the absolute path to the `sticky_note.py` script in the cloned repository.

2.  **Install the service file:**

    Copy the edited service file to your systemd user directory:

    ```bash
    mkdir -p ~/.config/systemd/user/
    cp sticky-note.service ~/.config/systemd/user/
    ```

3.  **Enable and start the service:**

    Reload the systemd user daemon, then enable and start the service:

    ```bash
    systemctl --user daemon-reload
    systemctl --user enable --now sticky-note.service
    ```

### Using the Desktop Launcher

A `sticky-note.desktop` file is provided to allow launching the application from your desktop's application menu. To use it, you may need to copy it to `~/.local/share/applications/` and make it executable:

```bash
mkdir -p ~/.local/share/applications/
cp sticky-note.desktop ~/.local/share/applications/
chmod +x ~/.local/share/applications/sticky-note.desktop
```

## System Tray Icon

The application runs in the background and is accessible via an icon in your system tray. If `libappindicator3` is installed, you will get a native application indicator. Otherwise, it will fall back to a standard `Gtk.StatusIcon`.

-   **Right-click** on the icon to open a menu with the following options:
    -   **Show/Hide Note:** Toggles the visibility of the sticky note window.
    -   **Quit:** Exits the application.

## AppImage (Alternative Distribution)

An AppImage is a single file that contains the application and all its dependencies. It can be run on most Linux distributions without installation.

### Building the AppImage

To build the AppImage, you will need `wget`. You will also need to install the development packages for GTK and librsvg2. `libappindicator3-dev` is optional but recommended.

```bash
sudo apt-get update
sudo apt-get install -y wget libgtk-3-dev librsvg2-dev libappindicator3-dev
```

Then, run the build script:

```bash
chmod +x build-appimage.sh
./build-appimage.sh
```

### Running the AppImage

To run the AppImage, make it executable and then run it:

```bash
chmod +x StickyNote-x86_64.AppImage
./StickyNote-x86_64.AppImage
```

## Uninstallation

To completely remove the application and all its related files from your computer, follow these steps.

**1. Stop and Disable the systemd Service**

If you set up the systemd service, stop and disable it first:

```bash
systemctl --user stop sticky-note.service
systemctl --user disable sticky-note.service
rm ~/.config/systemd/user/sticky-note.service
systemctl --user daemon-reload
```

**2. Remove the Desktop Launcher**

If you installed the desktop launcher, remove it with this command:

```bash
rm ~/.local/share/applications/sticky-note.desktop
```

**3. Remove the Application Files**

Delete the directory where you cloned the repository.

```bash
# Make sure you are in the correct parent directory before running this!
rm -rf Sticky_notes
```

**4. Remove the Saved Note Data**

The application saves your notes to a hidden file in your home directory. You can remove it with this command:

```bash
rm ~/.sticky_note_content
```

**5. Uninstall System Dependencies (Optional)**

This application requires some system libraries. If you are sure you don't need them for any other applications, you can uninstall them.

**Warning:** The following command will remove core GTK and Python libraries from your system. Other applications depend on these libraries. Removing them could break other applications or parts of your desktop environment. **Proceed with extreme caution.** It is often safer to leave these libraries installed.

```bash
# This command is potentially dangerous. Only run it if you are sure.
# sudo apt-get autoremove --purge python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
```

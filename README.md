# Sticky Notes

A simple sticky note application for Linux Ubuntu desktops. It provides a small, yellow notepad that stays on your desktop for quick note-taking.

## Features

- A simple, lightweight sticky note on your desktop.
- Stays on top of other windows and is visible on all workspaces (if supported by your system).
- Notes are automatically saved as you type.
- Notes are reloaded when you start the application.
- System tray icon for easy access and management.
- Can be run as a systemd user service.

## Files

- `sticky_note.py`: The main application script.
- `sticky-note.desktop`: The desktop entry file.
- `sticky-note.svg`: The application icon.
- `sticky-note.service`: The systemd service file.
- `build-appimage.sh`: A script to build the AppImage.
- `README.md`: This file.

## Requirements

- Python 3
- PyGObject (GTK 3)
- `libappindicator3` (optional, for the best system tray icon experience)

## Installation

1.  **Install dependencies:**

    On Ubuntu/Debian, you can install the required packages using `apt`. For the best experience, we recommend installing `gir1.2-appindicator3-0.1`.

    ```bash
    # Core dependencies
    sudo apt-get update
    sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0

    # Optional, for the best tray icon experience
    sudo apt-get install -y gir1.2-appindicator3-0.1
    ```

2.  **Run the application:**

    You can run the application directly from the command line:

    ```bash
    /usr/bin/python3 sticky_note.py
    ```

    However, for a better experience, we recommend running it as a service (see below).

## Running as a Service (systemd)

To run the application as a background service that starts automatically when you log in, you can use the provided systemd service file.

1.  **Edit the service file:**

    Open the `sticky-note.service` file and replace `/path/to/your/project/sticky_note.py` with the absolute path to the `sticky_note.py` script on your system.

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

    The `--now` flag will both enable the service to start on login and start it immediately.

### Managing the Service

-   **Start the service:** `systemctl --user start sticky-note.service`
-   **Stop the service:** `systemctl --user stop sticky-note.service`
-   **Check the status:** `systemctl --user status sticky-note.service`
-   **View the logs:** `journalctl --user -u sticky-note.service`

## System Tray Icon

The application runs in the background and is accessible via an icon in your system tray. If `libappindicator3` is installed, you will get a native application indicator. Otherwise, it will fall back to a standard `Gtk.StatusIcon`.

-   **Right-click** on the icon to open a menu with the following options:
    -   **Show/Hide Note:** Toggles the visibility of the sticky note window.
    -   **Quit:** Exits the application.

When you close the sticky note window, the application will continue running in the background. To quit the application completely, you must use the "Quit" option from the tray icon menu.

## AppImage

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

This will create an AppImage file in the current directory (e.g., `StickyNote-x86_64.AppImage`).

### Running the AppImage

To run the AppImage, make it executable and then run it:

```bash
chmod +x StickyNote-x86_64.AppImage
./StickyNote-x86_64.AppImage
```

## Desktop Launcher

A `sticky-note.desktop` file is provided to allow launching the application from your desktop's application menu. To use it, you may need to copy it to `~/.local/share/applications/` and make it executable:

```bash
mkdir -p ~/.local/share/applications/
cp sticky-note.desktop ~/.local/share/applications/
chmod +x ~/.local/share/applications/sticky-note.desktop
```

After that, you should be able to find "Sticky Note" in your application launcher.

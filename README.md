# Sticky Notes

A simple sticky note application for Linux Ubuntu desktops. It provides a small, yellow notepad that stays on your desktop for quick note-taking.

## Features

- A simple, lightweight sticky note on your desktop.
- Stays on top of other windows and is visible on all workspaces (if supported by your system).
- Notes are automatically saved as you type.
- Notes are reloaded when you start the application.
- **New:** System tray icon for easy access and management.

## Files

- `sticky_note.py`: The main application script.
- `sticky-note.desktop`: The desktop entry file.
- `sticky-note.svg`: The application icon.
- `build-appimage.sh`: A script to build the AppImage.
- `README.md`: This file.

## Requirements

- Python 3
- PyGObject (GTK 3)
- AppIndicator3

## Installation

1.  **Install dependencies:**

    On Ubuntu/Debian, you can install the required packages using `apt`:

    ```bash
    sudo apt-get update
    sudo apt-get install -y python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1
    ```

2.  **Run the application:**

    To run the application, simply execute the `sticky_note.py` script using the system's python interpreter:

    ```bash
    /usr/bin/python3 sticky_note.py
    ```

## System Tray Icon

The application runs in the background and is accessible via an icon in your system tray (the top bar in GNOME).

-   **Right-click** on the icon to open a menu with the following options:
    -   **Show/Hide Note:** Toggles the visibility of the sticky note window.
    -   **Quit:** Exits the application.

When you close the sticky note window, the application will continue running in the background. To quit the application completely, you must use the "Quit" option from the tray icon menu.

## AppImage

An AppImage is a single file that contains the application and all its dependencies. It can be run on most Linux distributions without installation.

### Building the AppImage

To build the AppImage, you will need `wget`. You will also need to install the development packages for GTK, librsvg2, and libappindicator3:

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

## Run on Startup

To make the sticky note appear every time you start your computer, you can add it to your desktop environment's startup applications.

The exact steps may vary depending on your desktop environment (GNOME, KDE, XFCE, etc.), but the general process is:

1.  Open your "Startup Applications" or "Autostart" settings.
2.  Add a new startup program.
3.  In the "Command" field, enter the full path to the `sticky_note.py` script (e.g., `/usr/bin/python3 /path/to/sticky_note.py`) or the AppImage file.
4.  Give it a name (e.g., "Sticky Note") and save it.

Alternatively, you can manually create a `.desktop` file in `~/.config/autostart/`. You can copy the `sticky-note.desktop` file there, but you will need to edit the `Exec` line to have the full path to the executable.

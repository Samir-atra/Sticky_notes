#!/bin/bash

# Exit on error
set -e

# App name
APP=StickyNote

# App directory
APP_DIR=$APP.AppDir

# Download AppImage tools
wget -q https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-x86_64.AppImage
wget -q https://raw.githubusercontent.com/tauri-apps/linuxdeploy-plugin-gtk/master/linuxdeploy-plugin-gtk.sh
chmod +x linuxdeploy-x86_64.AppImage
chmod +x linuxdeploy-plugin-gtk.sh

# Extract linuxdeploy
./linuxdeploy-x86_64.AppImage --appimage-extract

# Clean up previous build
rm -rf $APP_DIR

# Create the AppDir structure
mkdir -p $APP_DIR/usr/bin/
mkdir -p $APP_DIR/usr/share/applications/
mkdir -p $APP_DIR/usr/share/icons/hicolor/256x256/apps/

# Copy the application files
cp sticky_note.py $APP_DIR/usr/bin/sticky_note
cp sticky-note.desktop $APP_DIR/usr/share/applications/

# Copy the application icon
mkdir -p $APP_DIR/usr/share/icons/hicolor/scalable/apps/
cp sticky-note.svg $APP_DIR/usr/share/icons/hicolor/scalable/apps/sticky-note.svg

# Make the main script executable
chmod +x $APP_DIR/usr/bin/sticky_note

# Run linuxdeploy from the extracted directory
# The plugin needs to be in the same directory as the linuxdeploy AppRun
# or in the PATH. I'll copy it there.
cp linuxdeploy-plugin-gtk.sh squashfs-root/usr/bin/

./squashfs-root/AppRun --appdir $APP_DIR --plugin gtk --output appimage

echo "AppImage created successfully!"

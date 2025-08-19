#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
try:
    gi.require_version('AppIndicator3', '0.1')
    from gi.repository import AppIndicator3 as appindicator
    HAS_APPINDICATOR = True
except (ValueError, ImportError):
    HAS_APPINDICATOR = False

from gi.repository import Gtk, Gdk, GLib
import os
import sys

NOTE_FILE = os.path.expanduser("~/.sticky_note_content")
APPINDICATOR_ID = 'stickynote-app'

class StickyNoteWindow(Gtk.Window):
    def __init__(self, app):
        super().__init__(title="Sticky Note", application=app)
        self.set_default_size(300, 300)

        if hasattr(self, 'set_keep_above'):
            self.set_keep_above(True)
        else:
            print("Warning: 'set_keep_above' method not found. The window will not stay on top.")

        if hasattr(self, 'set_sticky'):
            self.set_sticky(True)
        else:
            print("Warning: 'set_sticky' method not found. The window will not be sticky.")

        self.scrolled_window = Gtk.ScrolledWindow()
        self.add(self.scrolled_window)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.scrolled_window.add(self.textview)

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.connect("changed", self.save_note)

        self.setup_styles()
        self.load_note()

        self.connect("delete-event", self.on_delete_event)
        self.connect("show", self.on_window_show)

    def on_delete_event(self, widget, event):
        self.hide()
        return True

    def on_window_show(self, widget):
        # We use a short timeout to ensure the window manager has had time
        # to process the window showing before we try to grab focus.
        GLib.timeout_add(100, self.textview.grab_focus)

    def setup_styles(self):
        css_provider = Gtk.CssProvider()
        css = b"""
        window {
            background-color: #FFFACD; /* LemonChiffon, a nice yellow */
        }
        textview {
            background-color: #FFFACD;
            color: #000000; /* Black text */
            font-family: 'Ubuntu Mono', monospace;
            font-size: 14px;
        }
        """
        css_provider.load_from_data(css)

        screen = Gdk.Screen.get_default()
        style_context = self.get_style_context()
        style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

        textview_style_context = self.textview.get_style_context()
        textview_style_context.add_provider_for_screen(screen, css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

    def load_note(self):
        if os.path.exists(NOTE_FILE):
            try:
                with open(NOTE_FILE, "r") as f:
                    note_content = f.read()
                    self.textbuffer.set_text(note_content)
            except IOError as e:
                print(f"Error loading note: {e}")

    def save_note(self, widget):
        try:
            note_content = self.textbuffer.get_text(
                self.textbuffer.get_start_iter(),
                self.textbuffer.get_end_iter(),
                True
            )
            with open(NOTE_FILE, "w") as f:
                f.write(note_content)
        except IOError as e:
            print(f"Error saving note: {e}")

class StickyNoteApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='org.example.stickynote')
        self.window = None
        self.indicator = None

    def do_startup(self):
        Gtk.Application.do_startup(self)
        self.menu = self.build_menu()

        if HAS_APPINDICATOR:
            self.indicator = appindicator.Indicator.new(APPINDICATOR_ID, os.path.abspath('sticky-note.svg'), appindicator.IndicatorCategory.APPLICATION_STATUS)
            self.indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
            self.indicator.set_menu(self.menu)
        else:
            self.indicator = Gtk.StatusIcon()
            self.indicator.set_from_file(os.path.abspath('sticky-note.svg'))
            self.indicator.set_tooltip_text("Sticky Note")
            self.indicator.connect("popup-menu", self.on_status_icon_popup_menu)

    def do_activate(self):
        if not self.window:
            self.window = StickyNoteWindow(self)
        self.window.present()

    def build_menu(self):
        menu = Gtk.Menu()
        item_show_hide = Gtk.MenuItem(label='Show/Hide Note')
        item_show_hide.connect('activate', self.on_show_hide)
        menu.append(item_show_hide)

        item_quit = Gtk.MenuItem(label='Quit')
        item_quit.connect('activate', self.on_quit)
        menu.append(item_quit)

        menu.show_all()
        return menu

    def on_status_icon_popup_menu(self, icon, button, time):
        self.menu.popup(None, None, None, None, button, time)

    def on_show_hide(self, widget):
        if self.window:
            if self.window.is_visible():
                self.window.hide()
            else:
                self.window.present()

    def on_quit(self, widget):
        self.quit()

if __name__ == "__main__":
    app = StickyNoteApp()
    sys.exit(app.run(sys.argv))

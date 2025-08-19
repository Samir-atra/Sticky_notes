#!/usr/bin/python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import os

NOTE_FILE = os.path.expanduser("~/.sticky_note_content")

class StickyNote(Gtk.Window):
    def __init__(self):
        import inspect
        print("--- Debug Information (inside __init__) ---")
        print(f"Object type: {type(self)}")
        print("Inheritance chain (MRO):")
        for cls in inspect.getmro(type(self)):
            print(f"  - {cls}")

        print("\nMethods available on the 'self' object (searching for 'sticky'):")
        methods = [m for m in dir(self) if 'sticky' in m.lower()]
        print(methods)
        print("--- End Debug Information ---\n")
        super().__init__(title="Sticky Note")
        self.set_default_size(300, 300)
        self.set_keep_above(True)
        self.set_sticky(True)

        self.scrolled_window = Gtk.ScrolledWindow()
        self.add(self.scrolled_window)

        self.textview = Gtk.TextView()
        self.textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.scrolled_window.add(self.textview)

        self.textbuffer = self.textview.get_buffer()
        self.textbuffer.connect("changed", self.save_note)

        self.setup_styles()
        self.load_note()

        self.connect("destroy", Gtk.main_quit)

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

        # Also apply to textview
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


if __name__ == "__main__":
    win = StickyNote()
    win.show_all()
    Gtk.main()

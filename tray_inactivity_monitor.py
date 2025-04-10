#!/usr/bin/env python3

import subprocess
import time
import threading
import os
import sys

from AppKit import NSImage
from AppKit import NSStatusBar, NSVariableStatusItemLength, NSMenu, NSMenuItem, NSApplication
from Foundation import NSObject
from Quartz import CGEventSourceSecondsSinceLastEventType, kCGEventSourceStateHIDSystemState

INACTIVITY_THRESHOLD = 10  # seconds

def get_resource_path(filename):
    return os.path.join(os.path.dirname(sys.argv[0]), "Resources", filename)

def get_bundle_resource_path():
    bundle_path = os.path.abspath(os.path.dirname(sys.argv[0]))
    return os.path.join(bundle_path, "xmrig", "xmrig")

class InactivityMonitor:
    def __init__(self, on_start=None, on_stop=None):
        self.running = True
        self.proc = None
        self.on_start = on_start
        self.on_stop = on_stop
        self.monitor_thread = threading.Thread(target=self.monitor_loop, daemon=True)
        self.monitor_thread.start()

    def get_idle_time(self):
        ALL_EVENT_TYPES = 0xFFFFFFFF
        return CGEventSourceSecondsSinceLastEventType(
            kCGEventSourceStateHIDSystemState,
            ALL_EVENT_TYPES
        )

    def launch_xmrig(self):
        if not self.proc:
            xmrig_path = get_bundle_resource_path()
            self.proc = subprocess.Popen([xmrig_path])
            print("xmrig started")
            if self.on_start:
                self.on_start()

    def kill_xmrig(self):
        if self.proc and self.proc.poll() is None:
            self.proc.terminate()
            self.proc.wait()
            print("xmrig stopped")
            if self.on_stop:
                self.on_stop()
        self.proc = None

    def monitor_loop(self):
        while True:
            if self.running:
                idle = self.get_idle_time()
                if idle > INACTIVITY_THRESHOLD and self.proc is None:
                    self.launch_xmrig()
                elif idle < 1 and self.proc:
                    self.kill_xmrig()
            time.sleep(1)

    def toggle(self):
        self.running = not self.running
        if not self.running:
            self.kill_xmrig()
        return self.running


class AppDelegate(NSObject):
    def applicationDidFinishLaunching_(self, notification):
        statusbar = NSStatusBar.systemStatusBar()
        self.item = statusbar.statusItemWithLength_(NSVariableStatusItemLength)

        # Load icons
        self.icon_running = NSImage.alloc().initByReferencingFile_(get_resource_path("icon_running.png"))
        self.icon_paused = NSImage.alloc().initByReferencingFile_(get_resource_path("icon_paused.png"))

        self.set_icon_paused()  # Set default icon to paused

        # Create menu
        menu = NSMenu.alloc().init()
        self.toggle_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Pause Monitoring", "toggleMonitoring:", ""
        )
        menu.addItem_(self.toggle_item)

        quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_(
            "Quit", "terminate:", ""
        )
        menu.addItem_(quit_item)
        self.item.setMenu_(menu)

        # Start monitor with icon update callbacks
        self.monitor = InactivityMonitor(
            on_start=self.set_icon_running,
            on_stop=self.set_icon_paused
        )

    def set_icon_running(self):
        self.item.button().setImage_(self.icon_running)

    def set_icon_paused(self):
        self.item.button().setImage_(self.icon_paused)

    def toggleMonitoring_(self, sender):
        active = self.monitor.toggle()
        new_title = "Pause Monitoring" if active else "Resume Monitoring"
        self.toggle_item.setTitle_(new_title)
        # If paused manually, set paused icon
        if not active:
            self.set_icon_paused()


if __name__ == "__main__":
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    app.setDelegate_(delegate)
    app.run()

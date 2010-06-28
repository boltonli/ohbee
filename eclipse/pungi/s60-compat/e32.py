#
# e32
#
# Copyright 2004-2006 Helsinki Institute for Information Technology (HIIT)
# and the authors.  All rights reserved.
#
# Authors: Ken Rimey <rimey@hiit.fi>
#          Torsten Rueger <rueger@hiit.fi>
#

# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
wxPython emulation of e32 module from Python for S60

This module emulates the e32 functionality for testing and emulating
Symbian applications on a desktop.

Unlike the original e32, this one depends on appuifw.
"""

# Configurations tested (all with unicode enabled):
#  * Mac OS X 10.4 with wxPython 2.5.3.1
#  * Linux with wxPython 2.5.3.1, 2.5.4, 2.6.1.0
#  * Windows with wxPython 2.5.3.1

from time import sleep
from thread import start_new_thread

import wx
import wx.lib.newevent

from appuifw import app as _app

_UpdateEvent, _EVT_UPDATE = wx.lib.newevent.NewEvent()

class Ao_lock:
    def __init__(self):
        self.app = _app
        self.locked = True

    def wait(self):
        try:
            evtloop = wx.EventLoop()
            old = wx.EventLoop.GetActive()
            wx.EventLoop.SetActive(evtloop)
        except NotImplementedError:
            # wxPython on Mac OS X doesn't yet support the new event loop
            # stuff as of 2.5.3.1.
            evtloop = self.app

        try:
            # Mini event loop
            while self.locked:
                if not evtloop.Pending():
                    # Processing idle events here is redundant on the Mac
                    # because Dispatch() does it, but it is necessary on
                    # other platforms.
                    if self.app.ProcessIdle():
                        # Idle handler requested another round.
                        continue
                    else:
                         # Throttle the loop, because it seems Dispatch()
                         # doesn't block in wxGTK.
                        sleep(0.01)

                if not evtloop.Dispatch():
                    return              # Abort requested.

            # Dispatch pending events before returning.
            while evtloop.Pending():
                if not evtloop.Dispatch():
                    return              # Abort requested.
        finally:
            self.locked = True
            if evtloop is not self.app:
                wx.EventLoop.SetActive(old)

    def signal(self):
        self.locked = False
        # Call PostEvent() asynchronously, because (in wxGTK) it may block
        # during event callback processing, which can lead to deadlocks in
        # our usage.
        start_new_thread(wx.PostEvent, (self.app, _UpdateEvent()))

def ao_yield():
    _app.Yield()

def drive_list():
    return [""]

def ao_sleep(interval, cb=None):
    if cb is not None:
        wx.FutureCall(interval*1000, cb)
    else:
        ao_yield()
        sleep(interval)

def in_emulator():
    return True

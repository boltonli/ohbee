#
# appuifw
#
# Copyright 2004-2006 Helsinki Institute for Information Technology (HIIT)
# and the authors.  All rights reserved.
#
# Authors: Torsten Rueger <rueger@hiit.fi>
#          Alexander Igonichev <amigo12@newmail.ru>
#          Elvis Pfutzenreuter <elvis.pfutzenreuter@indt.org.br>
#          Ken Rimey <rimey@hiit.fi>
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
wxPython emulation of appuifw module from Python for S60

This module emulates the appuifw functionality for testing and
emulating Symbian applications on a desktop.
"""

import time
import locale

import wx
import graphics
from key_codes import *

STYLE_BOLD          = 0x01
STYLE_ITALIC        = 0x02
STYLE_STRIKETHROUGH = 0x04
STYLE_UNDERLINE     = 0x08
HIGHLIGHT_STANDARD  = 0x10
HIGHLIGHT_ROUNDED   = 0x20
HIGHLIGHT_SHADOW    = 0x40

EEventKeyUp = 1
EEventKeyDown = 2
EEventKey = 3

class Application(wx.App):
    def __init__(self, **keys):
        self.frame = None

        self.title = ""
        self.body = None
        self.menu = []
        self.exit_key_handler = None

        self.old_title = self.title
        self.old_body = self.body
        self.old_menu = list(self.menu)

        wx.App.__init__(self, **keys)
        self.Bind(wx.EVT_IDLE, self.OnIdle)

    def set_tabs(self, tab_texts, callback=None):
        self.frame.set_tabs(tab_texts, callback)

    def activate_tab(self, index):
        self.frame.tabs.SetSelection(index)

    def OnInit(self):
        self.frame = AppFrame(None, -1, self.title)
        self.frame.Show(True)
        self.SetTopWindow(self.frame)
        return True

    def OnExit(self):
        pass

    def OnIdle(self, event):
        if self.title != self.old_title:
            self.frame.SetTitle(self.title)
            self.old_title = self.title

        if self.body is not self.old_body:
            self.frame.SetBody(self.body)
            self.old_body = self.body

        if self.menu != self.old_menu:
            self.frame.SetMenu(self.menu)
            self.old_menu = list(self.menu)

        self.frame.SetExitKeyHandler(self.exit_key_handler)

class AppFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(320,500))

        self.Bind(wx.EVT_CLOSE, self.OnClose)

        self.tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.tabs = wx.RadioBox(self, -1, "", choices=[""])
        self.tab_sizer.Add(self.tabs, 1)
        self.tab_sizer.Show(0, False)

        self.body = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)
        self.body_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.body_sizer.Add(self.body, 1, wx.GROW)

        self.exit = wx.Button(self, wx.ID_CANCEL, " Exit ")
        self.exit.Bind(wx.EVT_BUTTON, self.ExitKeyHandler, self.exit)

        self.menu = wx.Choice(self, -1, choices = ["Options"])
        self.menu.SetSelection(0)
        self.menu_handlers = {}
        self.Bind(wx.EVT_CHOICE, self.OnMenuSelect)
        self.button_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.button_sizer.Add(self.menu, 0)
        self.button_sizer.Add((0, 0), 1)
        self.button_sizer.Add(self.exit, 0)

        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self.main_sizer.Add(self.tab_sizer, 0, wx.ALL | wx.GROW, 10)
        self.main_sizer.Add(wx.StaticLine(self, -1), 0, wx.GROW)
        self.main_sizer.Add(self.body_sizer, 1, wx.ALL | wx.GROW, 10)
        self.main_sizer.Add(wx.StaticLine(self, -1), 0, wx.GROW)
        self.main_sizer.Add(self.button_sizer, 0, wx.ALL | wx.GROW, 10)
        self.main_sizer.Add((0, 10), 0)
        self.SetSizer(self.main_sizer)
        self.Layout()

        self.exit_key_handler = None
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def OnMenuSelect(self, event):
        selected = self.menu.GetStringSelection()
        if self.menu_handlers.has_key(selected):
            handler = self.menu_handlers[selected]
            handler()
        self.menu.SetSelection(0)

    def OnKeyDown(self, event):
        app.body.OnKeyDown(event)

    def OnClose(self, event):
        # Exit application if frame is closed.

        # Calling wx.Exit() results in a crash under wxPython 2.5.3.1,
        # so the following will have to suffice.
        self.ExitKeyHandler(event)

    def SetBody(self, body):
        if body is None:
            body = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE)

        self.body.Show(False)
        self.body_sizer.Detach(self.body)

        self.body = body
        self.body_sizer.Add(self.body, 1, wx.GROW)
        self.body.Show(True)

        self.Layout()

    def SetMenu(self, content):
        self.menu_handlers.clear()
        self.menu.Clear()
        self.menu.Append("Options")
        for label, handler in content:
            self.menu_handlers[label] = handler
            self.menu.Append(label)
        self.menu.SetSelection(0)

    def SetExitKeyHandler(self, handler):
        self.exit_key_handler = handler

    def ExitKeyHandler(self, event):
        handler = self.exit_key_handler
        if handler is not None:
            handler()

    def set_tabs(self, tab_texts, callback=None):
        self.tabs.Show(False) # Removed RadioBox doesn't disappear without this.
        self.tab_sizer.Remove(self.tabs)

        self.tabs = wx.RadioBox(self, -1, "", choices=tab_texts)
        self.tab_sizer.Add(self.tabs, 1)
        self.tab_sizer.Show(0, len(tab_texts) > 1)

        self.tab_select = callback
        if callback:
            self.Bind(wx.EVT_RADIOBOX, self.TabSelected, self.tabs)

        self.Layout()

    def TabSelected(self, event):
        if self.tab_select:
            self.tab_select(self.tabs.GetSelection())

class Text(wx.TextCtrl):
    def __init__(self):
        wx.TextCtrl.__init__(self, app.frame, style=wx.TE_MULTILINE)
        self.Show(False)

        self.focus = True  # This attribute is part of the public API.

        self.bindings = {}
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

    def OnKeyDown(self, event):
        code = event.GetKeyCode()
        handler = self.bindings.get(code)
        if handler is not None:
            handler()
        event.Skip()

    def bind(self, key, handler):
        code = key_mappings.get(key)
        # Ignore request if key not in key_mappings.
        if code is not None:
            self.bindings[code] = handler

    def get(self, pos=0, len=None):
        if len is not None:
            last = pos + len
        else:
            last = self.GetLastPosition()

        return self.GetRange(pos, last)

    def set(self, text):
        self.SetValue(text)
        self.SetInsertionPointEnd()

    def add(self, text):
        self.WriteText(text)

    def len(self):
        return self.GetLastPosition()

    def clear(self):
        self.Clear()

    def get_pos(self):
        return self.GetInsertionPoint()

    def set_pos(self, pos):
        self.SetInsertionPoint(pos)

class Listbox(wx.ListCtrl):
    def __init__(self, data, callback):
        wx.ListCtrl.__init__(self, app.frame, -1,
                             style = (wx.LC_REPORT
                                      | wx.LC_NO_HEADER
                                      | wx.LC_SINGLE_SEL))
        self.Show(False)

        self.double = False             # Start in single-column mode.
        self.InsertColumn(0, "")
        self.Bind(wx.EVT_SIZE, self.OnResize)

        self.callback = callback
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.OnSelect, self)

        self.bindings = { wx.WXK_RETURN : callback }
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)

        self.set_list(data)

    def OnResize(self, event):
        w = self.GetClientSize().width
        n = self.GetColumnCount()
        for i in range(n):
            self.SetColumnWidth(i, w / n)
        event.Skip()

    def OnSelect(self, event):
        self.callback()

    def OnKeyDown(self, event):
        code = event.GetKeyCode()
        handler = self.bindings.get(code)
        if handler is not None:
            handler()
        event.Skip()

    def bind(self, key, handler):
        code = key_mappings.get(key)
        # Ignore request if key not in key_mappings.
        if code is not None:
            self.bindings[code] = handler

    def current(self):
        index = self.GetFirstSelected()
        if index < 0:
            index = 0
        return index

    def set_list(self, data, current = 0):
        self.DeleteAllItems()
        for i in range(len(data)):
            item = data[i]
            if not isinstance(item, tuple):
                self.InsertStringItem(i, item)
            else:
                if not self.double:
                    self.double = True
                    self.InsertColumn(1, "")
                self.InsertStringItem(i, item[0])
                self.SetStringItem(i, 1, item[1])
        if data:
            self.Select(current)

FFormEditModeOnly = 1                   # Effectively on by default.
FFormViewModeOnly = 2                   # Not implemented.
FFormAutoLabelEdit = 4
FFormAutoFormEdit = 8
FFormDoubleSpaced = 16                  # Ignored.

class Form(wx.Dialog):
    def __init__(self, data=[], flags=0):
        wx.Dialog.__init__(self, app.frame, -1, "View / Edit", size=(300,250))
        self.size1 = (100, -1)
        self.size2 = (150, -1)
        self.size3 = (40, -1)

        if flags & FFormAutoFormEdit:
            # Enabling form edit must also enable label edit so newly
            # created default labels can be filled in.
            flags |= FFormAutoLabelEdit
        self.flags = flags

        self.data = []
        for item in data:
            if len(item) == 3:
                self.data.append(item)
            else:
                label, type = item
                if type == "text":
                    value = ""
                elif type in ("number", "date", "time"):
                    value = 0.0
                elif type == "combo":
                    raise ValueError("No value for combo field.")
                else:
                    raise ValueError("Bad field type: %s." % type)

                self.data.append((label, type, value))

        self.confirmed_data = list(self.data)
        self.save_hook = None

        self.label_controls = []
        self.value_controls = []
        sizer = wx.BoxSizer(wx.VERTICAL)

        for item in self.data:
            label, type, value = item

            if flags & FFormAutoLabelEdit:
                label_control = wx.TextCtrl(self, -1, label, size=self.size1)
            else:
                label_control = wx.StaticText(self, -1, label, size=self.size1)

            if type == "text":
                value_control = wx.TextCtrl(self, -1, value, size=self.size2)
            elif type == "number":
                value_control = wx.TextCtrl(self, -1, str(value), size=self.size2)
            elif type == "date":
                ymddate = _tm2ymd(value)
                y = wx.TextCtrl(self, -1, str(ymddate[0]), size=self.size3)
                m = wx.TextCtrl(self, -1, str(ymddate[1]), size=self.size3)
                d = wx.TextCtrl(self, -1, str(ymddate[2]), size=self.size3)
                value_control = {'y': y, 'm': m, 'd': d}
            elif type == "time":
                hmstime = _tm2hms(value)
                h = wx.TextCtrl(self, -1, str(hmstime[0]), size=self.size3)
                m = wx.TextCtrl(self, -1, str(hmstime[1]), size=self.size3)
                s = wx.TextCtrl(self, -1, str(hmstime[2]), size=self.size3)
                value_control = [h, m, s]
            elif type == "combo":
                value_control = wx.Choice(self, -1, choices=value[0], size=self.size2)
                value_control.SetSelection(value[1])
            else:
                raise ValueError("Bad field type: %s" % type)

            self.label_controls.append(label_control)
            self.value_controls.append(value_control)

            sub = wx.BoxSizer(wx.HORIZONTAL)
            sub.Add(label_control, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
            
            if isinstance(value_control, dict): 
                for control in _date_localed_sequence():
                    sub.Add(value_control[control], 1, wx.ALIGN_CENTRE|wx.ALL, 5)
            elif isinstance(value_control, list): 
                for control in value_control:
                    sub.Add(control, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
            else:
                sub.Add(value_control, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

            sizer.Add(sub, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        buttons = []
        buttons.append(wx.Button(self, wx.ID_OK, "OK"))
        if flags & FFormAutoFormEdit:
            buttons.append(wx.Button(self, -1, "Add"))
            self.Bind(wx.EVT_BUTTON, self.OnAdd, buttons[-1])
            buttons.append(wx.Button(self, -1, "Del"))
            self.Bind(wx.EVT_BUTTON, self.OnDel, buttons[-1])
        buttons.append(wx.Button(self, wx.ID_CANCEL, "Cancel"))

        box = wx.BoxSizer(wx.HORIZONTAL)
        for button in buttons:
            box.Add(button, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sizer.Add(box, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        buttons[0].SetDefault()

        self.SetSizer(sizer)
        self.Fit()

    def __len__(self):
        return len(self.confirmed_data)

    def __getitem__(self, key):
        return self.confirmed_data[key]

    def OnAdd(self, event):
        #type = popup_menu(["text", "number", "date", "time", "combo"])

        label = "<label>"
        type = "text"
        value = ""

        label_control = wx.TextCtrl(self, -1, label, size=self.size1)
        value_control = wx.TextCtrl(self, -1, value, size=self.size2)

        self.data.append((label, type, value))
        self.label_controls.append(label_control)
        self.value_controls.append(value_control)

        sub = wx.BoxSizer(wx.HORIZONTAL)
        sub.Add(label_control, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
        sub.Add(value_control, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer = self.GetSizer()
        sizer.Insert(len(self.data) - 1, sub, 0,
                     wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        self.Fit()

    def OnDel(self, event):
        self._update()                  # Get current labels.
        labels = [label for label, type, value in self.data]

        index = popup_menu(labels, "Delete:")
        if index is not None:
            del self.data[index]
            del self.label_controls[index]
            if isinstance(self.value_controls[index], dict):
                 for control in self.value_controls[index].keys():
                      del self.value_controls[index][control]
            elif isinstance(self.value_controls[index], list):
                 while value_controls[index]:
                      del value_controls[index][0]
            del self.value_controls[index]

            sizer = self.GetSizer()
            sizer.Hide(index)           # Remove() is broken.
            sizer.Remove(index)
            self.Fit()

    def execute(self):
        while True:
            if self.ShowModal() != wx.ID_OK:
                break

            self._update()

            if self.confirmed_data == self.data:
                break
            elif self.save_hook and not self.save_hook(self.data):
                continue                # XXX Should reset form UI.
            else:
                self.confirmed_data = list(self.data)
                break

        self.Destroy()

    def _update(self):
        # Update self.data to match what is on the screen.
        data = []
        for i in range(len(self.data)):
            label, type, value = self.data[i]

            # Update label from control:
            if isinstance(self.label_controls[i], wx.TextCtrl):
                label = self.label_controls[i].GetValue()

            # Update value from control:
            if type == "text":
                value = self.value_controls[i].GetValue()
            elif type == "number":
                value = float(self.value_controls[i].GetValue())
            elif type == "time":
                value = _hms2tm(int(self.value_controls[i][0].GetValue()), 
                                int(self.value_controls[i][1].GetValue()), 
                                int(self.value_controls[i][2].GetValue()))
            elif type == "date":
                value = _ymd2tm(int(self.value_controls[i]['y'].GetValue()), 
                                int(self.value_controls[i]['m'].GetValue()), 
                                int(self.value_controls[i]['d'].GetValue()))
            elif type == "combo":
                choices, index = value
                index = self.value_controls[i].GetSelection()
                value = choices, index
            else:
                raise NotImplementedError

            data.append((label, type, value))

        self.data = data

def _tm2ymd(ndate):
	l = time.gmtime(ndate)
	return (l[0], l[1], l[2])

def _ymd2tm(y, m, d):
	return time.mktime((y, m, d, 0, 0, 1, 0, 0, 0)) - time.timezone

def _tm2hms(ntime):
	l = time.gmtime(ntime)
	return (l[3], l[4], l[5])

def _hms2tm(h, m, s):
	return h*3600 + m*60 + s

def _date_localed_sequence():
	s = locale.nl_langinfo(locale.D_FMT).lower()
	s2 = [ c for c in s if c in ("y", "m", "d") ]
	if len(s2) < 3:
		# Eeek!
		return ['y', 'm', 'd']
	return s2

class Canvas(wx.PyControl,graphics.DC):
    def __init__(self,redraw_callback=None,event_callback=None):
        size = (176,202)
        #size = (240,320)
        wx.PyControl.__init__(self,app.frame,-1,size=size)
        graphics.DC.__init__(self,size)
        self.event_cb = event_callback
        self.redraw_cb = redraw_callback
        self.Show(True)
        self.SetBackgroundColour("WHITE")
        self.bgcolor = self.GetBackgroundColour()
        self.buffer = wx.EmptyBitmap(self._size[0],self._size[1])
        dc = wx.BufferedDC(None, self.buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.bindings = {}
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyDown)
        self.Bind(wx.EVT_KEY_UP, self.OnKeyUp)
        self.dc = None
        self.eskip = False

    def OnPaint(self, event):
        if self.redraw_cb:
            self.redraw_cb((0,0,175,201))
        dc = wx.BufferedPaintDC(self, self.buffer)

    def OnKeyDown(self, event):
        code = event.GetKeyCode()
        if self.eskip:
            self.eskip = False
        else:
            self.eskip = True
            handler = self.bindings.get(code)
            if handler is not None:
                handler()
            elif self.event_cb is not None:
                pars = {'type': EEventKeyDown, 'keycode': code, 'scancode': code, 'modifiers': 0}
                self.event_cb(pars)
                pars = {'type': EEventKey, 'keycode': code, 'scancode': code, 'modifiers': 0}
                self.event_cb(pars)
        event.Skip()

    def OnKeyUp(self, event):
        code = event.GetKeyCode()
        if self.event_cb is not None:
            pars = {'type': EEventKeyUp, 'keycode': code, 'scancode': code, 'modifiers': 0}
            self.event_cb(pars)
        event.Skip()

    def bind(self, key, handler):
        code = key_mappings.get(key)
        # Ignore request if key not in key_mappings.
        if code is not None:
            self.bindings[code] = handler

def selection_list(data):
    return popup_menu(data)

def query(label, type, initial_value=""):
    if type == "text":
        return _text_query(label, initial_value)
    elif type == "query":
        return _confirm(label)
    else:
        return None

def _text_query(label, initial_value=""):
    result = wx.GetTextFromUser(label, "Query", initial_value)
    return result or None

def _confirm(label):
    # The icons seem to be screwed up in my installation, but hopefully
    # that can be fixed.  I think the usage in this function and the
    # following is correct.  --Ken
    result = wx.MessageBox(label, "Confirmation",
                           wx.OK | wx.CANCEL | wx.ICON_QUESTION)
    if result == wx.OK:
        return True
    else:
        return None

def note(text, type):
    if type == "error":
        icon = wx.ICON_ERROR
    else:
        icon = wx.ICON_INFORMATION

    wx.MessageBox(text, type.title(), wx.OK | icon)

def popup_menu(data, label=""):
    choices = []
    for item in data:
        if isinstance(item, tuple):
            item = ": ".join(item)
        choices.append(item)

    index = wx.GetSingleChoiceIndex(label, "Choice", choices)
    if index >= 0:
        return index
    else:
        return None

app = Application(redirect=False)

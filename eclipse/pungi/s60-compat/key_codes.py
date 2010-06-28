#
# key_codes
#
# Copyright 2004-2006 Helsinki Institute for Information Technology (HIIT)
# and the authors.  All rights reserved.
#
# Authors: Torsten Rueger <rueger@hiit.fi>
#          Alexander Igonichev <amigo12@newmail.ru>
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
Constants required by the appuifw module
"""
import wx

EKeyBackspace = 1
EKeyUpArrow = 2
EKeyDownArrow = 3 
EKeyLeftArrow = 4 
EKeyRightArrow = 5
EKey0 = 6
EKey1 = 7
EKey2 = 8
EKey3 = 9
EKey4 = 10
EKey5 = 11
EKey6 = 12
EKey7 = 13
EKey8 = 14
EKey9 = 15
EKeySelect = 16
EKeyLeftSoftkey = 17

key_mappings = {}

key_mappings[EKeyBackspace] = wx.WXK_BACK
key_mappings[EKeyUpArrow] = wx.WXK_UP
key_mappings[EKeyDownArrow] = wx.WXK_DOWN 
key_mappings[EKeyLeftArrow] = wx.WXK_LEFT
key_mappings[EKeyRightArrow] = wx.WXK_RIGHT
key_mappings[EKeySelect] = wx.WXK_RETURN
key_mappings[EKeyLeftSoftkey] = wx.WXK_SPACE
key_mappings[EKey0] = wx.WXK_NUMPAD0
key_mappings[EKey1] = wx.WXK_NUMPAD1
key_mappings[EKey2] = wx.WXK_NUMPAD2
key_mappings[EKey3] = wx.WXK_NUMPAD3
key_mappings[EKey4] = wx.WXK_NUMPAD4
key_mappings[EKey5] = wx.WXK_NUMPAD5
key_mappings[EKey6] = wx.WXK_NUMPAD6
key_mappings[EKey7] = wx.WXK_NUMPAD7
key_mappings[EKey8] = wx.WXK_NUMPAD8
key_mappings[EKey9] = wx.WXK_NUMPAD9

# Based on list in src/core/Lib/key_codes.py in PyS60 1.3.1:
EScancode0=0x30
EScancode1=0x31
EScancode2=0x32
EScancode3=0x33
EScancode4=0x34
EScancode5=0x35
EScancode6=0x36
EScancode7=0x37
EScancode8=0x38
EScancode9=0x39
EScancodeStar=0x2a
EScancodeHash=0x7f
EScancodeBackspace=0x01
#EScancodeLeftSoftkey=EStdKeyDevice0
#EScancodeRightSoftkey=EStdKeyDevice1
EScancodeSelect=13
EScancodeYes=0xc4
EScancodeNo=0xc5
EScancodeLeftArrow = wx.WXK_LEFT
EScancodeRightArrow = wx.WXK_RIGHT
EScancodeUpArrow = wx.WXK_UP
EScancodeDownArrow = wx.WXK_DOWN
#EScancodeEdit=EStdKeyLeftShift
#EScancodeMenu=EStdKeyApplication0

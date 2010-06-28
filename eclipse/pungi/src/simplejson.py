#
# $Id: s60-simplejson.py,v 1.2 2006/12/27 20:00:04 asc Exp $
#

#
# This is a bare bones port, for Series 60 Python, of Bob Ippolito's
# simplejson.py : http://cheeseshop.python.org/pypi/simplejson
#
# If you are reading this it is also very early days and may
# yet change (translation : may be broken).
#
# Since installing custom libraries in Series 60 3rd Edition Python is
# such a pain in the ass, it is designed to be something that a person
# can simply copy and paste in to their own scripts/applications
# (translation : beware of namespace collisions)
#
# For documentation, please see the '__main__' block below
#
# Aaron Straup Cope
# http://aaronland.info/python/s60-simplejson/

#
# required for the 'yield' love in py 2.2
#

from __future__ import generators

import sre_parse, sre_compile, sre_constants
from sre_constants import BRANCH, SUBPATTERN
from re import VERBOSE, MULTILINE, DOTALL
import re

FLAGS = re.VERBOSE | re.MULTILINE | re.DOTALL
WHITESPACE = re.compile(r'\s*', FLAGS)

#
# random global functions
#

def pattern(pattern, flags=FLAGS):
    def decorator(fn):
        fn.pattern = pattern
        fn.regex = re.compile(pattern, flags)
        return fn
    return decorator

#
# Not defined in py 2.2
#

def enumerate (list) :
    # list of tuples
    lot = []
    
    for i in list :
        lot.append((len(lot), i))

    return lot

#
# scanner.py
#

class Scanner(object):

    def __init__(self, lexicon, flags=FLAGS):
        self.actions = [None]
        # combine phrases into a compound pattern
        s = sre_parse.Pattern()
        s.flags = flags
        p = []
        for idx, token in enumerate(lexicon):
            phrase = token.pattern
            try:
                subpattern = sre_parse.SubPattern(s,
                    [(SUBPATTERN, (idx + 1, sre_parse.parse(phrase, flags)))])
            except sre_constants.error:
                raise
            p.append(subpattern)
            self.actions.append(token)

        p = sre_parse.SubPattern(s, [(BRANCH, (None, p))])
        self.scanner = sre_compile.compile(p)

    def iterscan(self, string, idx=0, context=None):

        """
        Yield match, end_idx for each match
        """
        match = self.scanner.scanner(string, idx).match
        actions = self.actions
        lastend = idx
        end = len(string)
        while True:
            m = match()
            if m is None:
                break
            matchbegin, matchend = m.span()
            if lastend == matchend:
                break
            action = actions[m.lastindex]
            if action is not None:
                rval, next_pos = action(m, context)
                if next_pos is not None and next_pos != matchend:
                    # "fast forward" the scanner
                    matchend = next_pos
                    match = self.scanner.scanner(string, matchend).match
                yield rval, matchend
            lastend = matchend
            
#
# decoder.py
#

"""
Implementation of JSONDecoder
"""

def _floatconstants():
    import struct
    import sys
    _BYTES = '7FF80000000000007FF0000000000000'.decode('hex')

    #
    # Not sure if s60 py is 'big' or not
    # but sys.byteorder is not defined
    #
    
    # if sys.byteorder != 'big':
    #    _BYTES = _BYTES[:8][::-1] + _BYTES[8:][::-1]
    
    nan, inf = struct.unpack('dd', _BYTES)
    return nan, inf, -inf

NaN, PosInf, NegInf = _floatconstants()

def linecol(doc, pos):
    lineno = doc.count('\n', 0, pos) + 1
    if lineno == 1:
        colno = pos
    else:
        colno = pos - doc.rindex('\n', 0, pos)
    return lineno, colno

def errmsg(msg, doc, pos, end=None):
    lineno, colno = linecol(doc, pos)
    if end is None:
        return '%s: line %d column %d (char %d)' % (msg, lineno, colno, pos)
    endlineno, endcolno = linecol(doc, end)
    return '%s: line %d column %d - line %d column %d (char %d - %d)' % (
        msg, lineno, colno, endlineno, endcolno, pos, end)

_CONSTANTS = {
    '-Infinity': NegInf,
    'Infinity': PosInf,
    'NaN': NaN,
    'true': True,
    'false': False,
    'null': None,
}

def JSONConstant(match, context, c=_CONSTANTS):
    return c[match.group(0)], None

pattern('(-?Infinity|NaN|true|false|null)')(JSONConstant)

def JSONNumber(match, context):
    match = JSONNumber.regex.match(match.string, *match.span())
    integer, frac, exp = match.groups()
    if frac or exp:
        res = float(integer + (frac or '') + (exp or ''))
    else:
        res = int(integer)
    return res, None
pattern(r'(-?(?:0|[1-9]\d*))(\.\d+)?([eE][-+]?\d+)?')(JSONNumber)

STRINGCHUNK = re.compile(r'(.*?)(["\\])', FLAGS)
BACKSLASH = {
    '"': u'"', '\\': u'\\', '/': u'/',
    'b': u'\b', 'f': u'\f', 'n': u'\n', 'r': u'\r', 't': u'\t',
}

DEFAULT_ENCODING = "utf-8"

def scanstring(s, end, encoding=None, _b=BACKSLASH, _m=STRINGCHUNK.match):
    if encoding is None:
        encoding = DEFAULT_ENCODING
    chunks = []
    _append = chunks.append
    begin = end - 1
    while 1:
        chunk = _m(s, end)
        if chunk is None:
            raise ValueError(
                errmsg("Unterminated string starting at", s, begin))
        end = chunk.end()
        content, terminator = chunk.groups()
        if content:
            if not isinstance(content, unicode):
                content = unicode(content, encoding)
            _append(content)
        if terminator == '"':
            break
        try:
            esc = s[end]
        except IndexError:
            raise ValueError(
                errmsg("Unterminated string starting at", s, begin))
        if esc != 'u':
            try:
                m = _b[esc]
            except KeyError:
                raise ValueError(
                    errmsg("Invalid \\escape: %r" % (esc,), s, end))
            end += 1
        else:
            esc = s[end + 1:end + 5]
            try:
                m = unichr(int(esc, 16))
                if len(esc) != 4 or not esc.isalnum():
                    raise ValueError
            except ValueError:
                raise ValueError(errmsg("Invalid \\uXXXX escape", s, end))
            end += 5
        _append(m)
    return u''.join(chunks), end

def JSONString(match, context):
    encoding = getattr(context, 'encoding', None)
    return scanstring(match.string, match.end(), encoding)

pattern(r'"')(JSONString)

def JSONObject(match, context, _w=WHITESPACE.match):
    pairs = {}
    s = match.string
    end = _w(s, match.end()).end()
    nextchar = s[end:end + 1]
    # trivial empty object
    if nextchar == '}':
        return pairs, end + 1
    if nextchar != '"':
        raise ValueError(errmsg("Expecting property name", s, end))
    end += 1
    encoding = getattr(context, 'encoding', None)
    iterscan = JSONScanner.iterscan
    while True:
        key, end = scanstring(s, end, encoding)
        end = _w(s, end).end()
        if s[end:end + 1] != ':':
            raise ValueError(errmsg("Expecting : delimiter", s, end))
        end = _w(s, end + 1).end()
        try:
            value, end = iterscan(s, idx=end, context=context).next()
        except StopIteration:
            raise ValueError(errmsg("Expecting object", s, end))
        pairs[key] = value
        end = _w(s, end).end()
        nextchar = s[end:end + 1]
        end += 1
        if nextchar == '}':
            break
        if nextchar != ',':
            raise ValueError(errmsg("Expecting , delimiter", s, end - 1))
        end = _w(s, end).end()
        nextchar = s[end:end + 1]
        end += 1
        if nextchar != '"':
            raise ValueError(errmsg("Expecting property name", s, end - 1))
    object_hook = getattr(context, 'object_hook', None)
    if object_hook is not None:
        pairs = object_hook(pairs)
    return pairs, end

pattern(r'{')(JSONObject)

def JSONArray(match, context, _w=WHITESPACE.match):
    values = []
    s = match.string
    end = _w(s, match.end()).end()
    # look-ahead for trivial empty array
    nextchar = s[end:end + 1]
    if nextchar == ']':
        return values, end + 1
    iterscan = JSONScanner.iterscan
    while True:
        try:
            value, end = iterscan(s, idx=end, context=context).next()
        except StopIteration:
            raise ValueError(errmsg("Expecting object", s, end))
        values.append(value)
        end = _w(s, end).end()
        nextchar = s[end:end + 1]
        end += 1
        if nextchar == ']':
            break
        if nextchar != ',':
            raise ValueError(errmsg("Expecting , delimiter", s, end))
        end = _w(s, end).end()
    return values, end
pattern(r'\[')(JSONArray)
 
ANYTHING = [
    JSONObject,
    JSONArray,
    JSONString,
    JSONConstant,
    JSONNumber,
]

JSONScanner = Scanner(ANYTHING)

class JSONDecoder(object):
    """
    Simple JSON <http://json.org> decoder

    Performs the following translations in decoding:
    
    +---------------+-------------------+
    | JSON          | Python            |
    +===============+===================+
    | object        | dict              |
    +---------------+-------------------+
    | array         | list              |
    +---------------+-------------------+
    | string        | unicode           |
    +---------------+-------------------+
    | number (int)  | int, long         |
    +---------------+-------------------+
    | number (real) | float             |
    +---------------+-------------------+
    | true          | True              |
    +---------------+-------------------+
    | false         | False             |
    +---------------+-------------------+
    | null          | None              |
    +---------------+-------------------+

    It also understands ``NaN``, ``Infinity``, and ``-Infinity`` as
    their corresponding ``float`` values, which is outside the JSON spec.
    """

    _scanner = Scanner(ANYTHING)
    __all__ = ['__init__', 'decode', 'raw_decode']

    def __init__(self, encoding=None, object_hook=None):
        """
        ``encoding`` determines the encoding used to interpret any ``str``
        objects decoded by this instance (utf-8 by default).  It has no
        effect when decoding ``unicode`` objects.
        
        Note that currently only encodings that are a superset of ASCII work,
        strings of other encodings should be passed in as ``unicode``.

        ``object_hook``, if specified, will be called with the result
        of every JSON object decoded and its return value will be used in
        place of the given ``dict``.  This can be used to provide custom
        deserializations (e.g. to support JSON-RPC class hinting).
        """
        self.encoding = encoding
        self.object_hook = object_hook

    def decode(self, s, _w=WHITESPACE.match):
        """
        Return the Python representation of ``s`` (a ``str`` or ``unicode``
        instance containing a JSON document)
        """

        obj, end = self.raw_decode(s, idx=_w(s, 0).end())
        end = _w(s, end).end()
        if end != len(s):
            raise ValueError(errmsg("Extra data", s, end, len(s)))
        return obj

    def raw_decode(self, s, **kw):
        """
        Decode a JSON document from ``s`` (a ``str`` or ``unicode`` beginning
        with a JSON document) and return a 2-tuple of the Python
        representation and the index in ``s`` where the document ended.

        This can be used to decode a JSON document from a string that may
        have extraneous data at the end.
        """
        kw.setdefault('context', self)
        try:
            obj, end = self._scanner.iterscan(s, **kw).next()
        except StopIteration:
            raise ValueError("No JSON object could be decoded")
        return obj, end

#
# simplejson.py
#

class simplejson :

    def __init__ (self) :
        pass
    
    def dump(self, obj, fp, skipkeys=False, ensure_ascii=True, check_circular=True,
             allow_nan=True, cls=None, indent=None, **kw):

        """
        Serialize ``obj`` as a JSON formatted stream to ``fp`` (a
        ``.write()``-supporting file-like object).
        
        If ``skipkeys`` is ``True`` then ``dict`` keys that are not basic types
        (``str``, ``unicode``, ``int``, ``long``, ``float``, ``bool``, ``None``) 
        will be skipped instead of raising a ``TypeError``.
        
        If ``ensure_ascii`` is ``False``, then the some chunks written to ``fp``
        may be ``unicode`` instances, subject to normal Python ``str`` to
        ``unicode`` coercion rules.  Unless ``fp.write()`` explicitly
        understands ``unicode`` (as in ``codecs.getwriter()``) this is likely
        to cause an error.
        
        If ``check_circular`` is ``False``, then the circular reference check
        for container types will be skipped and a circular reference will
        result in an ``OverflowError`` (or worse).
        
        If ``allow_nan`` is ``False``, then it will be a ``ValueError`` to
        serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``)
        in strict compliance of the JSON specification, instead of using the
        JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).
        
        If ``indent`` is a non-negative integer, then JSON array elements and object
        members will be pretty-printed with that indent level.  An indent level
        of 0 will only insert newlines.  ``None`` is the most compact representation.
        
        To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
        ``.default()`` method to serialize additional types), specify it with
        the ``cls`` kwarg.
        """

        if cls is None:
            cls = JSONEncoder
            iterable = cls(skipkeys=skipkeys, ensure_ascii=ensure_ascii,
                           check_circular=check_circular, allow_nan=allow_nan, indent=indent,
                           **kw).iterencode(obj)
            
            # could accelerate with writelines in some versions of Python, at
            # a debuggability cost
            
            for chunk in iterable:
                fp.write(chunk)

    def dumps(self, obj, skipkeys=False, ensure_ascii=True, check_circular=True,
              allow_nan=True, cls=None, indent=None, **kw):
    
        """
        Serialize ``obj`` to a JSON formatted ``str``.
        
        If ``skipkeys`` is ``True`` then ``dict`` keys that are not basic types
        (``str``, ``unicode``, ``int``, ``long``, ``float``, ``bool``, ``None``) 
        will be skipped instead of raising a ``TypeError``.
        
        If ``ensure_ascii`` is ``False``, then the return value will be a
        ``unicode`` instance subject to normal Python ``str`` to ``unicode``
        coercion rules instead of being escaped to an ASCII ``str``.
        
        If ``check_circular`` is ``False``, then the circular reference check
        for container types will be skipped and a circular reference will
        result in an ``OverflowError`` (or worse).
        
        If ``allow_nan`` is ``False``, then it will be a ``ValueError`` to
        serialize out of range ``float`` values (``nan``, ``inf``, ``-inf``) in
        strict compliance of the JSON specification, instead of using the
        JavaScript equivalents (``NaN``, ``Infinity``, ``-Infinity``).
        
        If ``indent`` is a non-negative integer, then JSON array elements and object
        members will be pretty-printed with that indent level.  An indent level
        of 0 will only insert newlines.  ``None`` is the most compact representation.
        
        To use a custom ``JSONEncoder`` subclass (e.g. one that overrides the
        ``.default()`` method to serialize additional types), specify it with
        the ``cls`` kwarg.
        """
        
        if cls is None:
            cls = JSONEncoder
            
        return cls(skipkeys=skipkeys, ensure_ascii=ensure_ascii,
                   check_circular=check_circular, allow_nan=allow_nan, indent=indent, **kw).encode(obj)

    def load(self, fp, encoding=None, cls=None, object_hook=None, **kw):

        """
        Deserialize ``fp`` (a ``.read()``-supporting file-like object containing
        a JSON document) to a Python object.
        
        If the contents of ``fp`` is encoded with an ASCII based encoding other
        than utf-8 (e.g. latin-1), then an appropriate ``encoding`` name must
        be specified.  Encodings that are not ASCII based (such as UCS-2) are
        not allowed, and should be wrapped with
        ``codecs.getreader(fp)(encoding)``, or simply decoded to a ``unicode``
        object and passed to ``loads()``
        
        ``object_hook`` is an optional function that will be called with the
        result of any object literal decode (a ``dict``).  The return value of
        ``object_hook`` will be used instead of the ``dict``.  This feature
        can be used to implement custom decoders (e.g. JSON-RPC class hinting).
        
        To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
        kwarg.
        """
        
        if cls is None:
            cls = JSONDecoder

        if object_hook is not None:
            kw['object_hook'] = object_hook

        return cls(encoding=encoding, **kw).decode(fp.read())

    def loads(self, s, encoding=None, cls=None, object_hook=None, **kw):

        """
        Deserialize ``s`` (a ``str`` or ``unicode`` instance containing a JSON
        document) to a Python object.
    
        If ``s`` is a ``str`` instance and is encoded with an ASCII based encoding
        other than utf-8 (e.g. latin-1) then an appropriate ``encoding`` name
        must be specified.  Encodings that are not ASCII based (such as UCS-2)
        are not allowed and should be decoded to ``unicode`` first.
        
        ``object_hook`` is an optional function that will be called with the
        result of any object literal decode (a ``dict``).  The return value of
        ``object_hook`` will be used instead of the ``dict``.  This feature
        can be used to implement custom decoders (e.g. JSON-RPC class hinting).
        
        To use a custom ``JSONDecoder`` subclass, specify it with the ``cls``
        kwarg.
        """
        
        if cls is None:
            cls = JSONDecoder

        if object_hook is not None:
            kw['object_hook'] = object_hook

        return cls(encoding=encoding, **kw).decode(s)

#
#
#

if __name__ == '__main__' :

    import appuifw
    import e32
    import httplib

    c = httplib.HTTPConnection('twitter.com');
    c.request('GET', '/statuses/public_timeline.json')
    r = c.getresponse()

    s = simplejson()
    
    try :
        posts = s.loads(r.read())

        for tw in posts :
            msg = tw['text']
            
            if e32.in_emulator() :
                appuifw.note(unicode(msg), 'note')
            else :
                import audio
                audio.say(msg)
                
            break
        
    except Exception, e :
        appuifw.note(unicode(e), 'error')

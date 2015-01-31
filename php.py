#!/usr/bin/env python

import re

__version__ = "1.1"

try:  # Python3
    from urllib.parse import quote
except ImportError:  # Python2
    from urllib import quote


class Php(object):

    INI_REGEX_UNQUOTED_LINE = re.compile(r'^([^ =]+)\s*=\s*"?([^"]*)"?$')
    INI_REGEX_QUOTED_LINE = re.compile(r'^([^ =]+)\s*=\s*(.*)$')
    INI_REGEX_INDEXED_ARRAY = re.compile(r'^([^\]]+)\[\]$')
    INI_REGEX_ASSOCIATIVE_ARRAY = re.compile(r'^([^\]]+)\["?([^\]"]+)"?\]$')
    INI_REGEX_HEADER_LINE = re.compile(r'^\[([^\]]+)\]$')

    @classmethod
    def http_build_query(cls, params, convention="%s"):
        """

        This was ripped shamelessly from a PHP forum and ported to Python:

            http://www.codingforums.com/showthread.php?t=72179

        Essentially, it's a (hopefully perfect) replica of PHP's
        http_build_query() that allows you to pass multi-dimensional arrays
        to a URL via POST or GET.

        """

        if len(params) == 0:
            return ""

        output = ""
        for key in params.keys():

            if type(params[key]) is dict:

                output = output + cls.http_build_query(params[key], convention % key + "[%s]")

            elif type(params[key]) is list:

                i = 0
                new_params = {}
                for element in params[key]:
                    new_params[str(i)] = element
                    i += 1

                output = output + cls.http_build_query(
                    new_params,
                    convention % key + "[%s]"
                )

            else:

                key = quote(key)
                val = quote(str(params[key]))
                output = output + convention % key + "=" + val + "&"

        return output

    @classmethod
    def parse_ini_file(cls, filename, strip_quotes=False):
        """

        A hacked-together attempt at making an .ini file parser that's compatible
        with the "standards" that PHP follows in its parse_ini_file() function.
        Among the handy features included are:

            * List notation (varname[] = value)
            * Associative array notation (varname[key] = value)
            * Removal of wrapping double-quotes (varname = "stuff" -becomes- varname = stuff)

        You can turn off the doublequote removal with strip_quotes=False

        Example:
            from php import parse_ini_file
            config = parse_ini_file("config.ini")
            print config["sectionName"]["keyName"]

        """

        ini = {}
        header_key = None
        with open(filename, "r") as f:
            while True:
                line = f.readline()
                if not line:
                    break
                ini, header_key = cls._parse_ini_loop(
                    line,
                    header_key,
                    ini,
                    strip_quotes
                )

        return ini


    @classmethod
    def _parse_ini_loop(cls, line, header_key, ini, strip_quotes):

        header = cls.INI_REGEX_HEADER_LINE.match(line)

        keyval = None

        if strip_quotes:
            keyval = cls.INI_REGEX_UNQUOTED_LINE.match(line)
        else:
            keyval = cls.INI_REGEX_QUOTED_LINE.match(line)

        if header:

            ini[header.group(1)] = {}
            header_key = header.group(1)

        elif keyval:

            indexed_array = cls.INI_REGEX_INDEXED_ARRAY.match(keyval.group(1))
            associative_array = cls.INI_REGEX_ASSOCIATIVE_ARRAY.match(keyval.group(1))

            value = keyval.group(2).rstrip("\n")
            if indexed_array:
                try:
                    ini[header_key][indexed_array.group(1)].append(value)
                except KeyError:
                    ini[header_key][indexed_array.group(1)] = [value]
            elif associative_array:
                try:
                    ini[header_key][associative_array.group(1)][associative_array.group(2)] = value
                except KeyError:
                    ini[header_key][associative_array.group(1)] = {associative_array.group(2): value}
            else:
                ini[header_key][keyval.group(1)] = value

        return ini, header_key

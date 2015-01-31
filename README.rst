python-php
==========

Making some of those PHP-only functions available to Python

Sometimes you want to write a Python script for a project written in PHP.
For the most part, this is easy, but for a few key things, PHP breaks with
the standard and does things in a its own way.  For these cases, you can use
this module to compensate.


http_build_query()
------------------

This was ripped shamelessly from a `PHP forum`_ and ported to Python:

Essentially, it's a (hopefully perfect) replica of PHP's
`http_build_query()`_ that allows you to pass multi-dimensional arrays to a
PHP-managed URL via POST or GET.

.. _PHP forum: http://www.codingforums.com/showthread.php?t=72179
.. _http_build_query(): http://php.net/manual/en/function.http-build-query.php


parse_ini_file()
----------------

A hacked-together attempt at making an .ini file parser that's compatible with
the "standards" that PHP follows in its parse_ini_file() function.  Among the
handy features included are:

* List notation (``varname[] = value``)
* Associative array notation (``varname[key] = value``)
* Removal of wrapping doublequotes (``varname = "stuff"`` becomes ``varname = stuff``)

You can turn off the doublequote removal with ``stripquotes=False``


Example
.......
::

    from php import parse_ini_file
    config = parse_ini_file("config.ini")
    print config["sectionName"]["keyName"]


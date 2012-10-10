# -*- coding: utf-8 -*-
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

# Copyright (c) 2012 dput authors
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.	See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
"""
Implementation of the interface to run a checker.
"""

from dput.core import logger
from dput.util import get_obj
from dput.exceptions import DputConfigurationError


def run_checker(checker, changes, profile):
    """
    Run a checker (by the name of ``checker``) against the changes file (by
    the name of ``changes``), with the upload profile (named ``profile``).

    args:
        ``checker`` (str) string of the checker (which is the name of the
            the JSON file which contains the checker def)

        ``changes`` (:class:`dput.changes.Changes`) changes file that the
            check should be run against.

        ``profile`` (dict) dictonary of the profile that will help guide
            the checker's runtime.
    """
    logger.debug("running checker: %s" % (checker))
    obj = get_obj('checkers', checker)
    if obj is None:
        raise DputConfigurationError("No such checker: `%s'" % (
            checker
        ))

    interface = 'cli'
    if 'interface' in profile:
        interface = profile['interface']
    logger.debug("Using interface %s" % (interface))
    interface_obj = get_obj('interfaces', interface)
    if interface_obj is None:
        raise DputConfigurationError("No such interface: `%s'" % (
            interface
        ))
    interface = interface_obj()
    interface.initialize()

    ret = obj(
        changes,
        profile,
        interface
    )

    interface.shutdown()
    return ret

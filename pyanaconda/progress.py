#
# progress.py: code for handling the one big progress bar
#
# Copyright (C) 2012  Red Hat, Inc.  All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
# Author(s): Chris Lumens <clumens@redhat.com>

from contextlib import contextmanager
import Queue

# A queue to be used for communicating progress information between a subthread
# doing all the hard work and the main thread that does the GTK updates.  This
# queue should have elements of the following format pushed into it:
#
# (PROGRESS_CODE_*, [arguments])
#
# Arguments vary based on the code given.  See below.
progressQ = Queue.Queue()

# Arguments:
#
# _INIT - [num_steps]
# _STEP - []
# _MESSAGE - [string]
# _COMPLETE - []
PROGRESS_CODE_INIT = 0
PROGRESS_CODE_STEP = 1
PROGRESS_CODE_MESSAGE = 2
PROGRESS_CODE_COMPLETE = 3

# Surround a block of code with progress updating.  Before the code runs, the
# message is updated so the user can tell what's about to take so long.
# Afterwards, the progress bar is updated to reflect that the task is done.
@contextmanager
def progress_report(message):
    q = progressQ
    q.put((PROGRESS_CODE_MESSAGE, [message]))
    yield
    q.put((PROGRESS_CODE_STEP, []))
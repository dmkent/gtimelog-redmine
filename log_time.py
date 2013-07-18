#!/usr/bin/env python
"""Tool to automatically log time from gTimeLog files to Redmine.

   Any task with an issue tag in it will contribute spent time to
   that issue.
"""
from datetime import date
import logging
import optparse
import os
import re

from dateutil.parser import parse as parse_date
import pandas

import redmine_conn
import settings


LOGGER = logging.getLogger('gtimelog-redmine')


def parse_timelog(fname):
    """Parse a gTimeLog text file."""
    LOGGER.debug('Parsing time-log file: %s', fname)
    fin = file(fname)

    data = []
    index = []
    for line in fin.readlines():
        line = line.strip('\n')
        if not line:
            continue

        # split to date and description components
        vals = line.split(': ', 1)

        index.append(parse_date(vals[0]))
        data.append(unicode(vals[1]))

    fin.close()
    return pandas.Series(data, index=index)


def log_time(fname, cur_date, debug=False):
    """Log time from ```fname`` on ``cur_date`` to Redmine."""
    issue_pat = re.compile(r'.*(#(?P<issue>\d+)).*')

    # Get connection to Redmine
    conn = redmine_conn.RedmineConnection(**settings.redmine)

    data = parse_timelog(fname)

    # Filter to only the current date
    filtered = data[[d.date() == cur_date for d in data.index]]

    for row in range(1, filtered.shape[0]):
        desc = filtered.irow(row)
        duration = filtered.index[row] - filtered.index[row - 1]
        hours = duration.days * 24 + duration.seconds / 3600.0

        match = issue_pat.match(desc)
        if match:
            issue = int(match.group('issue'))
            LOGGER.debug('Logging %.2f hours to issue #%d (%s)',
                         hours, issue, desc)
            if not debug:
                conn.log_time(issue, hours, comments=desc)


def main():
    """Log to Redmine."""
    usage = ('%prog [options] [date_to_parse]\n\n' +
             '\tdate_to_parse:    Date to log for. Defaults to today.')
    parser = optparse.OptionParser(usage=usage)

    parser.add_option('-f', '--file', dest='fname', default=None,
                      help='Time log file to use. Defaults to gLogTime.')
    parser.add_option('-d', '--debug', action='store_true',
                      help="Don't actually insert anything into Redmine.")

    opts, args = parser.parse_args()

    logging.basicConfig(level=logging.WARN)
    if opts.debug:
        LOGGER.setLevel(logging.DEBUG)

    if len(args) == 1:
        cur_date = parse_date(args[0]).date()
    else:
        cur_date = date.today()

    if opts.fname:
        fname = opts.fname
    else:
        fname = os.path.expandvars('$HOME/.gtimelog/timelog.txt')

    if not os.path.isfile(fname):
        parser.error("Can't find time log file: %s" % fname)

    log_time(fname, cur_date, debug=opts.debug)

if __name__ == '__main__':
    main()

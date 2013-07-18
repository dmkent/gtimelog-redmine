from datetime import date
import glob

from dateutil.parser import parse as parse_date
import pandas

import redmine_conn

def parse_timelog(fname):
    fin = file(fname)

    data = []
    index = []
    for line in fin.readlines():
        line = line.strip('\n')
        if not line:
            continue
        vals = line.split(': ', 1)
        index.append(parse_date(vals[0]))
        data.append(unicode(vals[1]))

    return pandas.Series(data, index=index)

def main(fname, cur_date):
    data = parse_timelog(fname)

    filtered = data[[d.date() == cur_date for d in data.index]]

    print filtered

if __name__ == '__main__':
    main(glob.glob('/home/dkent/.gtimelog/timelog.txt')[0], date(2013, 7, 18))

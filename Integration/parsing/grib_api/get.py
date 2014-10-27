__author__ = 'SKuptsov'

import traceback
import sys

from grib_api.gribapi import *
from datetime import datetime

INPUT = "test/data/multi_1.glo_30m.hs.201312.grb2"
VERBOSE = 1 # verbose error reporting


def example():
    f = open(INPUT)

    while 1:
        gid = grib_new_from_file(f)
        if gid is None: break

        iterid = grib_iterator_new(gid, 0)

        missingValue = grib_get_double(gid, "missingValue")

        date = grib_get(gid, 'dataDate')

        #indicatorOfParameter = grib_get(gid, 'marsParam')

        hour = grib_get(gid, 'dataTime')

        if len(str(hour)) == 3:
            hour = '0' + str(hour)[:-2]
        elif len(str(hour)) == 1:
            hour = '00'
        else:
            hour = str(hour)[:-2]

        #print(indicatorOfParameter)

        print(date)

        print(hour)

        date_object = datetime.strptime(str(date) + ' '+ hour, '%Y%m%d %H')

        print(date_object)

        i = 0
        #while 1:
        #    result = grib_iterator_next(iterid)
        #    if not result: break
        #
        #    [lat,lon,value] = result
        #
        #    sys.stdout.write("- %d - lat=%.6f lon=%.6f value=" % (i,lat,lon))
        #
        #    if value == missingValue:
        #        print "missing"
        #    else:
        #        print "%.6f" % value
        #
        #    i += 1

        grib_iterator_delete(iterid)
        grib_release(gid)

    f.close()


def main():
    try:
        example()
    except GribInternalError, err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print >> sys.stderr, err.msg

        return 1


if __name__ == "__main__":
    sys.exit(main())
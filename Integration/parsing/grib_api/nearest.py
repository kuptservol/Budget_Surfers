__author__ = 'SKuptsov'

import traceback
import sys

from grib_api.gribapi import *

INPUT="test/data/nww3.dp.200409.grb"
VERBOSE=1 # verbose error reporting

def example():
    points = ((50.8708,-1.59),)

    f = open(INPUT)
    gid = grib_new_from_file(f)

    for lat,lon in points:
        nearest = grib_find_nearest(gid,lat,lon)[0]
        print lat,lon
        print nearest.lat,nearest.lon,nearest.value,nearest.distance,nearest.index

        four = grib_find_nearest(gid,lat,lon,is_lsm = False,npoints = 4)
        for i in range(len(four)):
            print "- %d -" % i
            print four[i]

        print "-"*100

    grib_release(gid)
    f.close()

def main():
    try:
        example()
    except GribInternalError,err:
        if VERBOSE:
            traceback.print_exc(file=sys.stderr)
        else:
            print >>sys.stderr,err.msg

        return 1

if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python

__author__ = 'matt'
__date__ = '6/16/13'

"""
PARSE SOME Freaking Hydro DATA
Source: http://waterservices.usgs.gov/rest/IV-Test-Tool.html

"""
import urllib2, json, pprint, os, dateutil.parser, time, subprocess

if __name__ == '__main__':
    print "Staring"
    print os.path.dirname(__file__)

    url = "http://waterservices.usgs.gov/nwis/iv/?format=json,1.1&sites=12208000,12167000,12161000&period=P2D&parameterCd=00060,00065"
    in_cfs_data = json.loads(urllib2.urlopen(url).read())
    out_data_path = os.path.join(os.pardir, 'data/gauge_data.js')

    # Dates are in actual ISO 8601 format.
    # https://github.com/mbostock/d3/wiki/Time-Formatting#wiki-format_iso
    # time.mktime(dateutil.parser.parse(i['dateTime']).timetuple())
    # Given a string representing ISO Time, convert to a datetime.datetime object, then to a time tuple,
    # then use time.mktime() to covert to epoch time.

    stilly_granite_falls = [[int(time.mktime(dateutil.parser.parse(i['dateTime']).timetuple()))*1000, float(i['value'])] for i in in_cfs_data['value']['timeSeries'][0]['values'][0]['value']]
    stilly_arlington = [[int(time.mktime(dateutil.parser.parse(i['dateTime']).timetuple()))*1000, float(i['value'])] for i in in_cfs_data['value']['timeSeries'][2]['values'][0]['value']]
    nooksack_deming = [[int(time.mktime(dateutil.parser.parse(i['dateTime']).timetuple()))*1000, float(i['value'])] for i in in_cfs_data['value']['timeSeries'][4]['values'][0]['value']]

    formatted_gauge_data = json.dumps(
        [{'key':"Stillaguamish At Granite Falls", 'values': stilly_granite_falls},
         {'key':"Stillaguamish At Arlington", 'values': stilly_arlington},
         {'key':"Nooksack River", 'values': nooksack_deming}]
    )

    with open(os.path.join(out_data_path), 'w') as out_file:
        out_file.write(formatted_gauge_data)

    pprint.pprint(formatted_gauge_data)

# Use suprocess module to push revised data to github.
subprocess.call(['git', 'add', out_data_path])
subprocess.call(['git', 'commit', '-m', '"Data Upload: ' + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()) + '"'])
subprocess.call(['git', 'push'])


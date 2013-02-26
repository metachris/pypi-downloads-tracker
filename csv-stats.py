import os
import sys
import csv
import yaml
from pprint import pprint
import datetime
from bs4 import BeautifulSoup
try:
    #Python3
    import urllib.request as urllib
except:
    import urllib

date = datetime.date.today()


class CSVStats(object):
    def csv_stats(self, project):
        csvfile = open(os.path.expanduser(project["csvfile"]), 'r')
        csvreader = csv.reader(csvfile)

        stats = {}
        for row in csvreader:
            if not row:
                continue
            date, fn, v, dl = row
            if not date in stats:
                stats[date] = {}
            if fn == "TOTAL_VERSION":
                stats[date][v] = dl
            elif fn == "TOTAL_ALL":
                stats[date]["TOTAL"] = dl

        day_last = None
        stats_diff = {}

        # Traverse days in ascending order
        keys = stats.keys()
        keys.sort()
        for day in keys:
            if not day_last:
                stats_diff[day] = {}
                for v in stats[day]:
                    stats_diff[day][v] = "%5s" % stats[day][v]
            else:
                stats_diff[day] = {}
                for version in stats[day]:
                    if version in stats[day] and version in stats[day_last]:
                        stats_diff[day][version] = "%5s  (+%s)" % \
                                (stats[day][version], \
                                int(stats[day][version]) - \
                                int(stats[day_last][version]))
                    else:
                        stats_diff[day][version] = "%5s" % stats[day][version]
            day_last = day

        # All our diffs are now in stats_diff
        return stats_diff


def main():
    config = yaml.load_all(open("config_dev.yaml"))
    if len(sys.argv) < 2:
        print "Use: %s <project-name>" % sys.argv[0]
        print
        print "Available project-names:"
        for project in config:
            p = project["pypi-project"]
            print "- '%s'" % p["name"]
        exit(1)

    stats = CSVStats()
    projects = []
    for project in config:
        p = project["pypi-project"]
        #projects.append(p)
        if sys.argv[1].lower() == p["name"].lower():
            print "Statistics for '%s' (https://pypi.python.org/pypi/%s)" % \
                    (p["name"], p["name"])
            pprint(stats.csv_stats(p))
            return
        #get_stats(p["name"], p["versions"], p["csvfile"])


if __name__ == "__main__":
    main()

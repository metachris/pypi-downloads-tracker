import os
import csv
import yaml
import datetime
from bs4 import BeautifulSoup
try:
    #Python3
    import urllib.request as urllib
except:
    import urllib

date = datetime.date.today()


def log_to_file(csvwriter, fn, version, downloads):
    print("filename: %s, version: %s, downloads: %s" % \
            (fn, version, downloads))
    csvwriter.writerow((date, fn, version, downloads))


def get_stats(pypi_project, versions, csvfile):
    # Prepare the output csv file
    downloads_cnt_all = 0
    csvfile = open(os.path.expanduser(csvfile), 'ab')
    csvwriter = csv.writer(csvfile)
    for version in versions:
        downloads_cnt_version = 0
        url = os.path.join("https://pypi.python.org/pypi/", \
                pypi_project, version)
        print url
        content = urllib.urlopen(url).read()
        soup = BeautifulSoup(content)
        download_table = soup.find("table", "list")

        downloads_total = 0
        cache = []
        for row in download_table.find_all("tr"):
            # Each row has a link and the last column is the downloads count
            href = row.find("a")
            cols = row.findAll("td")
            if not href:
                continue
            fn = href.string

            # skips to the last column and saves # of downloads
            for col in cols:
                _downloads = col.string

            downloads = int(_downloads)
            downloads_cnt_version += downloads
            downloads_cnt_all += downloads
            cache.append((fn, version, downloads))

        # In case there were multiple files for this version, this is for all
        if len(cache) > 1:
            for items in cache:
                log_to_file(csvwriter, *items)

        log_to_file(csvwriter, "TOTAL_VERSION", version, \
                downloads_cnt_version)
        print

    # And this count is a total of all files of all versions
    log_to_file(csvwriter, "TOTAL_ALL", "", downloads_cnt_all)
    csvfile.write("\n")
    print
    print


def main():
    config = yaml.load_all(open("config.yaml"))
    for project in config:
        p = project["pypi-project"]
        get_stats(p["name"], p["versions"], p["csvfile"])


if __name__ == "__main__":
    main()

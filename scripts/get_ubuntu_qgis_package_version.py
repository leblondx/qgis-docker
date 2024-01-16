#!/usr/bin/env python3

# This scripts will output the last LTR and stable QGIS versions for Ubuntu
# Formatted as json: {"stable": "3.14.0", "ltr": "3.10.7"}

from apt_repo import APTRepository
import argparse
import re
import json

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-q', '--qgis', help='desktop or server', choices=['desktop', 'server'])
    parser.add_argument('-d', '--dist', help='The Ubuntu distribution', default='focal')
    args = parser.parse_args()
    dist = args.dist

    package_name = 'qgis' if args.qgis == 'dekstop' else 'qgis-server'
    data = {}
    for ltr in (True, False):
        url = f"https://qgis.org/ubuntu{'-ltr' if ltr else ''}"
        components = ['main']
        repo = APTRepository(url, dist, components)
        package = repo.get_packages_by_name(package_name)[0]
        assert package.package == package_name
        # https://regex101.com/r/lkuibv/2
        p = re.compile(f'^1:(\d(?:\.\d+)+)(?:\+\d+{dist})(?:\-\d+)?$')
        m = p.match(package.version)
        data['ltr' if ltr else 'stable'] = m.group(1)

    print(json.dumps(data))

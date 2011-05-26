#!/usr/bin/env python

from __future__ import print_function
import sys
import getpass
import subprocess
import os
from os import path

def exit_error(error):
    print(error, file=sys.stderr)
    exit(1)
    
ini_file = path.expanduser(path.join("~", ".get-shit-done.ini"))

if "linux" in sys.platform:
    restart_network_command = ["/etc/init.d/networking", "restart"]
elif "darwin" in sys.platform:
    restart_network_command = ["dscacheutil", "-flushcache"]
else:
    # Intention isn't to exit, as it still works, but just requires some
    # intervention on the user's part.
    message = '"Please contribute DNS cache flush command on GitHub."'
    restart_network_command = ['echo', message]

hosts_file = '/etc/hosts'
start_token = '## start-gsd'
end_token = '## end-gsd'
site_list = ['reddit.com', 'forums.somethingawful.com', 'somethingawful.com',
            'digg.com', 'break.com', 'news.ycombinator.com', 'infoq.com',
            'bebo.com', 'twitter.com', 'facebook.com', 'blip.com',
            'youtube.com', 'vimeo.com', 'delicious.com', 'flickr.com',
            'friendster.com', 'hi5.com', 'linkedin.com', 'livejournal.com',
            'meetup.com', 'myspace.com', 'plurk.com', 'stickam.com',
            'stumbleupon.com', 'yelp.com', 'slashdot.org']

def sites_from_ini(ini_file):
    # This allows you to specify sites in a file using the following format.
    # site_list is defined above so this will not be used by default.
    # sites = google.com, facebook.com, quora.com ....
    if os.path.exists(ini_file):
        ini_file_handle = open(ini_file)
        for line in ini_file_handle:
            key, value = [each.strip() for each in line.split("=", 1)]
            if key == "sites":
                for item in [each.strip() for each in value.split(",")]:
                    site_list.append(item)
                    
def rehash():
    if "cygwin" in sys.platform:
        print ('Network restart not required.')
    else:
        subprocess.check_call(restart_network_command)

def work():
    hFile = open(hosts_file, 'a+')
    contents = hFile.read()

    if start_token in contents and end_token in contents:
        exit_error("Work mode already set.")

    print(start_token, file=hFile)

    # remove duplicates by converting list to a set
    for site in set(site_list):
        print("127.0.0.1\t" + site, file=hFile)
        print("127.0.0.1\twww." + site, file=hFile)

    print(end_token, file=hFile)
    
    rehash()


def play():
    hosts_file_handle = open(hosts_file, "r+")
    lines = hosts_file_handle.readlines()

    startIndex = -1

    for index, line in enumerate(lines):
        if line.strip() == start_token:
            startIndex = index

    if startIndex > -1:
        lines = lines[0:startIndex]

        hosts_file_handle.seek(0)
        hosts_file_handle.write(''.join(lines))
        hosts_file_handle.truncate()
    
    rehash()


def main():
    if len(sys.argv) != 2:
        exit_error('usage: ' + sys.argv[0] + ' [work|play]')
    {"work": work, "play": play}[sys.argv[1]]()

if __name__ == "__main__":
    sites_from_ini(ini_file)
    main()

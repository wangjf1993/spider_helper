from __future__ import print_function
import os
import sys
import re
from kill import remote_cmd, get_hosts, get_spiders


if __name__ == "__main__":
    ps_name = sys.argv[1]
    hosts = get_hosts()
    spider = get_spiders(ps_name)
    if spider is None:
        print("Cannot found '%s' in config.json." % ps_name)
        exit(1)

    cmd = "ps -ef|grep -vE 'grep|monitor.py|check.py'|grep %s" % spider[1]
    for host in hosts:
        print("On host %s" % host)
        print(remote_cmd(host, cmd).read())

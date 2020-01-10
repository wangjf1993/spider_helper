from __future__ import print_function
import os
import sys
import re
import time
import json
from kill import remote_cmd, get_hosts, get_spiders, kill_pid
from upload import start_spider
import datetime


def dprint(msg):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('(' + date + ')' + msg)


def check_pass(host, dir_name, main_file):
    cmd = "ps -ef|grep -vE 'grep|monitor.py'|grep %s" % main_file
    pss = remote_cmd(host, cmd).readlines()
    if len(pss) == 0:
        dprint('......spider %s not running.' % main_file)
        return False
    for line in pss:
        dprint('......%s' % line.strip())
    if len(pss) > 1:
        dprint('many......spider %s are running.' % main_file)
        kill_pid(host, main_file)
    return True


def check_and_start(host, dir_name, main_file):
    if not check_pass(host, dir_name, main_file):
        main_file_path = os.path.join(dir_name, main_file)
        cmd = "nohup python3 {0} > /dev/null 2>&1 &".format(main_file_path)
        remote_cmd(host, cmd)
        dprint("......spider %s started." % main_file_path)
        dprint("......command: %s" % cmd)

def get_monitors():
    monitors = []
    will_moniter = []
    with open("./config.json", 'r') as f:
        monitors = json.load(f)['monitors']
    spiders = get_spiders()
    for monitor in monitors:
        if monitor not in spiders:
            print('Cannot found %s in config.json file.' % monitor)
            exit(1)
        will_moniter.append(spiders[monitor])
    return will_moniter


if __name__ == '__main__':
    spiders = get_monitors()
    hosts = get_hosts()
    while True:
        for spider in spiders:
            dprint("check spider: %s" % os.path.join(spider[0], spider[1]))
            for host in hosts:
                dprint("...check on host: %s" % host)
                check_and_start(host, spider[0], spider[1])
            print("")
        print("wait 120 seconds...\n")
        time.sleep(120)

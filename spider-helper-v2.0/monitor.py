from __future__ import print_function
import sys
import time
from common import rcmd, Config
from start import start_spider
from check import check_spider
import datetime



def dprint(msg):
    date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print('(' + date + ')' + msg)


def check_pass(host, spider_name, spider_cmd):
    pss = check_spider(host, spider_cmd)
    if pss == "":
        dprint('......spider %s not running.' % spider_name)
        return False
    for line in pss.split('\n'):
        dprint('......%s' % line.strip())
    return True


def check_and_start(host, source_dir, spider_name, spider_cmd):
    if not check_pass(host, spider_name, spider_cmd):
        start_spider(host, source_dir, spider_cmd)
        dprint("......spider %s started." % spider_name)
        dprint("......command: %s" % spider_cmd)


def get_monitors():
    will_moniter = []
    spiders = Config.get_spiders()
    for monitor in Config.get_monitors():
        if monitor not in spiders:
            print('Cannot found %s in config.json file.' % monitor)
            exit(1)
        will_moniter.append([monitor, spiders[monitor]])
    return will_moniter


if __name__ == '__main__':
    if len(sys.argv) == 2:
        config_file = sys.argv[1]
    elif len(sys.argv) == 1:
        config_file = './config.json'
    else:
        print("Example: \n"
              "  python3 monitor.py\n"
              "  python3 monitor.py ./config.json")
        exit(1)

    Config.config_file = config_file
    spiders = get_monitors()
    hosts = Config.get_hosts()
    source_dir = Config.get_sources_dir()
    while True:
        for spider in spiders:
            dprint("check spider: %s" % spider[0])
            for host in hosts:
                dprint("...check on host: %s" % host)
                check_and_start(host, source_dir, spider[0], spider[1])
            print("")
        print("wait 120 seconds...\n")
        time.sleep(120)

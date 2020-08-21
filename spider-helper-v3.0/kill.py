from __future__ import print_function
import re
import sys
from common import rcmd, Config


def kill_spider(host, spider_cmd):
    print("### ssh to %s ..." % host)
    cmd = "ps -ef|grep -vE 'grep|monitor.py|kill.py'|grep '%s'" % spider_cmd
    spiders = rcmd(host, cmd)
    if spiders is None:
        print("Failed to get spiders.")
        return

    for ps in spiders:
        pid = re.split(r'\s+', ps)[1]
        print(ps)
        print("kill %s ..." % pid)
        rcmd(host, "kill %s" % pid)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        config_file = sys.argv[1]
        spider_name = sys.argv[2]
    elif len(sys.argv) == 2:
        config_file = './config.json'
        spider_name = sys.argv[1]
    else:
        print("Example: \n"
              "  python3 kill.py jingdong\n"
              "  python3 kill.py ./config.json jingdong")
        exit(1)

    Config.config_file = config_file
    if spider_name == "all":
        spiders = Config.get_spiders()
    else:
        spiders = [Config.get_spiders(spider_name)]

    for spider in spiders:
        spider_cmd = Config.get_spiders(spider)
        if spider_cmd is None:
            print("Cannot found '%s' in %s." % (spider, config_file))
            exit(1)

        for host in Config.get_hosts():
            kill_spider(host, spider_cmd)

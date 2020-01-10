from __future__ import print_function
import sys
import os
from common import rcmd, Config


def start_spider(host, source_dir, spider_cmd):
    cmds = [
        "cd %s" % os.path.dirname(source_dir),
        "nohup {0} > /dev/null 2>&1 &".format(spider_cmd)
    ]
    cmd = "; ".join(cmds)
    rcmd(host, cmd)


if __name__ == "__main__":
    if len(sys.argv) == 3:
        config_file = sys.argv[1]
        spider = sys.argv[2]
    elif len(sys.argv) == 2:
        config_file = './config.json'
        spider = sys.argv[1]
    else:
        print("Example: \n"
              "  python3 start.py jingdong\n"
              "  python3 start.py ./config.json jingdong")
        exit(1)

    Config.config_file = config_file
    spider_cmd = Config.get_spiders(spider)
    if spider_cmd is None:
        print("Cannot found '%s' in %s." % (spider, config_file))
        exit(1)

    source_dir = Config.get_sources_dir()
    for host in Config.get_hosts():
        print("Start to execute command on %s: \n  %s" % (host, spider_cmd))
        start_spider(host, source_dir, spider_cmd)
        print("Start spider on %s success.\n" % host)

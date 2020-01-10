from __future__ import print_function
import sys
from common import rcmd, Config


def check_spider(host, spider_cmd):
    cmd = "ps -ef|grep -vE 'grep|monitor.py|check.py'|grep '%s'" % spider_cmd
    return rcmd(host, cmd).read()


if __name__ == "__main__":
    if len(sys.argv) == 3:
        config_file = sys.argv[1]
        spider = sys.argv[2]
    elif len(sys.argv) == 2:
        config_file = './config_huawei.json'
        spider = sys.argv[1]
    else:
        print("Example: \n"
              "  python3 check.py jingdong\n"
              "  python3 check.py ./config_huawei.json jingdong")
        exit(1)

    Config.config_file = config_file
    spider_cmd = Config.get_spiders(spider)
    if spider_cmd is None:
        print("Cannot found '%s' in %s." % (spider, config_file))
        exit(1)

    for host in  Config.get_hosts():
        print("On host %s" % host)
        print(check_spider(host, spider_cmd.get("command")))

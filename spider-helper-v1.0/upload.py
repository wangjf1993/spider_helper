from __future__ import print_function
import os
import sys
import re
from kill import remote_cmd, get_hosts, get_local_ip, get_spiders


def rm_remote_src(host, dir_name):
    cmd = "rm -rf %s" % dir_name
    print("Remove remote host %s source dir: %s" % (host, dir_name))
    remote_cmd(host, cmd)


def scp_src_dir(host, dir_name):
    cmd = "scp -r {1} {0}:{1}".format(host, dir_name)
    print("Scp %s to remote host %s" % (dir_name, host))
    os.system(cmd)


def start_spider(host, dir_name, main_file):
    main_file_path = os.path.join(dir_name, main_file)
    cmd = "nohup python3 {0} > /dev/null 2>&1 &".format(main_file_path)
    print("Start spider %s on %s: %s" % (main_file_path, host, cmd))
    remote_cmd(host, cmd)


if __name__ == "__main__":
    name = sys.argv[1]
    spider = get_spiders(name)
    if spider is None:
        print("Cannot found '%s' in config.json." % name)
        exit(1)
    dir_name, main_file = spider

    local_ip = get_local_ip()
    for host in get_hosts():
        if host != local_ip:
            rm_remote_src(host, dir_name)
            import time
            time.sleep(2)
            scp_src_dir(host, dir_name)
        # start_spider(host, dir_name, main_file)

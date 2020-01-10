from __future__ import print_function
import sys
import os
from common import local_ip, Config, rcmd


def rm_remote_src(host, dir_name):
    cmd = "rm -rf %s" % dir_name
    print("Remove remote host %s source dir: %s" % (host, dir_name))
    rcmd(host, cmd)


def scp_src_dir(host, dir_name):
    cmd = "scp -r {1} {0}:{1}".format(host, dir_name)
    print("Scp %s to remote host %s" % (dir_name, host))
    os.system(cmd)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        config_file = sys.argv[1]
    elif len(sys.argv) == 1:
        config_file = './config.json'
    else:
        print("Example: \n"
              "  python3 upload.py\n"
              "  python3 upload.py ./config.json")
        exit(1)

    Config.config_file = config_file
    source_dir = Config.get_sources_dir()
    for host in Config.get_hosts():
        if host != local_ip:
            rm_remote_src(host, source_dir)
            import time
            time.sleep(2)
            scp_src_dir(host, source_dir)

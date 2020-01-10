from __future__ import print_function
import os
import sys
import re
import json


def get_local_ip():
    info = os.popen("ip addr | grep 10.1.1").read()
    addr = re.split(r'\s+', info.strip())[1]
    return addr.split('/')[0]


local_ip =get_local_ip()


def remote_cmd(host, cmd):
    if host == local_ip:
        return os.popen(cmd)
    else:
        return os.popen('ssh %s "%s"' % (host, cmd))
    
    
def kill_pid(host, name):
    print("### ssh to %s ..." % host)
    cmd = "ps -ef|grep -vE 'grep|monitor.py|kill.py'|grep %s" % name
    pss = remote_cmd(host, cmd)
    for ps in pss.readlines():
        pid = re.split(r'\s+', ps)[1]
        print(ps)
        print("kill %s ..." % pid)
        remote_cmd(host, "kill %s" % pid)


def get_hosts():
    with open("./config.json", 'r') as f:
        return json.load(f)['hosts']


def get_spiders(name=None):
    spiders = {}
    with open("./config.json", 'r') as f:
        spiders = json.load(f)['spiders']
    if name and name not in spiders:
        return None
    return spiders[name] if name else spiders


if __name__ == "__main__":
    ps_name = sys.argv[1]
    hosts = get_hosts()
    spider = get_spiders(ps_name)
    if spider is None:
        print("Cannot found '%s' in config.json." % ps_name)
        exit(1)

    for host in hosts:
        kill_pid(host, spider[1])

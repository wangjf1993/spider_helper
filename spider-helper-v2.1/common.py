import json
import os
import re


class Config():

    config_file = './config_huawei.json'
    config = {}

    @classmethod
    def load_config(cls):
        if not cls.config:
            with open(cls.config_file, 'r') as cfg:
                cls.config = json.load(cfg)

    @classmethod
    def get_sources_dir(cls):
        cls.load_config()
        return cls.config['sources']

    @classmethod
    def get_spiders(cls, name=None):
        cls.load_config()
        if name is None:
            return cls.config['spiders']
        return cls.config['spiders'].get(name, None)

    @classmethod
    def get_monitors(cls):
        cls.load_config()
        return cls.config['monitors']

    @classmethod
    def get_hosts(cls):
        cls.load_config()
        return cls.config['hosts']


def get_local_ip():
    info = os.popen("ip addr | grep inet | grep -vE '127.0.0.1'").read()
    addr = re.split(r'\s+', info.strip())[1]
    return addr.split('/')[0]


local_ip = get_local_ip()


def rcmd(host, cmd):
    if host == local_ip:
        return os.popen(cmd)
    else:
        return os.popen('ssh %s "%s"' % (host, cmd))


def clear(source_dir):
    items = os.listdir(source_dir)
    for item in items:
        item_path = os.path.join(source_dir, item)
        if item == "__pycache__":
            rcmd(local_ip, "rm -rf %s" % item_path)
        elif item.endswith(".pyc") or item.endswith(".spec"):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            clear(item_path)

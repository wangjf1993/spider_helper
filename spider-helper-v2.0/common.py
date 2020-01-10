import json
import os
import re


class Config():
    config_file = './config.json'

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
    info = os.popen("ip addr | grep 10.1.1").read()
    addr = re.split(r'\s+', info.strip())[1]
    return addr.split('/')[0]


local_ip = get_local_ip()


def rcmd(host, cmd):
    if host == local_ip:
        return os.popen(cmd)
    else:
        return os.popen('ssh %s "%s"' % (host, cmd))

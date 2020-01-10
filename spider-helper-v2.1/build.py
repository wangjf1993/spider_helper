import sys
import os
from common import Config, rcmd, local_ip, clear


def build_spider(source_dir, subdir, spider_cmd):
    cmd_file = os.path.join(subdir, spider_cmd)
    py_file = "%s.py" % cmd_file
    cmds = [
        "cd %s" % source_dir,
        "rm -rf %s" % cmd_file,
        "pyinstaller -w -F %s --distpath %s" % (py_file, subdir),
        "rm -rf ./build"
    ]
    rcmd(local_ip, "; ".join(cmds))


if __name__ == "__main__":
    if len(sys.argv) == 3:
        config_file = sys.argv[1]
        spider_name = sys.argv[2]
    elif len(sys.argv) == 2:
        config_file = './config_huawei.json'
        spider_name = sys.argv[1]
    else:
        print("Example: \n"
              "  python3 build.py jingdong\n"
              "  python3 build.py ./config_huawei.json jingdong")
        exit(1)

    Config.config_file = config_file
    spider = Config.get_spiders(spider_name)
    if spider is None:
        print("Cannot found '%s' in %s." % (spider_name, config_file))
        exit(1)

    source_dir = Config.get_sources_dir()
    build_spider(source_dir, spider.get("subdir"), spider.get("command"))
    clear(source_dir)

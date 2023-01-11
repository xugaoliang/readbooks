#!/usr/bin/env python
# _*_ coding: utf-8 _*_
"""
Created on 2018-09-23 18:15:49
@author: wind
"""

import argparse
import os
import re


class Summary:
    def __init__(self, show_time=False) -> None:
        self.show_time = show_time
        self.summary_file = "./SUMMARY.md"

    def get_obj_list_by_dir_name(self, name):
        obj_list = []
        g = os.walk(f"{name}/")
        for dirpath, dirnames, filenames in g:
            tmp = dirpath.strip("/").split("/")
            level = len(tmp)
            class_name = tmp[-1]

            o_dir = {
                "is_file": False,
                "level": level,
                "class_name": class_name,
                "path": os.path.join(dirpath, "README.md")
            }
            arr = []
            for filename_full in sorted(filenames):
                if filename_full.endswith(".md") and filename_full != "README.md":
                    # 获取无后缀文件名
                    if re.match("\d{4}-\d{2}-\d{2}", filename_full):
                        filename_short = filename_full[11:-3]
                        filename_long = filename_full[:-3]
                    else:
                        filename_short = filename_full[:-3]
                        filename_long = filename_full[:-3]
                    # 获取文件数据
                    o = {
                        "is_file": True,
                        "level": level,
                        "class_name": class_name,
                        "filename_short": filename_short,
                        "filename_long": filename_long,
                        "path": os.path.join(dirpath, filename_full)
                    }
                    arr.append(o)
            if len(arr) > 0:  # 该目录下有 md 文件
                obj_list.append(o_dir)
                obj_list += arr
        return obj_list

    def get_markdown_by_dir_name(self, name):
        obj_list = self.get_obj_list_by_dir_name(name)
        # 转换为字符
        result = "\n"
        for o in obj_list:
            if not o["is_file"]:
                indent_space = "  "*(o["level"]-1)
                result += f"{indent_space}* [{o['class_name']}]({o['path']})\n"
            else:
                indent_space = "  "*(o["level"])
                show_name = o['filename_long'] if self.show_time else o['filename_short']
                result += f"{indent_space}* [{show_name}]({o['path']})\n"
        return result

    def get_custom_summary(self):
        return """# 读书

* [简介](README.md)
* [个人启发](个人启发.md)"""

    def write_content(self, file_handle, content):
        file_handle.write(content)

    def update_summary(self):

        with open(self.summary_file, "w", encoding="utf-8") as f:
            self.write_content(f, self.get_custom_summary())
            self.write_content(f, self.get_markdown_by_dir_name("读书"))


def main():
    parser = argparse.ArgumentParser(description="文件解析工具")
    parser.add_argument('--show_time',
                        action='store_true', default=False, help='是否显示时间')

    args = parser.parse_args()

    s = Summary(args.show_time)
    s.update_summary()


if __name__ == "__main__":
    main()


# 更新summary
# python update_summary.py --show_time

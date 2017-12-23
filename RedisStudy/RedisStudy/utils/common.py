# -*- coding: utf-8 -*-

import hashlib
import datetime
import re


def get_md5(url):
    if isinstance(url, str):
        url = url.encode("utf-8")
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def remove_space(value):
    value = value.strip().replace("·", "").strip()
    return value


def date_convert(value):
    try:
        create_date = datetime.datetime.strptime(value, "%Y-%m-%d").date()
    except Exception as e:
        create_date = datetime.datetime.now().date()

    return create_date


def return_value(value):
    return value


def get_nums(value):
    match_re = re.match(".*?(\d+).*", value)
    if match_re:
        nums = int(match_re.group(1))
    else:
        nums = 0

    return nums


def remove_comment_tags(value):
    #去掉tag中提取的评论
    if "评论" in value:
        return ""
    else:
        return value


if __name__ == '__main__':
    print(remove_space(value="   2017/12/12 · "))
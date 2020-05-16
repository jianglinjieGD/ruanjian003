# -*- coding: utf-8 -*-
# 这里是一些数据获取和处理的 函数
import datetime


def getCurrentTime( frm = "%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.now()
    return dt.strftime( frm )

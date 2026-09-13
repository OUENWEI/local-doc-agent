import logging
import sys
import os
from datetime import datetime


def setup_logger(name: str = "local_doc_agent") -> logging.Logger:
    """
    初始化项目日志系统。
    返回一个配置好的 Logger 实例，全项目共用。
    """
    logger = logging.getLogger(name)

    # 防止重复添加 handler（多次调用 setup_logger 时会重复打印）
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)  # 全局最低级别，交给 handler 过滤

    # 日志格式：时间 | 级别 | 模块名 | 信息
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # ---------- Handler 1：输出到控制台 ----------
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)  # 控制台只显示 INFO 以上
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # ---------- Handler 2：输出到文件 ----------
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # 自动创建 logs 文件夹
    log_file = os.path.join(log_dir, f"agent_{datetime.now().strftime('%Y%m%d')}.log")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)  # 文件里记录 DEBUG 以上（更详细）
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


# 全局 logger 实例（其他文件 import 这个即可）
logger = setup_logger()
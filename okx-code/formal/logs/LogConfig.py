# --*-- conding:utf-8 --*--
# @Time : 2024/11/27 下午12:44
# @Author : HWS
# @Email : xxxx@163.com
# @description : @TODO
# @Software : PyCharm

import logging
from logging.handlers import RotatingFileHandler
import os
import inspect
from datetime import datetime

class CustomLogger:
    log_counter = 1  # 用于存储日志序号

    def __init__(self, log_dir="logs", max_log_size=1e6, backup_count=3, enable_console_output=True, console_log_levels=None):
        """
        初始化日志系统，支持按级别记录到不同的日志文件，并添加日志轮转功能。
        :param log_dir: 日志文件存放的文件夹
        :param max_log_size: 每个日志文件的最大大小，单位字节
        :param backup_count: 日志文件备份数量
        :param enable_console_output: 是否启用控制台日志输出
        :param console_log_levels: 控制台输出的日志级别列表（例如：[logging.INFO, logging.ERROR]）
        """
        self.logger = logging.getLogger("CustomLogger")
        self.logger.setLevel(logging.DEBUG)  # 设置全局日志级别为 DEBUG（包含所有日志）

        # 创建日志文件夹（如果不存在）
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 设置不同日志级别对应的文件路径
        log_files = {
            logging.DEBUG: os.path.join(log_dir, "debug.log"),
            logging.INFO: os.path.join(log_dir, "info.log"),
            logging.WARNING: os.path.join(log_dir, "warning.log"),
            logging.ERROR: os.path.join(log_dir, "error.log"),
            logging.CRITICAL: os.path.join(log_dir, "critical.log")
        }

        # 为每个日志级别设置独立的文件 handler，添加日志轮转功能
        self._add_rotating_file_handler(logging.DEBUG, log_files[logging.DEBUG], logging.DEBUG, max_log_size, backup_count)
        self._add_rotating_file_handler(logging.INFO, log_files[logging.INFO], logging.INFO, max_log_size, backup_count)
        self._add_rotating_file_handler(logging.WARNING, log_files[logging.WARNING], logging.WARNING, max_log_size, backup_count)
        self._add_rotating_file_handler(logging.ERROR, log_files[logging.ERROR], logging.ERROR, max_log_size, backup_count)
        self._add_rotating_file_handler(logging.CRITICAL, log_files[logging.CRITICAL], logging.CRITICAL, max_log_size, backup_count)

        # 控制台输出
        if enable_console_output:
            self._add_console_handler(console_log_levels)

    def _add_rotating_file_handler(self, level, log_file, log_level, max_log_size, backup_count):
        """
        为指定级别的日志添加轮转的文件处理器。
        :param level: 日志级别
        :param log_file: 日志文件路径
        :param log_level: 日志级别
        :param max_log_size: 日志文件最大大小
        :param backup_count: 日志备份文件数量
        """
        # 使用 RotatingFileHandler 来进行日志轮转
        file_handler = RotatingFileHandler(log_file, maxBytes=max_log_size, backupCount=backup_count)
        file_handler.setLevel(log_level)
        formatter = logging.Formatter('%(log_counter)s. 时间：%(asctime)s   信息：%(message)s   发生位置：%(location)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def _add_console_handler(self, console_log_levels):
        """
        向控制台添加日志输出处理器，并允许根据日志级别进行过滤。
        :param console_log_levels: 控制台日志级别列表
        """
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(log_counter)s. 时间：%(asctime)s   类型：%(levelname)s   信息：%(message)s   发生位置：%(location)s')
        console_handler.setFormatter(formatter)

        # 只有在日志级别符合要求时才输出到控制台
        if console_log_levels:
            console_handler.setLevel(min(console_log_levels))  # 取最小的级别作为控制台日志级别
        else:
            console_handler.setLevel(logging.DEBUG)

        self.logger.addHandler(console_handler)

    def get_logger(self):
        """
        获取自定义的日志记录器实例
        :return: logger 实例
        """
        return self.logger

    def log_exception(self, message="Exception occurred"):
        """
        记录异常信息（仅记录异常简短信息，不输出异常对象）
        :param message: 异常信息
        """
        location = self._get_location()
        self.logger.error(message, extra={'location': location, 'log_counter': CustomLogger.log_counter})

    def log_debug(self, message):
        """
        记录调试日志
        :param message: 日志信息
        """
        location = self._get_location()
        self.logger.debug(message, extra={'location': location, 'log_counter': CustomLogger.log_counter})
        self._increment_counter()

    def log_info(self, message):
        """
        记录信息日志
        :param message: 日志信息
        """
        location = self._get_location()
        self.logger.info(message, extra={'location': location, 'log_counter': CustomLogger.log_counter})
        self._increment_counter()

    def log_warning(self, message):
        """
        记录警告日志
        :param message: 日志信息
        """
        location = self._get_location()
        self.logger.warning(message, extra={'location': location, 'log_counter': CustomLogger.log_counter})
        self._increment_counter()

    def log_error(self, message):
        """
        记录错误日志
        :param message: 日志信息
        """
        location = self._get_location()
        self.logger.error(message, extra={'location': location, 'log_counter': CustomLogger.log_counter})
        self._increment_counter()

    def log_critical(self, message):
        """
        记录严重错误日志
        :param message: 日志信息
        """
        location = self._get_location()
        self.logger.critical(message, extra={'location': location, 'log_counter': CustomLogger.log_counter})
        self._increment_counter()

    def _increment_counter(self):
        """
        自增日志序号
        """
        CustomLogger.log_counter += 1

    def _get_location(self):
        """
        获取调用日志记录的具体位置（模块、行号）
        :return: 调用位置字符串
        """
        frame = inspect.currentframe().f_back
        filename = frame.f_code.co_filename
        line_number = frame.f_lineno
        return f"{filename} (Line {line_number})"

# if __name__ == "__main__":
#     loggers = CustomLogger(log_dir="logs", max_log_size=1e6, backup_count=3,
#                           enable_console_output=True, console_log_levels=[logging.INFO, logging.ERROR])
#     try:
#         # 模拟异常
#         1 / 0
#     except Exception as e:
#         # 记录异常
#         loggers.log_exception("An exception occurred during execution")

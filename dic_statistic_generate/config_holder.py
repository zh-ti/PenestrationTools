import configparser
import os


class ConfigHolder:
    retain_origin_dic = None
    origin_dic_path = None
    result_dic_path = None
    dic_suffix_whitelist = None
    max_thread_num = None

    redis_host = None
    redis_port = None
    redis_username = None
    redis_password = None

    def __init__(self):
        # 创建配置解析器对象
        config = configparser.ConfigParser()

        # 读取配置文件
        config.read('./config.ini', encoding='utf-8')

        # 读取配置信息
        self.retain_origin_dic = config.get('base', 'retain_origin_dic')
        self.origin_dic_path = config.get('base', 'origin_dic_path')
        self.result_dic_path = config.get('base', 'result_dic_path')
        self.dic_suffix_whitelist = config.get('base', 'dic_suffix_whitelist').split(',')
        self.file_type_dic = config.get('base', 'file_type_dic')
        self.max_thread_num = config.getint('base', 'max_thread_num')

        self.redis_host = config.get('redis', 'host')
        self.redis_port = config.getint('redis', 'port')
        self.redis_username = config.get('redis', 'username', fallback=None)
        self.redis_password = config.get('redis', 'password', fallback=None)
        self.redis_db = config.getint('redis', 'db')

        # 验证配置信息
        assert self.retain_origin_dic in "yes,no", "【retain_origin_dic】参数只能是yes或no"
        assert os.path.exists(self.origin_dic_path), f"【{self.origin_dic_path}】目录不存在"
        assert os.path.isdir(self.origin_dic_path), f"【{self.origin_dic_path}】不是一个文件夹"
        assert os.path.exists(self.result_dic_path), f"【{self.result_dic_path}】目录不存在"
        assert os.path.isdir(self.result_dic_path), f"【{self.result_dic_path}】不是一个文件夹"

        # assert self.redis_port.isnumeric(), "【redis_port】参数只能是数字"
        # assert self.redis_db.isnumeric(), "【redis_db】参数只能是数字"

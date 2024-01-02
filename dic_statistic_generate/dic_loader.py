import os
from config_holder import ConfigHolder

config = ConfigHolder()


# 字典加载器
class DicLoader:
    origin_dic_list = None

    def __init__(self, classifier):
        self.origin_dic_list = []
        self.load(config.origin_dic_path, classifier)

    # 加载字典
    def load(self, dic_path, classifier):
        for file in os.listdir(dic_path):
            filePath = os.path.join(dic_path, file)
            # 判断文件是否是目录
            if os.path.isdir(filePath):
                self.load(filePath, classifier)
            else:
                filename, suffix = None, None
                if "." in file:
                    filename, suffix = file.rsplit('.', 1)
                # 判断文件后缀是否在字典白名单中 TODO 后续如果需要考虑无后缀的字典文件，需要修改判定条件
                if suffix is not None and suffix in config.dic_suffix_whitelist:
                    fileTypes = classifier(filePath.replace(config.origin_dic_path, "").lower())
                    self.origin_dic_list.append((fileTypes, filePath))

    # 返回下一个字典
    def next(self):
        return self.origin_dic_list.pop() if len(self.origin_dic_list) > 0 else None

    def getDicNum(self):
        return len(self.origin_dic_list)

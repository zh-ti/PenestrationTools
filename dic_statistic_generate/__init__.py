import concurrent.futures
from dic_statistic_generate.dic_loader import DicLoader
from config_holder import ConfigHolder
from classifier.file_name_classifier import FileNameClassifier
from statisticer import Statisticer

if __name__ == '__main__':
    config = ConfigHolder()
    dicLoader = DicLoader(FileNameClassifier(config.file_type_dic).classify)
    statisticer = Statisticer()
    print(f"统计开始，共{dicLoader.getDicNum()}个字典文件")
    with concurrent.futures.ThreadPoolExecutor(max_workers=ConfigHolder.max_thread_num) as executor:
        tasks = []
        for index in range(1, dicLoader.getDicNum()):
            dic_type, dic = dicLoader.next()
            tasks.append(executor.submit(statisticer.statistic, dic_type, dic))
            # 等待所有线程完成任务
        for task in tasks:
            task.result()
    print(f"全部统计完成")
    statisticer.finish()

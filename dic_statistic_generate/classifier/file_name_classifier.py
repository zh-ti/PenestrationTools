import json
import os
from collections import OrderedDict
from difflib import SequenceMatcher


class FileNameClassifier:
    file_type_dic = None

    def __init__(self, file_type_dic):
        with open(file_type_dic, mode='r', encoding='utf-8') as file:
            self.file_type_dic = json.load(file)

    def classify(self, filename, sep=os.sep):
        filenamePaths = filename.split(sep)
        types = OrderedDict.fromkeys([])
        for name in filenamePaths:
            if name and not name.isspace():
                types.update(self.guessTypes(name))
        return list(types.keys())

    def guessTypes(self, name):
        types = OrderedDict.fromkeys([])
        self.guessType(name, types, self.file_type_dic)
        return types

    def guessType(self, name, types, type_dic):
        for (dicType, keywords) in type_dic.items():
            if isinstance(keywords, dict):
                if findCommonSubstr(name, dicType).size >= 3:
                    types[dicType] = None
                self.guessType(name, types, keywords)
            elif isinstance(keywords, list):
                similarity = 0
                for keyword in keywords:
                    keyword = keyword.lower() if isinstance(keyword, str) else keywords
                    similarity = max(similarity, calcSimilarity(name, keyword))
                if similarity > 0.7:
                    types[dicType] = None


def calcSimilarity(text1, text2):
    return round(SequenceMatcher(None, text1, text2).ratio(), 2)


def findCommonSubstr(text1, text2):
    return SequenceMatcher(None, text1, text2).find_longest_match(0, len(text1), 0, len(text2))

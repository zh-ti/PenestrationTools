class FileContentClassifier:
    def __init__(self):
        pass

    @staticmethod
    def classify(file):
        with open(file, 'r', encoding='utf-8') as file:
            for line in file:
                print(line)

    @staticmethod
    def context(filename):
        pass



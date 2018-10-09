# -*- coding: utf-8 -*-
import jieba
from collections import Counter
from operator import itemgetter, attrgetter

import datetime
import math

jieba.load_userdict('my_dict/dict.txt')

class OutDoc(object):
    def __init__(self, doc_path=None):
        self._path = doc_path
        self._file_open = open(self._path, encoding='utf8')
        self._char = ['“', '、', '…', '？', '，', '。', '”','《', '》', '（', '）']
        self._high_freq = ['的', '在', '了', '于', '', '是', '将', '要', '及', '与', '只', '等'
                           '也', '和']

    def cut_words(self, new_file_path):
        new_file = open(new_file_path, 'a', encoding='utf8')
        stopwordsList = self.stopwordsList()
        for arow in self._file_open.readlines():
            seg_list = jieba.cut(arow, cut_all=False)
            lenc = ""
            for word in seg_list:
                if word not in stopwordsList:
                    if lenc == "":
                        lenc = word
                    else:
                        lenc = lenc + " " + word
            # new_row = " ".join(seg_list)

            new_file.write(lenc)
            new_file.readlines()
        new_file.close()

    def count_words_freq(self, word_list):
        new_word_list = self.replace_char(word_list)
        result = {}
        for word in new_word_list.split(' '):
            if word in result.keys():
                result[word] += 1
            else:
                result[word] = 1
        return result

    def sorted_result(self, dict_info, top):
        result = self.del_high_freq_word(dict_info)
        sort_list = sorted(result.items(), key=itemgetter(1), reverse=True)
        result_list = []

        for i in range(0, top):
            if len(sort_list) > i:
                result_list.append(sort_list[i])
        return result_list

    def replace_char(self, sentence):
        for char in self._char:
            sentence = sentence.replace(char, ' ')
        return sentence

    def del_high_freq_word(self, dict_word):
        for key in self._high_freq:
            if key in dict_word.keys():
                dict_word.pop(key)
        return dict_word

    def stopwordsList(self):
        stopwords = [line.strip() for line in open('stopword.txt', encoding='utf-8')]
        return stopwords


class TfIdf(object):
    def __init__(self, data_dict):
        self._data_dict = data_dict

    # TF 等于 该文档中该词出现的次数 除以文档的总词数
    # IDF 等于总的 log（总文档数/总文档中该词出现的次数 + 1）
    # 最后将 TF*IDF
    def calculate_result(self):
        result = []
        x = 0
        for row in self._data_dict:
            x += 1
            print(x)
            total_count = 0
            for i in range(len(row)):
                total_count = total_count + row[i][1]
            article = {}
            for i in range(len(row)):
                tf_idf = {}
                word = row[i][0]
                word_count = row[i][1]
                TF_word = word_count/total_count

                IDF_word_count = 0
                for arow in self._data_dict:
                    for i in range(len(arow)):
                        if arow[i][0] == word:
                            IDF_word_count += 1
                            break

                IDF = math.log(len(self._data_dict)/(IDF_word_count +1), 2)

                article[word] = TF_word * IDF
            sort_list = sorted(article.items(), key=itemgetter(1), reverse=True)
            result.append(sort_list)
        return result





if __name__ == "__main__":
    now = datetime.datetime.now()
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    new_obj = OutDoc('text.txt')
    new_obj.cut_words('test1.txt')
    file_n = open('test1.txt', 'r', encoding='utf8')

    data_dict = []
    for row in file_n.readlines():
        word_dict = new_obj.count_words_freq(row)
        sorted_result = new_obj.sorted_result(word_dict, top=10)
        data_dict.append(sorted_result)

    tfidf = TfIdf(data_dict)
    reslut = tfidf.calculate_result()

    for row in reslut:
        print(row)
    print(datetime.datetime.now() - now)










# -*- coding: utf-8 -*-
import jieba
from collections import Counter
from operator import itemgetter, attrgetter


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
        for arow in self._file_open.readlines():
            seg_list = jieba.cut(arow, cut_all=False)
            new_row = " ".join(seg_list)
            new_file.write(new_row)
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

def TF_IDF(file_path):
    file_article = open(file_path)
    for each_article in file_article.readlines():

        pass




if __name__ == "__main__":
    new_obj = OutDoc('text.txt')
    # new_obj.cut_words()

    file_n = open('new_text.txt', 'r', encoding='utf8')

    for row in file_n.readlines():
        word_dict = new_obj.count_words_freq(row)
        sorted_result = new_obj.sorted_result(word_dict, top=10)
        print(sorted_result)

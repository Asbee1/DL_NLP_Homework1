import jieba
import math
import os
import re
class TraversalFun():

    # 1 初始化
    def __init__(self, rootDir):
        self.rootDir = rootDir

    def TraversalDir(self):
        return TraversalFun.getCorpus(self, self.rootDir)

    def getCorpus(self, rootDir):
        corpus = []
        r1 = u'[a-zA-Z0-9’!"#$%&\'()*+,-./:：;<=>?@，。?★、…【】《》？“”‘’！[\\]^_`{|}~]+'
        listdir = os.listdir(rootDir)
        count=0
        for file in listdir:
            path  = os.path.join(rootDir, file)
            if os.path.isfile(path):
                with open(os.path.abspath(path), "r", encoding='ansi') as file:  #将所有非中文全部去除
                    filecontext = file.read();
                    filecontext = filecontext.replace("本书来自www.cr173.com免费txt小说下载站\n更多更新免费电子书请关注www.cr173.com", '')#删除广告
                    filecontext = re.sub(r1, '', filecontext)
                    filecontext = filecontext.replace("\n", '')#删除回车
                    filecontext = filecontext.replace("\u3000", '')#删除中文半角空格
                    filecontext = filecontext.replace(" ", '')#删除英文空格
                    count += len(filecontext)
                    corpus.append(filecontext)
            elif os.path.isdir(path):
                TraversalFun.AllFiles(self, path)
        return corpus,count

# 统计词频
def get_tf(tf_dic, words):

    for i in range(len(words)-1):
        tf_dic[words[i]] = tf_dic.get(words[i], 0) + 1#创建一元词频词典

def get_bigram_tf(tf_dic, words):
    for i in range(len(words)-1):
        tf_dic[(words[i], words[i+1])] = tf_dic.get((words[i], words[i+1]), 0) + 1#创建二元词频词典

def get_trigram_tf(tf_dic, words):
    for i in range(len(words)-2):
        tf_dic[((words[i], words[i+1]), words[i+2])] = tf_dic.get(((words[i], words[i+1]), words[i+2]), 0) + 1#创建三元词频词典


def cal_unigram_1(corpus,count):
    before = time.time()
    split_words = []
    words_len = 0
    line_count = 0
    words_tf = {}
    for line in corpus:
        for x in line:
            split_words.append(x)  #分完词之后的数组
            words_len += 1
        get_tf(words_tf, split_words)
        split_words = []
        line_count += 1

    print("字数:", count)
    entropy = []
    for uni_word in words_tf.items():
        entropy.append(-(uni_word[1] / words_len) * math.log(uni_word[1] / words_len, 2))#append在末尾添加新的对象
    print("一元模型信息熵:", round(sum(entropy), 3), "比特/字")


def cal_bigram_1(corpus, count):
    split_words = []
    words_len = 0
    line_count = 0
    words_tf = {}
    bigram_tf = {}

    for line in corpus:
        for x in line:
            split_words.append(x)
            words_len += 1

        get_tf(words_tf, split_words)
        get_bigram_tf(bigram_tf, split_words)

        split_words = []
        line_count += 1

    print("字数:", count)
    bigram_len = sum([dic[1] for dic in bigram_tf.items()])

    entropy = []
    for bi_word in bigram_tf.items():
        jp_xy = bi_word[1] / bigram_len  # p(x,y)
        cp_xy = bi_word[1] / words_tf[bi_word[0][0]]  # p(x|y)
        entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算信息熵
    print("二元模型信息熵:", round(sum(entropy), 3), "比特/字")



def cal_trigram_1(corpus,count):
    before = time.time()
    split_words = []
    words_len = 0
    line_count = 0
    words_tf = {}
    trigram_tf = {}

    for line in corpus:
        for x in line:
            split_words.append(x)
            words_len += 1

        get_bigram_tf(words_tf, split_words)
        get_trigram_tf(trigram_tf, split_words)

        split_words = []
        line_count += 1

    print("字数:", count)
    trigram_len = sum([dic[1] for dic in trigram_tf.items()])


    entropy = []
    for tri_word in trigram_tf.items():
        jp_xy = tri_word[1] / trigram_len  # p(x,y)
        cp_xy = tri_word[1] / words_tf[tri_word[0][0]]  # p(x|y)
        entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算信息熵
    print("三元模型信息熵:", round(sum(entropy), 3), "比特/字")


def cal_unigram(corpus,count):

    split_words = []
    words_len = 0
    #line_count = 0
    words_tf = {}
    for line in corpus:
        for x in jieba.cut(line):
            split_words.append(x)  #分完词之后的数组
            words_len += 1
        get_tf(words_tf, split_words)
        split_words = []
        #line_count += 1

    print("分词个数:", words_len)
    print("平均词长:", round(count / words_len, 3))
    entropy = []
    for uni_word in words_tf.items():
        entropy.append(-(uni_word[1] / words_len) * math.log(uni_word[1] / words_len, 2))#append在末尾添加新的对象
    print("一元模型信息熵:", round(sum(entropy), 3), "比特/词")


def cal_bigram(corpus, count):

    split_words = []
    words_len = 0
    line_count = 0
    words_tf = {}
    bigram_tf = {}

    for line in corpus:
        for x in jieba.cut(line):
            split_words.append(x)
            words_len += 1

        get_tf(words_tf, split_words)
        get_bigram_tf(bigram_tf, split_words)

        split_words = []
        line_count += 1


    bigram_len = sum([dic[1] for dic in bigram_tf.items()])


    entropy = []
    for bi_word in bigram_tf.items():
        jp_xy = bi_word[1] / bigram_len  # p(x,y)
        cp_xy = bi_word[1] / words_tf[bi_word[0][0]]  # p(x|y)
        entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算信息熵
    print("二元模型信息熵:", round(sum(entropy), 3), "比特/词")



def cal_trigram(corpus,count):

    split_words = []
    words_len = 0
    line_count = 0
    words_tf = {}
    trigram_tf = {}

    for line in corpus:
        for x in jieba.cut(line):
            split_words.append(x)
            words_len += 1

        get_bigram_tf(words_tf, split_words)
        get_trigram_tf(trigram_tf, split_words)

        split_words = []
        line_count += 1



    trigram_len = sum([dic[1] for dic in trigram_tf.items()])


    entropy = []
    for tri_word in trigram_tf.items():
        jp_xy = tri_word[1] / trigram_len  # p(x,y)
        cp_xy = tri_word[1] / words_tf[tri_word[0][0]]  # p(x|y)
        entropy.append(-jp_xy * math.log(cp_xy, 2))  # 计算信息熵
    print("三元模型信息熵:", round(sum(entropy), 3), "比特/词")


if __name__ == '__main__':
    tra = TraversalFun("./data/1")
    corpus,count = tra.TraversalDir()
    #cal_unigram_1(corpus, count)
    #cal_bigram_1(corpus,count)
    #cal_trigram_1(corpus,count)

    cal_unigram(corpus, count)
    cal_bigram(corpus, count)
    cal_trigram(corpus, count)



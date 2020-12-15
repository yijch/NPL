from tqdm import tqdm
import matplotlib
import matplotlib.pyplot as plt
from collections import Counter, defaultdict


def draw(counter, plot_title, most=20):
    '''
    画画的baby，画画的baby，画画的baby......

    counter:画图的数据
    plot_title:图标题
    most:显示top 20的数据
    '''
    y_axis, x_axis = [], []
    for (k, v) in counter.most_common(most):
        y_axis.append(k)
        x_axis.append(v)
    # 中文乱码和坐标轴负号处理。
    matplotlib.rc('font', family='SimHei', weight='bold')
    plt.rcParams['axes.unicode_minus'] = False

    plt.figure(figsize=(16, 8))  # 设置画布的尺寸
    plt.title(plot_title, fontsize=20)  # 标题，并设定字号大小

    # alpha：透明度；facecolor：柱子填充色；edgecolor：柱子轮廓色；lw：柱子轮廓的宽度；label：图例；
    tmp = plt.barh(y_axis, x_axis, alpha=0.6, color='#6699CC')
    for rect in tmp:
        w = rect.get_width()
        plt.text(w, rect.get_y() + rect.get_height() / 2, '%d' % int(w), ha='left', va='center')
    plt.legend()
    plt.show()  # 显示图像


def _is_chinese_char(cp):
    """Checks whether CP is the codepoint of a CJK character."""
    # ord()函数：
    # 获取以一个字符（长度为1的字符串）对应的 ASCII 数值，或者 Unicode 数值，
    # 如果所给的 Unicode 字符超出了你的 Python 定义范围，则会引发一个 TypeError 的异常
    cp = ord(cp)
    if ((cp >= 0x4E00 and cp <= 0x9FFF)
            or (cp >= 0x3400 and cp <= 0x4DBF)  #
            or (cp >= 0x20000 and cp <= 0x2A6DF)  #
            or (cp >= 0x2A700 and cp <= 0x2B73F)  #
            or (cp >= 0x2B740 and cp <= 0x2B81F)  #
            or (cp >= 0x2B820 and cp <= 0x2CEAF)  #
            or (cp >= 0xF900 and cp <= 0xFAFF)
            or (cp >= 0x2F800 and cp <= 0x2FA1F)):
        return True
    return False


def cut_qts_to_words(qts_file):
    # 虚词不统计
    invalid_word = ["，", "。", "不", "而", "第", "何", "乎", "乃", "其", "且", "若", "于", "与", "也", "则", "者",
                    "之", "无", "有", "来", "一", "中", "时", "上", "为", "自", "如", "此", "去", "下", "得", "多",
                    "是", "子", "三", "已"]
    # 全局视角统计
    full_word_freq = Counter()  # 字频统计
    poem_num = 0  # 诗篇总数
    # 诗人视角统计
    author_counter = Counter()  # 每个诗人的写诗篇数
    author_word_freq = {}  # 示例：{'李白':Counter; '杜甫':Counter}
    with open(qts_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    poet_total ='' #初始化诗集库
    author_list = []

    for line in tqdm(lines, desc='统计各项数据：'):
        import re
        # 提取诗人

        a = [m.start() for m in re.finditer('\t', line)]
        author = line[a[1]+1:a[2]]  # 提取诗人
        line = line[0:a[1]+1] + line[a[2]:]
        # 规范化每篇诗词中的字
        line = re.sub('[\t，_]', '', line) ## 去除无效字符
        article = list(line)  # 单遍诗词分为单个字article
        article_str = '' # 初始化规范化后的诗词
        ##遍历诗词中的字，删除作品中的虚词和无效字符，诗词按诗人分类统计
        for i in article:
            if i not in invalid_word and _is_chinese_char(i) == True:
                article_str = article_str + i

        if author not in author_list:
            author_list.append(author)#诗人添加到诗人列表中
            author_counter[author] = 1 # 每个诗人的诗歌数量第1篇
        else:
            author_counter[author] += 1 # 每个诗人的写诗篇数
            article_str += article_str
        author_word_freq[author]=Counter(article_str)
        # author_word_freq中存放某字在某位诗人所作诗词中出现的次数
        #将当前诗词加入诗人的诗词集中
        poet_total = poet_total + article_str #当前诗词加入诗词总库
        poem_num += 1 #诗词总篇数+1
        full_word_freq=Counter(poet_total)
    return full_word_freq, author_counter, author_word_freq, poem_num


if __name__ == '__main__':
    f_qts_words = './python_exercise_data/qts_zh_simplified.txt'
    full_word_freq, author_counter, author_word_freq, poem_total_num = cut_qts_to_words(f_qts_words)

    print('诗词总篇数为： ' + str(poem_total_num))
    draw(author_word_freq['李白'], '李白top30字频统计', 30)
    draw(author_word_freq['孟浩然'], '孟浩然top30字频统计', 30)
    draw(full_word_freq, '全局top30字频统计', 30)
    draw(author_counter, '作诗数量top30统计', 30)

from os import register_at_fork
from count_words import count_words
import MeCab

def observatory(perspective_word, data_list):
    mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    mecab.parse('')  # 文字列がGCされるのを防ぐ
    result = []
    cnt = 1
    proprietary_noun_tag_cnt = {}

    all_page_cnt = len(data_list)
    # タグ毎の繰り返し
    for article_data in data_list:

        collaboration_cnt = {}
        proprietary_noun_page_cnt = {}
        tag = article_data["tag"]
        article_word_list = []
        # タグの記事の繰り返し
        for article in article_data["body"]:
            article = article.replace("\n", "")
            word_list = []

            count_words(mecab.parseToNode(article), word_list, proprietary_noun_page_cnt)
            article_word_list.append(word_list)
            # 領域名が記事に含まれているか
            if perspective_word in article:

                #　領域名が固有名詞判定を受けているか。受けていなかった場合、その単語のカウントをする必要がある
                if perspective_word not in word_list:
                    if perspective_word not in proprietary_noun_page_cnt.keys():
                        proprietary_noun_page_cnt[perspective_word] = 0

                    proprietary_noun_page_cnt[perspective_word] += 1

                # 領域名とそれぞれの固有名詞の共起回数をふやす
                for word in word_list:
                    if perspective_word == word:
                        continue

                    if perspective_word + word not in collaboration_cnt.keys():
                        collaboration_cnt[perspective_word + word] = 0

                    collaboration_cnt[perspective_word + word] += 1
        
        relation_r = []
        # 関連語の計算
        for word in proprietary_noun_page_cnt.keys():
            if word == perspective_word:
                continue

            # 固有名詞と領域名が共起されているか判定し、共起されていたら関係度を計算する
            if perspective_word + word not in collaboration_cnt.keys():
                relation_r.append([word, 0])
            else:
                #print(collaboration_cnt[perspective_word + word] ** 2, proprietary_noun_page_cnt[word], proprietary_noun_page_cnt[perspective_word])
                relation_r.append([word, collaboration_cnt[perspective_word + word] ** 2 / (proprietary_noun_page_cnt[word] * proprietary_noun_page_cnt[perspective_word])])
        
        relation_r = sorted(relation_r, reverse = True, key=lambda x: x[1])
        s_v = []

        print("OK1")
        for word in relation_r[:5]:
            s_v.append(word[0])

        collaboration_cnt = {}
        for article_words in article_word_list:
            for r in s_v:
                if r not in article_words:
                    continue

                for word in article_words:
                    if r == word:
                        continue

                    if r + word not in collaboration_cnt.keys():
                        collaboration_cnt[r + word] = 0
                    
                    collaboration_cnt[r + word] += 1
        print("OK2")
        topic = {}
        for word in proprietary_noun_page_cnt.keys():
            for r in s_v:
                if r + word not in collaboration_cnt.keys():
                    continue
                
                if word not in topic.keys():
                    topic[word] = 0
                
                topic[word] = topic[word] * collaboration_cnt[r + word] / proprietary_noun_page_cnt[word] if topic[word] != 0 else collaboration_cnt[r + word] / proprietary_noun_page_cnt[word]
        
        topic = sorted(topic.items(), reverse = True, key=lambda x: x[1])
        topic_words = []
        for word in topic[:20]:
            topic_words.append(word[0])

        result.append({
            "tag": tag,
            "topic_words":topic_words
        })

        # そのタグに使用された固有名詞をカウントする
        for word in proprietary_noun_page_cnt.keys():
            if word not in proprietary_noun_tag_cnt.keys():
                proprietary_noun_tag_cnt[word] = 0
            
            proprietary_noun_tag_cnt[word] += 1
        
        print(str(cnt) + "/" + str(len(data_list)))
        cnt += 1

    for value in result:
        word_difficulty = []
        for word in value["topic_words"]:
            word_difficulty.append([word, (all_page_cnt - proprietary_noun_tag_cnt[word]) / all_page_cnt])
        
        value["words_difficulty"] = word_difficulty
        

    return result

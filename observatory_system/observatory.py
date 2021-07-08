from count_words import count_words
from words_collaboration_count import words_collaboration_count
import MeCab

def observatory(perspective_word, data_list, tags_words_data):
    mecab = MeCab.Tagger('-d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')
    mecab.parse('')  # 文字列がGCされるのを防ぐ
    result = []
    cnt = 1
    proprietary_noun_tag_cnt = {}

    all_tag_cnt = len(data_list)
    page_word_cnt = {}

    # タグ毎の繰り返し
    for article_data in data_list:

        collaboration_cnt = {}
        proprietary_noun_page_cnt = {}
        tag = article_data["tag"]
        article_word_list = []
        page_word_cnt[tag] = len(article_data["body"])

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

        # 観点語集合を構成する
        s_v = [perspective_word]
        for word in relation_r[:5]:
            s_v.append(word[0])

        # 観点語集合とその他の単語の共起回数を求める
        collaboration_cnt = words_collaboration_count(article_word_list, s_v)
                    
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

        topic_words_count = {}
        for word in topic_words:
            topic_words_count[word] = proprietary_noun_page_cnt[word]
        
        result.append({
            "tag": tag,
            "word_appearance_count": topic_words_count,
            "word_count": len(proprietary_noun_page_cnt.keys()),
            "pro_t_tmax": {}
        })


        # そのタグに使用された固有名詞をカウントする
        for word in proprietary_noun_page_cnt.keys():
            if word not in proprietary_noun_tag_cnt.keys():
                proprietary_noun_tag_cnt[word] = 0
            
            proprietary_noun_tag_cnt[word] += 1
        
        tags_words_data[tag] = article_word_list
        print(str(cnt) + "/" + str(len(data_list)))
        cnt += 1
    
    # それぞれのタグの特徴語の難易度を計算
    for value in result:
        word_difficulty = []
        for word in value["word_appearance_count"].keys():
            word_difficulty.append({
                "word": word, 
                "word_difficulty": (all_tag_cnt - proprietary_noun_tag_cnt[word]) / all_tag_cnt
            })
        
        value["words_difficulty"] = sorted(word_difficulty, reverse = True, key=lambda x: x["word_difficulty"])
        
    return result

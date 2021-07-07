
def count_words(text, word_list, page_cnt): 
    POS = ["動詞", "名詞", "形容詞", "形容動詞"]
    
    while text:
        # 単語を取得
        word = text.surface
        # 品詞を取得
        pos = text.feature.split(",")[0]
        
        # 単語かどうかの判定
        if pos in POS:

            # 固有名詞かどうかの判定
            if text.feature.split(",")[1] == "固有名詞":
                
                # 辞書にキーがあるかどうかの判定
                if word not in word_list:
                    word_list.append(word)

                    if word not in page_cnt.keys():
                        page_cnt[word] = 0
                    page_cnt[word] += 1

        text = text.next

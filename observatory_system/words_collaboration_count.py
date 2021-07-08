
def words_collaboration_count(article_word_list, word_list):
    collaboration_cnt = {}
    for article_words in article_word_list:
        for r in word_list:
            if r not in article_words:
                continue

            for word in article_words:
                if r == word:
                    continue

                if r + word not in collaboration_cnt.keys():
                    collaboration_cnt[r + word] = 0
                    
                collaboration_cnt[r + word] += 1
    
    return collaboration_cnt
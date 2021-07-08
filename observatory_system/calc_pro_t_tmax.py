def calc_pro_t_tmax(topic_words_data, tags_words_data):

    for tag_data in topic_words_data:
        tag = tag_data["tag"]
        max_difficuluty_word = tag_data["words_difficulty"][0]["word"]
        words_count = {}

        for word_data in tag_data["words_difficulty"]:
            words_count[word_data["word"]] = 0
        
        for word_list in tags_words_data[tag]:
            for word in tag_data["word_appearance_count"].keys():
                if max_difficuluty_word in word_list or (max_difficuluty_word not in word_list and word in word_list):
                    words_count[word] += 1
        
        for word in tag_data["word_appearance_count"]:
            if word == max_difficuluty_word:
                continue

            tag_data["pro_t_tmax"][word] = words_count[word] / words_count[max_difficuluty_word]

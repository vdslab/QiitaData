from calc_pro_t_tmax import calc_pro_t_tmax

def calc_tags_difficulty(topic_words_data, tags_words_data):

    calc_pro_t_tmax(topic_words_data, tags_words_data)

    for tag_data in topic_words_data:
        max_difficulty_word = tag_data["words_difficulty"][0]["word"]
        max_difficulty = tag_data["words_difficulty"][0]["difficulty"]
        total = 0
        for word_data in tag_data["words_difficulty"]:
            if word_data["word"] == max_difficulty_word:
                continue

            total += word_data["difficulty"] * tag_data["pro_t_tmax"][word_data["word"]]
        tag_data["tag_difficulty"] = total + max_difficulty
        tag_data["numbers"] = []

    topic_words_data = sorted(topic_words_data, reverse = True, key=lambda x: x["tag_difficulty"])
    for i in range(len(topic_words_data)):
        topic_words_data[i]["numbers"].append(i + 1)
    
    topic_words_data = sorted(topic_words_data, reverse = True, key=lambda x: x["word_count"])
    for i in range(len(topic_words_data)):
        topic_words_data[i]["numbers"].append(i + 1)
    
    for tag_data in topic_words_data:
        tag_data["complexity"] = 20 - tag_data["numbers"][0] - tag_data["numbers"][1]
        del tag_data["numbers"]


    

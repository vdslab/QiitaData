import itertools

def set_best_permutation(topic_words_data, tags_word_dict, tag_list):
    best_permutation = {}
    max_score = 0
    all_topic_word = []
    for tag_data in topic_words_data:
        for topic in tag_data["word_appearance_count"].keys():
            all_topic_word.append(topic)
    
    all_topic_word = list(set(all_topic_word))

    for permutation in itertools.permutations(topic_words_data, len(topic_words_data)):
        total = 0

        for topic in all_topic_word:
            i = 0
            first, last, count = 0, 0, 0

            for tag_data in permutation:
                if topic in tags_word_dict[tag_data["tag"]]:
                    if first == 0:
                        first = i
                    else:
                        last = i
                    count += 1
                i += 1
            if last == 0:
                last = first

            total += count / (last - first + 1)
        
        if max_score < total:
            max_score = total
            best_permutation = permutation
            
    return best_permutation
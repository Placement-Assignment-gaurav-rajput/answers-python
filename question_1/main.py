# length of the highest-frequency word in a string.
from collections import Counter

from question_1.logger import logging


def most_freq_word_length(input_str: str) -> int:
    """
    :param input_str: a string that may contain repeated words
    :return: length of the most repeated word in the input string
    """
    try:
        logging.info(f"Input String: {input_str}")

        # Creating a list of words
        list_ = input_str.split(" ")

        # Creating a dictionary with keys as word and values as frequency of the word and sorting it on the frequency
        # of words in reverse order
        dict_ = {key_word: val_freq for key_word, val_freq in
                 sorted(Counter(list_).items(), key=lambda item: item[1], reverse=True)}
        logging.info(f"Dict of frequency of words: {dict_}")

        max_frequency_count, length = 0, 0

        # for logging the final list of words with max frequency
        final_dt = dict()

        for key, val in dict_.items():
            if max_frequency_count <= val and length <= len(key):
                max_frequency_count = val
                length = len(key)
                final_dt[key] = len(key)

        logging.info(
            f'Dict of length of most frequent word(s): {({k: v for k, v in sorted(final_dt.items(), key=lambda item: item[1], reverse=True)})}')

        logging.info(f"Returning max length as: {length} ")
        return length
    except Exception as e:
        raise Exception(e)
    

if __name__ == "__main__":
    print(most_freq_word_length("all the number from from from 1 to 100 hi hi hi hi write write write"))

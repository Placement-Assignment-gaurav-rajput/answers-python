import nltk
from collections import defaultdict
# from nltk.tokenize import word_tokenize
# from nltk.tag import pos_tag


nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')


def count_pos(text):
    """
    This function takes a string as input and returns a dictionary containing the count of each part of speech.
    """
    # Tokenize the text into words
    words = nltk.word_tokenize(text)
    
    # Tag each word with its part of speech
    tagged_words = nltk.pos_tag(words)
    
    # Initialize a dictionary to store the counts
    pos_counts = defaultdict(int)
    
    # Count the number of verbs, nouns, pronouns, and adjectives
    for word, tag in tagged_words:
        if tag.startswith('V'):
            pos_counts['verb'] += 1
        elif tag.startswith('N'):
            pos_counts['noun'] += 1
        elif tag.startswith('PR'):
            pos_counts['pronoun'] += 1
        elif tag.startswith('JJ'):
            pos_counts['adjective'] += 1
    
    return dict(pos_counts)

# Example usage
text = "The quick brown fox jumps over the lazy dog."
pos_counts = count_pos(text)
print(pos_counts)

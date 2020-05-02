import nltk
# nltk.download('state_union')
# nltk.download('averaged_perceptron_tagger')
from nltk.tokenize import sent_tokenize, word_tokenize
# from nltk.stem import PorterStemmer
# from nltk.corpus import state_union
# from nltk.tokenize import PunktSentenceTokenizer

text = word_tokenize("a carnivorous mammal long domesticated as a pet and for catching rats and mice")
tagged_sentence = nltk.pos_tag(text)
print(tagged_sentence)
edited_sentence = list()
bf = None
for word, tag in tagged_sentence:
    if tag != 'JJ' and tag != 'RB':
        if bf != 'CC' or tag != 'NN':
            edited_sentence.append(word)
            if tag == 'CC':
                bf = 'CC'
        else:
            edited_sentence.pop()
            bf = None
        

print(' '.join(edited_sentence))

# train_text = state_union.raw("2005-GWBush.txt")

# sample_text = state_union.raw("2006-GWBush.txt")

# custom_sent_tokenizer = PunktSentenceTokenizer(train_text)

# tokenized = custom_sent_tokenizer.tokenize(sample_text)

# def process_content():
#     try:
#         for i in tokenized:
#             words = nltk.word_tokenize(i)
#             tagged = nltk.pos_tag(words)
#             print(tagged)
#     except Exception as e:
#         print(str(e))

# process_content()

# example_text = "Hello Mr. Smith, how are you doing today? The weather is great and Python is awesome. The sky is pinkish blue."

# # print(sent_tokenize(example_text))

# # print(word_tokenize(example_text))

# #for i in word_tokenize

# ps = PorterStemmer()

# example_words = ["python", "pythoner", "pythonist", "pythoning", "pythoned"]

# for w in example_words:
#     print(ps.stem(w))

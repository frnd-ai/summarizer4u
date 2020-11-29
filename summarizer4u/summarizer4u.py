import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import subprocess
try:
    import en_core_web_sm
except:
    print("model not found")
    print("downloading model...")
    # os.system("python -m spacy download en_core_web_sm >> responses.text")
    subprocess.check_output('python -m spacy download en_core_web_sm >> respose.txt', shell=True)

from heapq import nlargest
import sys
import en_core_web_sm
stopwords = list(STOP_WORDS)

def summary(document1):
    nlp = en_core_web_sm.load()
    if sys.version_info[0] >= 3:
        docx = nlp(document1)
    else:
        docx = nlp(unicode(document1, "utf-8"))
    mytokens = [token.text for token in docx]
    word_frequencies = {}
    for word in docx:
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
                word_frequencies[word.text] += 1
    maximum_frequency = max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word]/maximum_frequency)
    sentence_list = [ sentence for sentence in docx.sents ]
    sentence_scores = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    sentence_scores[sent] += word_frequencies[word.text.lower()]
                    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
                    final_sentences = [ w.text for w in summarized_sentences ]
                    summary = ' '.join(final_sentences)
    return(summary)

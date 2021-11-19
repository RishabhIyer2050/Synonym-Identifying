'''Semantic Similarity: starter code

Author: Michael Guerzhoy. Last modified: Nov. 14, 2016.
'''

import math
import time


def norm(vec):
    '''Return the norm of a vector stored as a dictionary,
    as described in the handout for Project 3.
    '''
    
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    res = 0
    for i in vec1.keys():
        for j in vec2.keys():
            if i == j:
                res += vec1[i]*vec2[j]
    res = res/(norm(vec1)*norm(vec2))
    return res

def build_semantic_descriptors(sentences):
    d = {}

    for sentence in sentences:
        for word in set(sentence):
            if word in d.keys():
                for word_add in set(sentence):
                    if word_add != word:
                        if word_add in d[word].keys():
                            d[word].update({word_add: d[word][word_add]+1})
                        else:
                            d[word].update({word_add: 1})
            else:
                d.update({word: {}})
                for word_add in set(sentence):
                    if word_add != word:
                        d[word].update({word_add: 1})
    return d

def build_semantic_descriptors_from_files(filenames):
    sentences = []
    words = []
    for name in filenames:
        text = open(name, encoding="latin-1").read()

        text = text.lower()
        text = text.replace("--", " ").replace('\n', " ").replace('\t', " ")
        text = text.replace(",", "").replace("-", " ").replace(":", "").replace(";", "").replace("!",".").replace("?",".")
        
        for j in text.split("."):
            for k in j.split(" "):
                if k != "":
                    words.append(k)
            sentences.append(words)
            words = []

    res = build_semantic_descriptors(sentences)
    return res 

def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    maxv = -1
    maxc = 0
    count = 0

    for w in choices:
        if w not in semantic_descriptors.keys() or word not in semantic_descriptors.keys():
            curr = -1
        else:
            curr = similarity_fn(semantic_descriptors[word], semantic_descriptors[w])
        
        if curr>maxv:
            maxv = curr
            maxc = count
        count +=1
    
    return choices[maxc]
        

def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    text = open(filename, encoding="latin-1").read()
    words = []
    fin_sentences = []
    count =0

    sentences = text.split("\n")
    
    for i in sentences:
        for k in i.split(" "):
                if k != "":
                    words.append(k.lower())
        fin_sentences.append(words)
        words = []
    
    for i in range(0, len(sentences)):
        res = most_similar_word(fin_sentences[i][0], fin_sentences[i][2:], semantic_descriptors, similarity_fn)
        if res == fin_sentences[i][1]:
            count += 1
    
    return (count*100)/len(sentences)

if __name__ == "__main__":
    
    desc = build_semantic_descriptors_from_files(["book2.txt", "book1.txt"])
    res  = run_similarity_test("P3test.txt", desc, cosine_similarity)
    print(res, "of the guesses were correct")
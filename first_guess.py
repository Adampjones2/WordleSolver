# -*- coding: utf-8 -*-
"""
Created on Mon May  2 12:01:53 2022

@author: adamp
"""
from progress.bar import Bar
import statistics
from datetime import datetime
possible_words = []

fin = open('C:\\Users\\adamp\\Downloads\\words.txt')
for line in fin:
    word = line.strip()
    if len(word) == 5:
        possible_words.append(word)
fin.close()        

#%%
def reduce_possibilities(comp_results, word_list):
    for character in comp_results:
        if character[2] == 'green':
            word_list = remove_green(character[0], character[1], word_list)
        if character[2] == 'orange':
            word_list = remove_orange(character[0], character[1], word_list)
        if character[2] == 'grey':
            word_list = remove_grey(character[0], word_list)
    return word_list
# DEF function that compares guess and answer and says whether each letter is 
# grey orange or green

def compare_guess_answer(answer: str, guess: str)-> list[list[str,int,str]]:
    letter_info = []
    for i in range(len(answer)):
        if guess[i] in answer:
            if guess[i] == answer[i]:
                colour = 'green' 
                index = i 
                letter = guess[i]
            else:
                colour= 'orange' 
                index = i
                letter = guess[i]
        else:
            colour = 'grey'
            index = 6
            letter = guess[i]
        letter_info.append([letter, index, colour])
    return letter_info
    

# DEF function that removes words with certain letter from possible words

def remove_grey(letter: str, word_list: list[str]) -> list[str]:
    '''remove words that contain the grey letter from the list of
    possible words
    '''
    new_list = [word for word in word_list if letter not in word]
    return new_list

# DEF function for green letters

def remove_green(letter:str, index: int, word_list: list[str]) -> list[str]:
    '''removes words that don't have the green letter in that spot from
    the list of possible words
    '''
    new_list = [words for words in word_list if words[index] == letter]
    return new_list


# DEF function for orange letters

def remove_orange(letter: str, index: int, word_list: list[str]) -> list[str]:
    '''remove words that have the orange letter in that place and
    also remove words that don't contain the orange letter at all
    '''
    #remove words with letter in that place
    new_list = [words for words in word_list if words[index] != letter]
    # remove words that don't have that letter
    new_list2 = [words for words in new_list if letter in words]
    return new_list2

def letter_frequency(word_list: list[str]) -> dict:
    letter_freq = dict()
    for word in word_list:
        for letter in word:
            if letter not in letter_freq:
                letter_freq[letter] = 1
            else:
                letter_freq[letter] = letter_freq[letter] + 1
    return letter_freq

def word_scorer(word, letter_freqs):
    letter_frequencies = dict()
    word_score = 0
    for letter in word:
        if letter in letter_frequencies:
            letter_frequencies[letter] += 1
        else:
            word_score += letter_freqs[letter]
            letter_frequencies[letter] = 1
    return word_score

word_scores = dict()            
for word in possible_words:
    word_scores[word] = word_scorer(word, letter_frequency(possible_words))
    
            
#%%
word_scores = dict()            
for word in possible_words:
    word_scores[word] = word_scorer(word, letter_frequency(possible_words))
   
candidates = sorted(word_scores, key = word_scores.get)[-1:-100:-1]


def choose_first_word(poss_words):
    word_scores = dict()
    for word in poss_words:
        no_ruled_out = []
        for wrds in poss_words:
            guess_results = compare_guess_answer(wrds, word)
            rem_possible_words = reduce_possibilities(guess_results, poss_words)
            no_ruled_out.append(len(poss_words) - len(rem_possible_words))
        word_scores[word] = statistics.mean(no_ruled_out)
    return max(word_scores)

def choose_first_word2(poss_words, candidates):
    word_scores = dict()
    bar = Bar('Processing', max = len(candidates))
    for word in candidates:
        no_ruled_out = []
        for wrds in poss_words:
            guess_results = compare_guess_answer(wrds, word)
            rem_possible_words = reduce_possibilities(guess_results, poss_words)
            no_ruled_out.append(len(poss_words) - len(rem_possible_words))
        word_scores[word] = statistics.mean(no_ruled_out)
        bar.next()
    bar.finish()
    return max(word_scores, key = word_scores.get), word_scores, no_ruled_out

start_time = datetime.now().strftime("%H:%M:%S")     
print(start_time)

x = choose_first_word2(possible_words, candidates)
print('\n', x[0])

end_time =  datetime.now().strftime("%H:%M:%S") 
print(end_time)
# -*- coding: utf-8 -*-
"""
Created on Tue May 24 18:45:35 2022

@author: adamp
"""

from progress.bar import Bar
import matplotlib.pyplot as plt


def reduce_possibilities(comp_results, word_list, green_letters):
    for character in comp_results:
        if character[2] == 'green':
            word_list = remove_green(character[0], character[1], word_list)
            green_letters.setdefault(character[0],[]).append(character[1])
            green_letters[character[0]] = list(set(green_letters[character[0]]))
        if character[2] == 'orange':
            word_list = remove_orange(character[0], character[1], word_list)
        if character[2] == 'grey':
            word_list = remove_grey(character[0], word_list)
    return word_list, green_letters
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

# DEF function to count frequency of letters in list

def letter_frequency(word_list: list[str]) -> dict:
    letter_freq = dict()
    for word in word_list:
        for letter in word:
            if letter not in letter_freq:
                letter_freq[letter] = 1
            else:
                letter_freq[letter] = letter_freq[letter] + 1
    return letter_freq

def word_chooser(freq_dict: dict, word_list: list, green_letters: dict)-> str:
    word_scores = []
    letters_so_far = []
    for word in word_list:
        score = 0
        for i in range(len(word)):
            if not (word[i] in green_letters and i in green_letters[word[i]]):
                if not word[i] in letters_so_far:
                    score += freq_dict[word[i]]
        word_scores.append(score)
        letters_so_far.append(word[i])
    return word_list[word_scores.index(max(word_scores))]

def word_chooser2(possible_answers: list, possible_guesses: list, green_letters: dict) -> str:
    """
    After inputting todays wordle answer and your starting guess, along with 
    the list of valid words this function returns the answer along with the
    number of guesses taken and a list of the guesses made.
    """
    no_reduced = dict()
    for guess in possible_guesses:
        for ans in possible_answers:
            guess_results = compare_guess_answer(ans, guess)
            rem_possible_words = reduce_possibilities(guess_results, possible_answers)
        no_reduced[guess] = len(possible_answers) - len(rem_possible_words)
    return no_reduced


def wordle_solver(answer: str, starting_guess: str, valid_words: list) -> tuple():
    """
    After inputting todays wordle answer and your starting guess, along with 
    the list of valid words this function returns the answer along with the
    number of guesses taken and a list of the guesses made.

    """
    guesses = [starting_guess]
    possible_words = valid_words
    green_letters = dict()
    for i in range(6):
        if guesses[i] == answer:
            return ("Correct", answer, i+1, guesses)
        guess_results = compare_guess_answer(answer, guesses[i])
        possible_words, green_letters = reduce_possibilities(guess_results, possible_words, green_letters)
        next_guess = word_chooser(letter_frequency(possible_words), possible_words, green_letters)
        guesses.append(next_guess)
    return ("Failed", answer, None, guesses)





initial_possible_words = []
fin = open('C:\\Users\\adamp\\Downloads\\words.txt')
for line in fin:
    word = line.strip()
    if len(word) == 5:
        initial_possible_words.append(word)
        
wordle_solver('alias', 'lares', initial_possible_words)

wordle_solutions = []
bar = Bar('Processing', max = len(initial_possible_words))
for word in initial_possible_words:
    wordle_solutions.append(wordle_solver(word, 'lares', initial_possible_words))
    bar.next()
bar.finish()

failed_wordles = [wordle for wordle in wordle_solutions if wordle[0] == 'Failed']
successful_wordles = [wordle for wordle in wordle_solutions if wordle[0] == 'Correct']


plt.bar(["Successful", "Failed"], [len(successful_wordles), len(failed_wordles)])

guess_freq = dict()
for item in wordle_solutions:
    if str(item[2]) not in guess_freq:
        guess_freq[str(item[2])] = 1
    else:
        guess_freq[str(item[2])] += 1

plt.bar(list(guess_freq.keys()), list(guess_freq.values()))

failed_words = [word[1] for word in failed_wordles]
































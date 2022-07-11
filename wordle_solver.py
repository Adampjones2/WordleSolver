# -*- coding: utf-8 -*-
"""
Created on Sun May  1 11:59:21 2022

@author: adamp
"""
answer = 'acnes'

first_guess = 'lares'

initial_possible_words = []

fin = open('C:\\Users\\adamp\\Downloads\\words.txt')
for line in fin:
    word = line.strip()
    if len(word) == 5:
        initial_possible_words.append(word)
        
green_letters= dict()



# def function that takes results from compare and applies relevant function

def reduce_possibilities(comp_results, word_list):
    global green_letters
    for character in comp_results:
        if character[2] == 'green':
            word_list = remove_green(character[0], character[1], word_list)
            green_letters.setdefault(character[0],[]).append(character[1])
            green_letters[character[0]] = list(set(green_letters[character[0]]))
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

first_guess_results = compare_guess_answer(answer, first_guess)
first_possible_words = reduce_possibilities(first_guess_results, initial_possible_words)

if len(first_possible_words) == 1:
    print(f"{first_possible_words[0]} is the answer!")
# 2nd Guess
second_guess = word_chooser(letter_frequency(first_possible_words), first_possible_words, green_letters)
second_guess_results = compare_guess_answer(answer, second_guess)
second_possible_words = reduce_possibilities(second_guess_results, first_possible_words)

if len(second_possible_words) == 1:
    print(f"{second_possible_words[0]} is the answer!")
# 3rd Guess
third_guess = word_chooser(letter_frequency(second_possible_words), second_possible_words, green_letters)
third_guess_results = compare_guess_answer(answer, third_guess)
third_possible_words = reduce_possibilities(third_guess_results, second_possible_words)

if len(third_possible_words) == 1:
    print(f"{third_possible_words[0]} is the answer!")
# 4th Guess    
fourth_guess = word_chooser(letter_frequency(third_possible_words), third_possible_words, green_letters)
fourth_guess_results = compare_guess_answer(answer, fourth_guess)
fourth_possible_words = reduce_possibilities(fourth_guess_results, third_possible_words)

if len(fourth_possible_words) == 1:
    print(f"{fourth_possible_words[0]} is the answer!")
# Fifth Guess
fifth_guess = word_chooser(letter_frequency(fourth_possible_words), fourth_possible_words, green_letters)
fifth_guess_results = compare_guess_answer(answer, fifth_guess)
fifth_possible_words = reduce_possibilities(fifth_guess_results, fourth_possible_words)

if len(fifth_possible_words) == 1:
    print(f"{fifth_possible_words[0]} is the answer!")
# 6th Guess

if len(fifth_possible_words) == 1:
    sixth_guess = fifth_possible_words[0]
    print(f"{fifth_possible_words[0]} is the answer!")
else:
    print("You were unsuccessful!")

    
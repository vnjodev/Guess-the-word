"""
Guess-My-Word is a game where the player has to guess a word.

This is a simple word guessing game where Players have six attempts to guess a five-letter word, with feedback given for each guess in the form of colored tiles indicating when letters match or occupy the correct position

Author: Lemuel Madula
Company: TAFE
Copyright: 2024
Version: 0.1

"""

import random

MISS = 0  # _-.: letter not found ⬜
MISPLACED = 1  # O, ?: letter in wrong place 🟨
EXACT = 2  # X, +: right letter, right place 🟩

MAX_ATTEMPTS = 6
WORD_LENGTH = 5

ALL_WORDS = "./word-bank/all_words.txt"
TARGET_WORDS = "./word-bank/target_words.txt"


def play():
    """Code that controls the interactive game play"""
    print("**** WORD GUESSING GAME **** \nYou have 6 attempts to guess the word!")
    # select a word of the day:
    word_of_the_day = get_target_word()
    # build a list of valid words (words that can be entered in the UI):
    valid_words = get_valid_words()

    attempts = 0
    guess_remaining = MAX_ATTEMPTS
    while attempts < MAX_ATTEMPTS:
        guess = ask_for_guess(valid_words)
        score = score_guess(guess, word_of_the_day)
        
        print("Result of your guess:")
        print(format_score(guess, score))
        
        if is_correct(score):
            word_of_the_day = word_of_the_day.upper()
            if attempts == 1:
                print(f"Congratulations!You've guessed the word '{word_of_the_day}'! You've achieved an ACE!")
            else:
                print(f"Congratulations! You've guessed the word '{word_of_the_day}'!")
            break
            
        attempts += 1
        guess_remaining -= 1
        
        if guess_remaining == 1:
            print(f"You have {guess_remaining} guess remaining")
        else:
            print(f"You have {guess_remaining} guesses remaining")
            
    if attempts == MAX_ATTEMPTS:
        word_of_the_day = word_of_the_day.upper()
        print(f"Sorry, you've run out of attempts. The word was '{word_of_the_day}'.")
        
    #Play again feature
    play_again() 

def play_again():   
    choices = ["yes", "no", "y", "n"]
    
    while True:
        replay = input("Do you want to play again? (y/n): ").lower()
        if replay == 'y' or replay == 'yes':
            play()
        elif replay not in choices:
            print("Invalid input.")
        elif replay == 'n' or replay == 'no':
            return print("Thank you for playing!")
        


def is_correct(score):
    """Checks if the score is entirely correct and returns True if it is
    Examples:
    >>> is_correct((1,1,1,1,1))
    False
    >>> is_correct((2,2,2,2,1))
    False
    >>> is_correct((0,0,0,0,0))
    False
    >>> is_correct((2,2,2,2,2))
    True
    """
    #Loops through the items in the score is entirely EXACT and returns True if it is. 
    for items in score:
        if items != EXACT:
            return False
    return True


def get_valid_words(file_path=ALL_WORDS):
    """returns a list containing all valid words.
    Note to test that the file is read correctly, use:
    >>> get_valid_words()[0]
    'aahed'
    >>> get_valid_words()[-1]
    'zymic'
    >>> get_valid_words()[10:15]
    ['abamp', 'aband', 'abase', 'abash', 'abask']

    """
    # read words from files and return a list containing all words that can be entered as guesses
    valid_words_file = open(file_path, "r")
    valid_words_list = []
    for valid_word in valid_words_file:
        valid_word = valid_word.strip()
        valid_words_list.append(valid_word)
        
    return valid_words_list


def get_target_word(file_path=TARGET_WORDS, seed=None):
    """Picks a random word from a file of words

    Args:
        file_path (str): the path to the file containing the words

    Returns:
        str: a random word from the file

    >>> get_target_word()
    'aback'
    >>> get_target_word()
    'zonal'

    """ 
    # read words from a file and return a random word (word of the day)
    with open(file_path, "r") as target_file:
        target_word = target_file.read().splitlines()
         
    return random.choice(target_word)


def ask_for_guess(valid_words):
    """Requests a guess from the user directly from stdout/in
    Returns:
        str: the guess chosen by the user. Ensures guess is a valid word of correct length in lowercase
    """
    while True:
        user_guess = input("Enter your guess (5 letters): ").lower()
        if user_guess == "help".lower():
            help()
        elif user_guess not in valid_words or len(user_guess) != WORD_LENGTH:
            print("Invalid guess.")
        else:
            return user_guess
            
            
def score_guess(guess, target_word):
    """given two strings of equal length, returns a tuple of ints representing the score of the guess
    against the target word (MISS, MISPLACED, or EXACT)
    Here are some example (will run as doctest):

    >>> score_guess('hello', 'hello')
    (2, 2, 2, 2, 2)
    #>>> score_guess('drain', 'float')
    #(0, 0, 1, 0, 0)
    #>>> score_guess('hello', 'spams')
    #(0, 0, 0, 0, 0)

    # Try and pass the first few tests in the doctest before passing these tests.
    # >>> score_guess('gauge', 'range')
    # (0, 2, 0, 2, 2)
    # >>> score_guess('melee', 'erect')
    # (0, 1, 0, 1, 0)
    # >>> score_guess('array', 'spray')
    # (0, 0, 2, 2, 2)
    # >>> score_guess('train', 'tenor')
    # (2, 1, 0, 0, 1)
    # >>> score_guess('verve', 'serve')
    # (0, 2, 2, 2, 2)
    # >>> score_guess('trust', 'truth')
    # (2, 2, 2, 0, 1)
    # >>> score_guess ('groom', 'roomy')
    # (0, 1, 2, 1, 1)
    # >>> score_guess('roomy', 'groom')
    # (1, 1, 2, 1, 0)
    # >>> score_guess ('hello', 'world')
    """
    
    guess_result = [0, 0, 0, 0, 0]
    
    if guess == target_word:
        guess_result = [2, 2, 2, 2, 2]
        return tuple(guess_result)
            
    #loop over each leter in the guess
    for letter in range(len(guess)):
        #check for exact matches
        if guess[letter] == target_word[letter]:
            guess_result[letter] = EXACT  # mark the letter as an exact match           
            guess = guess[:letter] + ' ' + guess[letter+1:] # Replace the exact letter in guess with space to avoid duplicates
            target_word = target_word[:letter] + ' ' + target_word[letter+1:] # Replace the exact letter in target word with space to avoid duplicates
            
    #Find matches for the remaining letters
    for letter in range(len(guess)):
        if guess[letter] != target_word[letter] and guess[letter] in target_word:#check for partial matches
            index = target_word.index(guess[letter])  # Find the index of the matching letter in target_word
            target_word = target_word[:index] + ' ' + target_word[index+1:]  # Mark the letter as found in target_word
            guess_result[letter] = MISPLACED  # Update guess_result for this letter
            
    return tuple(guess_result)


def help():
    """Provides help for the game"""
    
    user_help = print("HOW TO PLAY \nEach guess must be a valid five-letter word.\nIf the tile is green 🟩, the letter is in the word and it is in the correct spot. \nIf the tile is orange  🟨, the letter is in the word, but it is not in the correct spot. \nIf the tile is white ⬜, the letter is not in the word.")
    
    return user_help
        

def format_score(guess, score):
    """Formats a guess with a given score as output to the terminal.
    >>> print(format_score('hello', (0,0,0,0,0)))
     H   E   L   L   O
    ⬜  ⬜  ⬜  ⬜  ⬜
    >>> print(format_score('hello', (0,0,0,1,1)))
     H   E   L   L   O
    ⬜  ⬜  ⬜  🟨  🟨
    >>> print(format_score('hello', (1,0,0,2,1)))
     H   E   L   L   O
    🟨  ⬜  ⬜  🟩  🟨
    >>> print(format_score('hello', (2,2,2,2,2)))
     H   E   L   L   O
    🟩  🟩  🟩  🟩  🟩
    """
    guess_format = '   '.join(guess.upper())
    score_format = ''
    
    for item in score:
        if item is EXACT:
            score_format += "🟩  "
        elif item == MISPLACED:
            score_format += "🟨  "  
        else:
            score_format += "⬜  "
            
    format = f"{guess_format.center(20)} \n{score_format}"     
    
    return format

def main(test=True):
    if test:
        import doctest
        return doctest.testmod()
    play()

if __name__ == '__main__':
    #print(main(test=True))
    print(play())
    #play()

        
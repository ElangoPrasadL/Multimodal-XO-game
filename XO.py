
import random
import pyttsx3
engine = pyttsx3.init(driverName='sapi5')
#rate = engine.getProperty('rate')   # getting details of current speaking rate
#print (rate)                        #printing current voice rate
#engine.setProperty('rate', 125) #changing rate according to preference
import numpy as np
import phonetics
import keyboard
from googletrans import Translator
import speech_recognition as sr
r = sr.Recognizer()
voice_enabled = True
rules_enabled = False
advanced_enabled = False
saved_settings = False
text_enabled = True
y_n_decision = {'yes': True, 'no': False}
symbol = {'x': 'x', 'o': 'o'}
player_symbol = ''
computer_symbol = ''





numbers = {'one': 1, 'two':2, 'Tu':2,'three': 3,'tree':3, 'four':4, 'five':5, 'six':6, 'seven':7, 'eight':8, 'nine':9}

def onStartWord(name, location, length): #can be used to stop the engine mid-sentence
    print ('word', name, location, length)
    if keyboard.is_pressed("esc"):
       engine.stop()

def levenshtein(code1, code2):
    #to calculate minimum distance between two strings based on number of positional changes
    size1 = len(code1) + 1
    size2 = len(code2) + 1
    matrix = np.zeros ((size1, size2))
    for x in range(size1):
        matrix [x, 0] = x
    for y in range(size2):
        matrix [0, y] = y

    for x in range(1, size1):
        for y in range(1, size2):
            if code1[x-1] == code2[y-1]:
                matrix [x,y] = min(
                    matrix[x-1, y] + 1,
                    matrix[x-1, y-1],
                    matrix[x, y-1] + 1
                )
            else:
                matrix [x,y] = min(
                    matrix[x-1,y] + 1,
                    matrix[x-1,y-1] + 1,
                    matrix[x,y-1] + 1
                )
    return (matrix[size1 - 1, size2 - 1])

def get_phonetically_closest_word(list_of_words, voice_ip):
    word_distance = {}
    voice_ip = voice_ip.replace(" ", "")
    for x in list_of_words:
        distance = levenshtein(phonetics.nysiis(text), phonetics.nysiis(x)) * 0.25 \
                    + levenshtein(phonetics.soundex(text), phonetics.soundex(x)) * 0.25 \
                    + levenshtein(phonetics.dmetaphone(text)[0], phonetics.dmetaphone(x)[0]) * 0.25\
                    + levenshtein(phonetics.metaphone(text), phonetics.nysiis(x)) * 0.25
        #print('dist='+str(distance))
        word_distance[x] = distance 
    closest_word = min(word_distance, key=lambda key: word_distance[key])
    return closest_word

def get_phonetic_distance(word, voice_ip):
    voice_ip = voice_ip.replace(" ", "")
    distance = levenshtein(phonetics.nysiis(text), phonetics.nysiis(word)) * 0.25 \
                    + levenshtein(phonetics.soundex(text), phonetics.soundex(word)) * 0.25 \
                    + levenshtein(phonetics.dmetaphone(text)[0], phonetics.dmetaphone(word)[0]) * 0.25\
                    + levenshtein(phonetics.metaphone(text), phonetics.nysiis(word)) * 0.25
    #print(distance)
    return distance

def get_player_symbol():
    global voice_enabled
    global text
    ip_symbol = ''
    while True:
        if(voice_enabled):
            try:
                while True:
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=1)
                        engine.say('What do you want your symbol to be? Say X or O or repeat')
                        engine.runAndWait()
                        voice_input = r.listen(source, phrase_time_limit = 5)
                        text = r.recognize_google(voice_input)
                        print(text)
                        if get_phonetic_distance('repeat', text) < 2.0:
                            continue
                        else:
                            break               
                if text in symbol:
                    ip_symbol = symbol[text].upper()
                else:
                    if any(item in text for item in ['x','c']):
                        symbol[text] = 'x'
                    elif any(item in text for item in ['o']) :
                        symbol[text] = 'o'
                    ip_symbol = symbol[text].upper()
                op = 'You have selected ' + ip_symbol
                engine.say(op)
                engine.runAndWait()                                
            except:
                engine.say('Voice input was not clear')
                engine.runAndWait()
        else :
            print('What do you want your symbol to be? Enter x or o:')
            ip_symbol = input().upper()
            

        if ip_symbol == 'X':
            return ['X', 'O']
        elif ip_symbol == 'O':
            return ['O', 'X']

def decide_who_plays_first():
    if random.randint(0,1) == 0:
        return 'player'
    else:
        return 'computer'

def check_if_game_over(board, player):
    if ((board[7]== player and board[8]== player and board[9]== player) or
            (board[4] == player and board[5] == player and board[6] == player) or
            (board[1] == player and board[2] == player and board[3] == player) or
            (board[7] == player and board[4] == player and board[1] == player) or
            (board[8] == player and board[5] == player and board[2] == player) or
            (board[9] == player and board[6] == player and board[3] == player) or
            (board[7] == player and board[5] == player and board[3] == player) or
            (board[9] == player and board[5] == player and board[1] == player)):
            if player == player_symbol:
                if text_enabled:
                    print('Congratulations. You won')
                if voice_enabled:
                    engine.say('Congratulations. You won')
                    engine.runAndWait()
            else :
                if text_enabled:
                    print('You lost. Better luck next time')
                if voice_enabled:
                    engine.say('You lost. Better luck next time')
                    engine.runAndWait()
            return True
    else:
        for i in range(1, 10):
            if board[i] == ' ':
                return False
        if text_enabled:
            print('The game is a Tie.')
        if voice_enabled:
            engine.say('The game is Tie.')
            engine.runAndWait()
        return True

        
def check_if_move_wins(board, player):
    return((board[4] == player and board[5] == player and board[6] == player) or
           (board[1] == player and board[2] == player and board[3] == player) or
           (board[7] == player and board[4] == player and board[1] == player) or
           (board[8] == player and board[5] == player and board[2] == player) or
           (board[9] == player and board[6] == player and board[3] == player) or
           (board[7] == player and board[5] == player and board[3] == player) or
           (board[9] == player and board[5] == player and board[1] == player))

def get_copy_of_board(board):

    copy = []

    for i in board:
        copy.append(i)

    return copy

def get_player_move(board):
    global move
    move = 0
    while move not in numbers.values() :
        if voice_enabled :
            try:
                while True:
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=1)
                        engine.say('what is your next move? Say a number from 1 to 9 or repeat')
                        engine.runAndWait()
                        voice_input = r.listen(source, phrase_time_limit = 5)
                        text = r.recognize_google(voice_input)
                        print(text)
                        if get_phonetic_distance('repeat', text) < 2.0:
                            continue
                        else:
                            break
                if text in numbers:
                    move = numbers[text]
                else:
                    try:
                        if 0 < int(text) < 10:
                            move = int(text)
                    except:
                        move = numbers[get_phonetically_closest_word(numbers,text)]
                if board[move] != ' ':
                    engine.say('Error.You have selected '+ move + 
                                '. The number selected is already played. Redoing previous step')
                    engine.runAndWait()
                    move = 0
                else:
                    engine.say('You have selected '+ str(move))
                    engine.runAndWait()

            except:
                engine.say('Voice input was not clear')
                engine.runAndWait()
                move = 0
                
        else:
            print('what is your next move? Enter a number from 1-9:')
            move_str = input()
            move = int(move_str)
            if board[move] != ' ':
                move = 0
            
    return move

def get_computer_move(board, computer_symbol):

    for i in range(1, 10):
        copy = get_copy_of_board(board)
        if copy[i] == ' ':
            copy[i] = computer_symbol
            if check_if_move_wins(copy, computer_symbol):
                return i

    for i in range(1, 10):
        copy = get_copy_of_board(board)
        if copy[i] == ' ':
            copy[i] = player_symbol
            if check_if_move_wins(copy, player_symbol):
                return i


    corners_choice = [1,3,7,9]
    while True :
        move = random.choice(corners_choice)
        if board[move] == ' ':
            return move
        corners_choice.remove(move)


    if board[5] == ' ':
        return 5

    sides_choice = [2,4,6,8]
    while True :
        move = random.choice(sides_choice)
        if board[move] == ' ':
            return move
        sides_choice.remove(move)



def output_board(board):

    if voice_enabled and advanced_enabled == False:
        for i in range(1,10):
            if i == 1:
                engine.say('First row')
                engine.runAndWait()
            elif i == 4:
                engine.say('Second row')
                engine.runAndWait()
            elif i == 7:
                engine.say('Third row')
                engine.runAndWait()
            if(board[i] == ' '):
                engine.say('blank')
                engine.runAndWait()
            else:
                engine.say(board[i])
                engine.runAndWait()
    if text_enabled :
        print(board[1] + '|' + board[2] + '|' + board[3])
        print('_____')
        print(board[4] + '|' + board[5] + '|' + board[6])
        print('_____')
        print(board[7] + '|' + board[8] + '|' + board[9])
        print('_____')

def output_rules_of_the_game():
    op = 'The game is played on a grid that is s 3 squares by 3 squares. \
        You are X or O, your friend is the other symbol. Players take turns putting their marks in empty squares.\
        The first player to get 3 of their marks in a row either vertically, horizontally, or diagonally is the winner.\
        When all 9 squares are full, the game is over. If no player has 3 marks in a row, the game ends in a tie.'
    if voice_enabled:
        engine.say(op)
        engine.runAndWait()
    if text_enabled:
        print(op)

def select_yes_or_no(question):
    global voice_enabled
    global text
    while True:
        if(voice_enabled):
            try:
                while True:
                    with sr.Microphone() as source:
                        r.adjust_for_ambient_noise(source, duration=1) 
                        engine.say(question+'Say yes or no or repeat')
                        engine.runAndWait()
                        voice_input = r.listen(source, phrase_time_limit = 5)
                        text = r.recognize_google(voice_input)
                        #text = r.recognize_google(voice_input)
                        #print(text)
                        if get_phonetic_distance('repeat', text) < 2.0:
                            continue
                        else:
                            break
                if text in y_n_decision:
                    engine.say('You have selected ' + text)
                    engine.runAndWait()                 
                    return y_n_decision[text]
                else:
                    if any(item in text for item in ['s', 'e','a','y']):
                        engine.say('You have selected ' + list(y_n_decision.keys())[list(y_n_decision.values()).index(True)])
                        engine.runAndWait()
                        return True
                    elif any(item in text for item in ['n', 'o']):
                        engine.say('You have selected ' + list(y_n_decision.keys())[list(y_n_decision.values()).index(False)])
                        engine.runAndWait()
                        return False                
            except:
                engine.say('Voice input was not clear.')
                engine.runAndWait()
                
        else:
            print(question +'Enter yes or no:')
            return input().lower() == 'yes'

def main():
    global y_n_decision
    global voice_enabled, voice_change
    global text
    global XO_board
    global player_symbol, computer_symbol
    global rules_enabled, advanced_enabled, saved_settings, text_enabled
    read_settings = {}
    
    print('Welcome to Tic Tac Toe')


    
    '''p = Translator() 
    k = p.translate('Welcome to Tic Tac Toe', dest='german')
    translated = str(k.text)
    print(translated)'''

    engine.say('Welcome to Tic Tac Toe') # + translated)
    engine.runAndWait()    
    try:
        read_settings = np.load('settings.npy',allow_pickle='TRUE').item()
        voice_enabled = read_settings['voice_enabled']
        voice_change  = read_settings['voice_change']
        advanced_enabled = read_settings['advanced_enabled']
        rules_enabled = read_settings['rules_enabled']
        text_enabled = read_settings['text_enabled']
        player_symbol = read_settings['player_symbol']
        computer_symbol = read_settings['computer_symbol']
        saved_settings = select_yes_or_no('Do you want to use the saved settings?')            
    except:
        saved_settings = False
    if saved_settings == False:
        try:
            while True:
                r = sr.Recognizer()
                with sr.Microphone() as source:                
                    r.adjust_for_ambient_noise(source, duration=1)
                    engine.say('Do you want voice-enabled inputs and commands? Say yes or no or repeat')
                    engine.runAndWait()
                    voice_input = r.listen(source, phrase_time_limit = 5)
                    text = r.recognize_google(voice_input)
                    if get_phonetic_distance('repeat', text) < 2.0:
                        continue
                    else:
                        break
    
    
            if text in y_n_decision:
                voice_enabled = y_n_decision[text]
                engine.say('You have selected ' + text)
                engine.runAndWait()
            else:
                if any(item in text for item in ['s', 'e','a','y']):
                    y_n_decision[text] = True
                    engine.say('You have selected ' + list(y_n_decision.keys())[list(y_n_decision.values()).index(True)])
                    engine.runAndWait()
                elif any(item in text for item in ['n', 'o']):
                    y_n_decision[text] = False
                    engine.say('You have selected ' + list(y_n_decision.keys())[list(y_n_decision.values()).index(False)])
                    engine.runAndWait()
                voice_enabled = y_n_decision[text]
        except:
            text_enabled = True
            print('Do you want voice-enabled inputs and commands? Enter yes or no:')
            if input().lower() == 'no':
                voice_enabled = False
            else:
                voice_enabled = True
        '''voices = engine.getProperty('voices')
        if voice_enabled:
            for voice in voices: 
                print("Voice:") 
                print(" - ID: %s" % voice.id) 
                print(" - Name: %s" % voice.name) 
                print(" - Languages: %s" % voice.languages) 
                print(" - Gender: %s" % voice.gender) 
                print(" - Age: %s" % voice.age)'''
        if voice_enabled:
            voice_change = select_yes_or_no('Do you want to change the gender of the voice?')
        if voice_change:
            voices = engine.getProperty('voices')
            engine.setProperty('voice', voices[1].id)
        advanced_enabled = select_yes_or_no('Do you want to enable advanced mode?')
    
        if advanced_enabled == False:
            rules_enabled = select_yes_or_no('Do you want to know the rules of the game?')
    
        
        if rules_enabled:
            output_rules_of_the_game()
        player_symbol, computer_symbol = get_player_symbol()
        settings = {'voice_enabled': voice_enabled, 'voice_change': voice_change, 'advanced_enabled': advanced_enabled,\
                    'rules_enabled': rules_enabled, 'player_symbol': player_symbol, 'computer_symbol': computer_symbol,\
                    'text_enabled' : text_enabled}
        np.save('settings.npy', settings)


    while True:
        XO_board = [' '] * 20 #empty board
        global turn
        turn = decide_who_plays_first()
        op = 'The ' + turn + ' will go first'
        if voice_enabled:
            engine.say(op)
            engine.runAndWait()
        else:
            print(op)
        while True:
            if turn == 'player':
                move = get_player_move(XO_board)
                XO_board[move] = player_symbol
                if text_enabled:
                    print('Player move : ' + str(move))
                output_board(XO_board)
                if check_if_game_over(XO_board, player_symbol) == False:
                    turn = 'computer'
                else:
                    break                        
            else:
                if advanced_enabled:
                    move = get_computer_move(XO_board, computer_symbol)
                    if text_enabled:
                        print('Computer move: ' + str(move))
                    if move == None:
                        for i in range(1, 10):
                            if XO_board[i] == ' ':
                                move = int(i)
                                break
                    XO_board[move] = computer_symbol
                else:
                    for i in range(1, 10):
                        if XO_board[i] == ' ':
                            move = int(i)
                            if text_enabled:
                                print('Computer move: ' + str(move))
                            XO_board[move] = computer_symbol
                            break
                if voice_enabled:
                    engine.say('The computer selected :' + str(move))
                    engine.runAndWait()
                output_board(XO_board)
                if check_if_game_over(XO_board, computer_symbol) == False:
                    turn = 'player'
                else:
                    break

        if not select_yes_or_no('Do you want to play again?'):
            if voice_enabled:
                engine.say('See you next time')
                engine.runAndWait()
            if text_enabled:
                print('See you next time')
            break

if __name__ == "__main__":
    main()

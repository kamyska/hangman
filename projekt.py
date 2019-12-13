from random import randrange
from datetime import datetime

game_counter = 0
name = ''
diff = 0
over = 0
lost = 0


def hello():
    global name
    print('Witaj w grze SZUBIENICA!')
    name = input('Podaj swoje imię: ')


def select_difficulty():
    print('Wybierz poziom gry:\n''1 - łatwy        2 - średni        3 - trudny\nWyjść z gry możesz wybierając 0\n')
    global diff
    while diff == 0:
        choice = input()
        if choice == '1':
            diff = 1
        elif choice == '2':
            diff = 2
        elif choice == '3':
            diff = 3
        elif choice == '0':
            print('\n***** Dziękuję za grę :) *****\n')
            exit()
        else:
            print('Niepoprawny wybór, wybierz jeszcze raz')


def create_dictionary():
    list = read_file('lista.txt')
    words = [n for n in list.split("\n")]
    dictionary = dict()
    for word in words:
        if '*' in word:
            category = word.replace('*', '')
        else:
            dictionary[word] = category
    return dictionary


def pick_word(dictionary):
    new_dict = {}
    for word in dictionary:
        if (diff == 1 and len(word) <= 7) or \
                (diff == 2 and 7 < len(word) <= 13) or \
                (diff == 3 and len(word) > 13):
            new_dict[word] = dictionary[word]
    selected_word = random_word(new_dict)
    category = new_dict[selected_word]
    dictionary.pop(selected_word)
    return selected_word, category


def random_word(dictionary):
    index = randrange(0, len(dictionary))
    new_list = list(dictionary)
    word = new_list[index]
    return word


def play(word, category):
    global game_counter
    global lost
    lost = 0
    moves = 0
    word = word.upper()
    output = create_output(word)
    print_screen(0, output, category)
    error = 0
    while '_' in output:
        if error < 6:
            error, moves, output = continue_playing(error, moves, output, word, category)
        else:
            lost = 1
            game_counter += 1
            export_stats(calc_statisics(error, moves, word))
            game_lost(word)
            break
    if lost == 0:
        game_counter += 1
        export_stats(calc_statisics(error, moves, word))
        game_won()

    return output, error


def continue_playing(error, moves, output, word, category):
    letter = ask_for_letter().upper()
    if len(letter) == 1:
        moves += 1
        if letter not in word:
            error += 1
        list = findOccurrences(word, letter)
        word.replace(letter, " ")
    for index in list:
        output = output[0:(2 * index)] + letter + output[(2 * index) + 1:]
    print_screen(error, output, category)
    return error, moves, output


def ask_for_letter():
    letter = input('Wprowadź literę: ')
    print('\n\n')
    while len(letter) != 1:
        letter = input('Wprowadź literę: ')
        print('\n\n')
    return letter


def create_output(word):
    output = ''
    for i in word:
        if i == ',':
            output += ', '
        elif i == ' ':
            output += '  '
        else:
            output += '_ '
    return output


def print_screen(error, output, category):
    i = len(output) + 2
    print(i * '_')
    print(draw_hangman(error, i))
    print(i * '_')
    print(i * '*')
    print('Kategoria: ', category)
    print('\n\n')
    print(output)
    print('\n\n')
    print(i * '*')


def draw_hangman(error, i):
    i = int(i / 2 - 5)
    j = i + 1
    stage0 = i * ' ' + 'SZUBIENICA\n' + j * ' ' + '    \n' + j * ' ' + '     \n' + j * ' ' + '      \n' + j * ' ' + '     \n' + j * ' ' + '_______'
    stage1 = i * ' ' + 'SZUBIENICA\n' + j * ' ' + '    \n' + j * ' ' + '     \n' + j * ' ' + '      \n' + j * ' ' + ' |   \n' + j * ' ' + '_|_____'
    stage2 = i * ' ' + 'SZUBIENICA\n' + j * ' ' + '    \n' + j * ' ' + ' |   \n' + j * ' ' + ' |    \n' + j * ' ' + ' |   \n' + j * ' ' + '_|_____'
    stage3 = i * ' ' + 'SZUBIENICA\n' + j * ' ' + '  __\n' + j * ' ' + ' |  |\n' + j * ' ' + ' |    \n' + j * ' ' + ' |   \n' + j * ' ' + '_|_____'
    stage4 = i * ' ' + 'SZUBIENICA\n' + j * ' ' + '  __\n' + j * ' ' + ' |  |\n' + j * ' ' + ' |  o \n' + j * ' ' + ' |   \n' + j * ' ' + '_|_____'
    stage5 = i * ' ' + 'SZUBIENICA\n' + j * ' ' + '  __\n' + j * ' ' + ' |  |\n' + j * ' ' + ' | \o/\n' + j * ' ' + ' |  |\n' + j * ' ' + '_|_____'
    stage6 = i * ' ' + 'SZUBIENICA\n' + j * ' ' + '  __\n' + j * ' ' + ' |  |\n' + j * ' ' + ' | \o/\n' + j * ' ' + ' |  |\n' + j * ' ' + '_|_/_\_'
    if error == 0:
        return (stage0)
    if error == 1:
        return (stage1)
    if error == 2:
        return (stage2)
    if error == 3:
        return (stage3)
    if error == 4:
        return (stage4)
    if error == 5:
        return (stage5)
    if error == 6:
        return (stage6)
    else:
        exit()


def findOccurrences(word, letter):
    return [i for i, l in enumerate(word) if letter == l]


def game_lost(word):
    print('Hasło: ',word.upper())
    print('\n***** Przegrałeś :( *****\n')
    game_over()


def game_won():
    print('\n***** Brawo! Wygrałeś - odgadłeś hasło! *****\n')
    game_over()


def game_over():
    global over
    global diff
    over = 1
    choice = input(
        'Czy chcesz zagrać jeszcze raz?\n\nWpisz \'1\', aby zagrać jeszcze raz\nWciśnij dowolny inny klawisz, aby opuścić grę')
    if choice == '1':
        over = 0
        diff = 0
    else:
        print('\n***** Dziękuję za grę :) *****\n')
        exit()


def export_stats(stats):
    write_file('stats.txt', stats)


def calc_statisics(error, moves, word):
    # global game_counter
    x = 100 - ((error / moves) * 100)
    x = round(x)
    now = datetime.now()
    hour = now.strftime("%H:%M:%S")
    day = now.strftime("%d/%m/%Y")
    hits = (moves - error)
    if lost == 0:
        header = '***** WYGRANA *****'
    else:
        header = '***** PRZEGRANA *****'
    stats = ''.join([header, '\n\nStatystyki gracza: ', name, '\nData: ', day,
                     '\nGodzina: ', hour, '\nGra nr: ', str(game_counter), '\nRuchy: ', str(moves),
                     '\nPoprawne trafienia: ', str(hits), '\nBłędne trafienia: ', str(error), '\nSkuteczność trafień: ',
                     str(x), '%\nHasło: ',word.upper(),'\n\n'])

    return stats


def read_file(path):
    with open(path, 'r+') as plik:
        list = plik.read()
    return list


def write_file(path, content):
    with open(path, 'a+') as plik:
        plik.write(content)


def print_word(word):
    for i in word:
        print("_ ")

def main():
    hello()
    while over == 0:
        select_difficulty()
        dictionary = create_dictionary()
        word, category = pick_word(dictionary)
        play(word, category)

main()
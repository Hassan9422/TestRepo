import random


def main():
    my_list = creating_words_list()
    the_word = random.choice(my_list)
    if guessing_word(the_word):
        print("congratulations! you guessed the word correctly!")
    else:
        print(f"sorry you couldn't guessed it correctly :(, the correct word is {the_word}")


def creating_words_list():
    words_list = []
    while True:
        try:
            word = input("please insert a name (Ctrl+C to quit): ")
            words_list.append(word)
        except KeyboardInterrupt:
            return words_list


def guessing_word(string):
    o = 0
    my_word = list('-' * len(string))
    print('\n')
    while o < len(string) + 2:
        letter = input("please insert a letter: ")
        index = 0
        for s in string:
            if letter == s:
                my_word[index] = letter
            index += 1
        for e in my_word:
            print(e)

        if letter not in string:
            o += 1

        if "".join(my_word) == string:
            return True
    return False


if __name__ == "__main__":
    main()

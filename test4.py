import random
import time


def main():
    m = my_guess()
    c = computer_guess()
    if m == 0:
        print('Wow! you are the mastermind. you guessed it correctly in your first time!')
    elif c == 0:
        print('Wow! the computer became the mastermind. it guessed it correctly in its first time!')

    if m > c:
        print(f"you lost! it took {m} times you guessed. but the computer guesses it in {c} number of times!")
    elif m < c:
        print(f"you won! it took only {m} times you guessed. the computer guesses it in {c} number of times!")
    else:
        print(f"Tie! you and the computer both were able to guess it correctly in {c} number of times!")


def my_guess():
    tries = 0
    number = list('x' * 4)
    for i in range(len(number)):
        number[i] = str(random.randint(0, 9))
    while True:
        correct_digit_guesses = 0
        try:
            guess = list(input("Please guess the number(4 digits):"))
            if guess == number and tries == 0:
                return tries
            elif guess == number:
                print("it's right!")
                return tries
            if len(guess) != 4:
                raise ValueError()

            tries += 1
            for i in range(4):
                if number[i] == guess[i]:
                    print(f"{number[i]}", end='')
                    correct_digit_guesses += 1
                else:
                    print("x", end='')

            print("\n")
            print(f"Not quite the number. You did get {correct_digit_guesses} digits correct.")
            print("please try a new number.")
        except ValueError:
            print("you have to inter FOUR digits as an INTEGER")


def computer_guess():
    tries = 0
    my_num = list(input("please enter your desired number (4 digits): "))
    computer_num = list("x" * len(my_num))
    computer_guess_list = computer_num[:]
    j = [0, 1, 2, 3]
    while True:
        try:
            k = []
            if computer_guess_list == my_num and tries == 0:
                return tries
            elif computer_guess_list == my_num:
                print("that's right!")
                return tries
            tries += 1
            for i in j:
                computer_num[i] = str(random.randint(0, 9))

                if my_num[i] == computer_num[i]:
                    computer_guess_list[i] = computer_num[i]
                    k.append(i)
            for u in k:
                j.remove(u)
            print('\n')
        except ValueError:
            print("you have to inter an integer")


if __name__ == "__main__":
    main()

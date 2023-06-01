import random


def main():
    while True:
        try:
            b = int(input("please insert the beginning of a range you wish in integer: "))
            e = int(input("please insert the end of the range in integer: "))
            random_num = random.randint(b, e)
            while True:
                try:
                    guess = int(input("please guess a number: "))
                    if guess == random_num:
                        print(f"that's correct! the number is {guess}")
                        while True:
                            res = input("wanna play more? (please insert Y/N) ")
                            if res.lower() == "y":
                                break
                            elif res.lower() == 'n':
                                exit("Have a great time!")
                            else:
                                print('please insert Y or N')
                        break
                    elif guess < random_num:
                        print("it's too low!")
                    else:
                        print("it's too high!")

                except ValueError:
                    print("please insert an integer number!")
                    continue

        except ValueError:
            print("please insert a proper integer number")


if __name__ == '__main__':
    main()

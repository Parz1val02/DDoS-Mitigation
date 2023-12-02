#!/usr/bin/python
import os
import sys

if __name__=='__main__':
    '''if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} [# of option]')
        print('1. Print system information\n'+
            '2. Print date\n' +
            '3. Print RAM usge\n' +
            '4. Exit')
        sys.exit(1)
        '''

    while(True):
        print(f'Usage: [# of option]')
        print('1. Print system information\n'+
            '2. Print date\n' +
            '3. Print RAM usge\n' +
            '4. Exit')
        try:
            option = int(input("Enter # of option to execute> "))
            if(option == 1):
                print(os.system('hostnamectl'))
            elif(option == 2):
                print(os.system('date'))
            elif(option == 3):
                print(os.system('free -h'))
            elif(option == 4):
                sys.exit(0)
            else:
                print('Incorrect # of option')
        except ValueError:
            print("The option number must be an integer")

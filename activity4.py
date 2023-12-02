#!/usr/bin/python

if __name__=='__main__':
    num1 = input('Input first number> ')
    num2 = input('Input second number> ')

    try:
        div = int(num1)/int(num2)
    except ZeroDivisionError:
        print('Can not divide by zero')
    except ValueError:
        print('Both operand must be numbers')
    else:
        print(f'The result of dividing {num1} by {num2} is {div}')
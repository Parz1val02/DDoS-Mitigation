#!/usr/bin/python

if __name__== "__main__":
    num_minutes = int(input("Enter the number of minutes> "))
    hours = int(num_minutes/60)
    minutes = num_minutes%60
    print(f'{num_minutes} == {hours}h:{minutes}')
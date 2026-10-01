#Importing the libraries
from random import randint

#The Class Die implement a six-sided die

class Die:
    #the __init__ method is used to createa new instance of a die with a default value of 1
    def __init__(self):
        self.value = 1
    #the roll value method is used to set a value to a random number between 1 and 6

    def roll(self):
        self.value = randint(1,6)
    # the get  value method returns the top face value of the die

    def getValue(self):
        return self.value
    
    def __str__(self):
        return str(self.getValue())
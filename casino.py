
#This game plays the game of dice called craps where
#Players would bet on the outcomes of a pair of dice rolls.
#If the sum of the dice is 2, 3 or 12, the player loses immediately.
#If the sum of the dice is 7 or 11, they win immediately.
#The purpose of the program is to simulate the results between two players

from player import Player

#Importing the datetime to get the current date and time
from datetime import datetime

#This function is created to play a single game and print out the results after each roll.
def playOneGame():

    player = Player()
    while not player.isWinner() and not player.isLoser():
        player.rollDice()
        print(player)
    if player.isWinner():
        print("You win!")
    else:
        print("You lose!")

#This function is created to play multiple games and outputs the results based 
#on the number of games selected.
def playMultipleGames(number):
    #Initializing the variables
    wins = 0
    losses = 0
    winRolls = 0
    lossRolls = 0

    #Looping through the number of executions
    for count in range(number):
        player = Player()
        hasWon = player.play()
        rolls = player.getNumberOfRolls()
        if hasWon:
            wins += 1
            winRolls += rolls
        else:
            losses += 1
            lossRolls += rolls

    #Calculating the statistics
    print("The total number of wins is", wins)
    print("The total number of losses is", losses)
    print("The average number of rolls per win is %0.2f" % \
          (winRolls / wins))
    print("The average number of rolls per loss is %0.2f" % \
          (lossRolls / losses))
    print("The winning percentage is %0.3f" % (wins / number))
    print("The multi-game has been saved into the log.")

    logStats(wins, losses, winRolls, lossRolls, number)

#This function will log each multi game run to include the date/time and the details of the run
def logStats(wins, losses, winRolls, lossRolls, number):
    file = open("log.txt", "a")

    #Create a date/time object to get the current date and time
    now = datetime.now()
    #Formatting the output of the date and time to dd/mm/YY H:M:S
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    file.write("\n\ndate and time = " + dt_string)
    #Writing the statistics to a file
    file.write("\nThe total number of wins is " + str(wins))
    file.write("\nThe total number of losses is " + str(losses))
    file.write("\nThe average number of rolls per win is " +
               str(winRolls / wins))
    file.write("\nThe average number of rolls per loss is " +
               str(lossRolls / losses))
    file.write("\nThe winning percentage is " + str(wins / number))

#The main function as the point of entry
def main():
    #Play one game
    print("Running one sample game in full:")
    playOneGame()

    #Play multiple games based on the entry by the user
    number = int(input("How many games would you want to have tested: "))
    playMultipleGames(number)

if __name__ == "__main__":
    main()


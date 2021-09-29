import csv
import statistics
import tkinter
from tkinter import filedialog


class Statistics:
    def __init__(self):
        self.names_to_raw_rolls = {}          # a dictionary with entries of key = name, value = [] of raw D20 rolls. Name is pulled straight from the logs and can be a player name or PC name.
        self.filename = self.get_filename_of_name_mappings()
        self.player_names = []                # a list of all player names
        self.player_names_to_rolls = {}       # a dictionary with entries of key = player name, value = [] of raw D20 rolls for all PC names associated with that player name
        self.player_names_to_averages = {}    # a dictionary with entries of key = player name, value = the average of all rolls for all PC names associated with that player name
        self.player_names_to_stdevs = {}      # a dictionary with entries of key = player name, value = the stdev of all rolls for all PC names associated with that player name

    # Open a file browser window for the user to select the file containing a mapping of player names to PC names
    # Returns the filename as a file path
    def get_filename_of_name_mappings(self):
        print("Select file mapping player names to character names (must be a .csv file)")
        root = tkinter.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(title='Select file', parent=root, filetypes=[("Text files", "*.csv")]) # shows dialog box and return the path
        return filename


    # Adds a roll to a given name's history. If that name doesn't already exist, it is created
    # and the roll is added to its history
    def add_roll(self, name, roll):
        if name in self.names_to_raw_rolls:
            self.names_to_raw_rolls[name].append(roll)
        else:
            self.names_to_raw_rolls[name] = [roll]


    # Gets the player and PC names for which there is a roll history
    def get_names(self):
        return list(self.names_to_raw_rolls.keys())


    # Gets the history of rolls for a given name. Returns a list.
    # If that name doesn't have a history of rolls, an empty list is returned.
    def get_rolls(self, name):
        return self.names_to_raw_rolls.get(name, [])


    # returns the average of a given list of numbers
    def average(self, lis):
        if len(lis) == 0:
            return 0
        return sum(lis) / len(lis)


    # returns the standard deviation of a given list of numbers
    def stdev(self, lis):
        if len(lis) == 0:
            return 0
        return statistics.pstdev(lis)


    # Called after logs have been parsed. Generates statistics about each player's rolls which are stored
    # in the Statistics object.
    def generate_statistics(self):
        if self.filename == "" or not self.filename.lower().endswith(".csv"):
            return

        # the file containing a mapping of player names to PC names is a structured in this format....
        # player 1 name, player 1 login name, PC name 1, PC name 2, PC name 3
        # Player 2 name, player 2 login name, PC name 4, PC name 5
        with open(self.filename, 'r', encoding="utf-8") as f:
            readerObj = csv.reader(f) # Assumes the file was made in notepad, not excel. If the csv was made in Excel, it adds a BOM at the front that messes up the first player name.
            
            # associate all rolls with a given player name.
            # also track which names have been handled to verify later that there are no names in the logs that are not associated with a player
            names_handled = []
            for row in readerObj:
                player_name = row[0]
                self.player_names.append(player_name)
                self.player_names_to_rolls[player_name] = []
                for i in range(1, len(row)):
                    PC_name = row[i]
                    self.player_names_to_rolls[player_name] = self.player_names_to_rolls[player_name] + (self.get_rolls(PC_name))
                    names_handled.append(PC_name)

        # alert if there are any names in the logs that are not associated with a player
        names_with_rolls = self.get_names()
        for name in names_with_rolls:
            if not name in names_handled:
                print("Name '{}' is not associated with a player!".format(name))
                print("These rolls are unaccounted for: {}".format(self.get_rolls(name)))

        # generate statistical information
        for name in self.player_names:
            self.player_names_to_averages[name] = self.average(self.player_names_to_rolls[name])
            self.player_names_to_stdevs[name] = self.stdev(self.player_names_to_rolls[name])


    def output_statistics(self):
        print("Raw Rolls", self.player_names_to_rolls)
        print("Averages", self.player_names_to_averages)
        print("Standard Deviations", self.player_names_to_stdevs)
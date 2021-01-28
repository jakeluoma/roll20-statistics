import csv
import statistics
import tkinter
from tkinter import filedialog


class Statistics:
    def __init__(self):
        # a dictionary with entries of key = name, value = [] of raw D20 rolls
        self.names_to_raw_rolls = {}
        self.filename = self.get_filename()
        self.player_names = []
        self.player_names_to_rolls = {}
        self.player_names_to_averages = {}
        self.player_names_to_stdevs = {}


    def get_filename(self):
        print("Select file mapping player names to character names (must be a .csv file)")
        root = tkinter.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(title='Select file', parent=root, filetypes=[("Text files", "*.csv")]) # shows dialog box and return the path
        return filename


    # Adds a roll to a given name's history. If that name doesn't already exist, it is created
    # and then the roll is added to its history
    def add_roll(self, name, roll):
        if name in self.names_to_raw_rolls:
            self.names_to_raw_rolls[name].append(roll)
        else:
            self.names_to_raw_rolls[name] = [roll]


    # Gets the names for which there is a history
    def get_names(self):
        return list(self.names_to_raw_rolls.keys())


    # Gets the history of rolls for a given name. Returns a list.
    # If that name doesn't have a history of rolls, an empty list is returned.
    def get_rolls(self, name):
        return self.names_to_raw_rolls.get(name, [])

    
    def average(self, lis):
        if len(lis) == 0:
            return 0
        return sum(lis) / len(lis)

    def stdev(self, lis):
        if len(lis) == 0:
            return 0
        return statistics.pstdev(lis)


    def generate_statistics(self):
        if self.filename == "" or not self.filename.lower().endswith(".csv"):
            return

        with open(self.filename, 'r') as f:
            readerObj = csv.reader(f) # Assumes the file was made in notepad, not excel. If the csv was made in Excel, it adds a BOM at the front that messes up the first player name.
            
            for row in readerObj:
                name = row[0]
                self.player_names.append(name)
                self.player_names_to_rolls[name] = []
                length = len(row)
                for i in range(1, length):
                    self.player_names_to_rolls[name] = self.player_names_to_rolls[name] + (self.get_rolls(row[i]))

        # should probably have a check to make sure all character names are accounted for

        for name in self.player_names:
            self.player_names_to_averages[name] = self.average(self.player_names_to_rolls[name])
            self.player_names_to_stdevs[name] = self.stdev(self.player_names_to_rolls[name])


    def output_statistics(self):
        print("Raw Rolls", self.player_names_to_rolls)
        print("Averages", self.player_names_to_averages)
        print("Standard Deviations", self.player_names_to_stdevs)
import re
import tkinter
from tkinter import filedialog

from .states.name_unknown_state import Name_Unknown_State
from .states.name_known_state import Name_Known_State
from .states.result_or_damage_state import Result_Or_Damage_State

"""
The parser is implemented as an object-oriented state machine. It keeps track of the various states it can be in
as well as the state it is currently in. Every state implements the same methods which are called to affect state transitions
and/or parsing actions. The parser uses regexes to recognize that a particular state method should be called. 

The parser's embedded states call the embedded Statistics class' add_roll() method which associates a name with a roll
when a d20 roll is encountered.
"""
class Parser:
    def __init__(self, statistics, debug):
        self.statistics = statistics
        self.debug = debug
        self.filename = self.get_filename()
        self.name_unknown_state = Name_Unknown_State(self.statistics, self)
        self.name_known_state = Name_Known_State(self.statistics, self)
        self.result_or_damage_state = Result_Or_Damage_State(self.statistics, self)
        self.current_state = self.name_unknown_state
        self.name = ""
        self.raw_number_one = 0
        self.raw_number_two = 0


    def change_to_name_unknown_state(self):
        self.current_state = self.name_unknown_state

    def change_to_name_known_state(self):
        self.current_state = self.name_known_state

    def change_to_result_or_damage_state(self):
        self.current_state = self.result_or_damage_state


    def get_filename(self):
        print("Select chat log file you want processed (must be a .txt file)")
        root = tkinter.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(title='Select file', parent=root, filetypes=[("Text files", "*.txt")]) # shows dialog box and return the path
        return filename

    
    def set_name(self, name):
        self.name = name

    def get_name(self):
        return self.name


    def set_raw_number_one(self, number):
        self.raw_number_one = number

    def get_raw_number_one(self):
        return self.raw_number_one


    def set_raw_number_two(self, number):
        self.raw_number_two = number

    def get_raw_number_two(self):
        return self.raw_number_two

    
    def debug_print(self, text):
        if self.debug:
            print(text)


    def parse(self):
        if self.filename == "" or not self.filename.lower().endswith(".txt"):
            return

        # ^...$ means the whole string has to match what's inside of them
        name_regex = re.compile('^(.+):$')
        name_with_roll_regex = re.compile('(.+):rolling 1?d20.*')
        name_with_non_d20_roll_regex = re.compile('(.+):rolling ([0-9]*)d[0-9]+.*')
        roll_regex = re.compile('rolling 1?d20.*')
        roll_with_non_d20_regex = re.compile('rolling ([0-9]*)d[0-9]+.*')
        raw_number_regex = re.compile('^[0-9]+$')
        raw_number_plus_raw_number_regex = re.compile('^([0-9]+) \+ ([0-9]+)')
        raw_number_space_raw_number_regex = re.compile('^([0-9]+)  ([0-9]+)')
        text_mod_regex = re.compile('.+\((-|\+)?([0-9]+)\)')
        initiative_part_one_regex = re.compile('([0-9]+)\.[0-9]+')
        initiative_part_two_regex = re.compile('INITIATIVE \((-?[0-9]+)\.[0-9]+\)')

        with open(self.filename, encoding="utf-8") as f:
            while True:
                line = f.readline()
                if line == "":
                    break

                self.debug_print("line: {}".format(line))


                """
                NAME
                Has form:
                Flabnatz (GM):
                """
                match = name_regex.match(line)
                if match:
                    name = match.group(1)
                    # There are some exceptions which will falsely match this regex and should be skipped.
                    # One is when you whisper to GM. It outputs text like "(To GM):".
                    # Another is when there is a text description that has a bunch of text ending with a colon.
                    # I arbitrarily say that any "name" longer than 10 words is actually a text description.
                    # I'm sure some special player will break that assumption, but what can you do :)
                    if name == "(To GM)":
                        continue
                    if len(name.split()) > 10:
                        continue

                    self.current_state.name(name)
                    
                    self.debug_print("Matched name regex. Name is {}".format(name))
                    continue


                """
                NAME WITH ROLL
                Has form:
                Flabnatz (GM):rolling d20
                (
                14
                )
                =14

                OR

                Flabnatz (GM):rolling 1d20 + 5
                (
                7
                )+5
                =12
                """
                match = name_with_roll_regex.match(line)
                if match:
                    name = match.group(1)

                    f.readline() # throw away '('
                    roll_line = f.readline() # get roll
                    roll = int(roll_line)
                    f.readline() # throw away ')'
                    f.readline() # throw away result

                    self.current_state.name_with_roll_comand(name, roll)

                    self.debug_print("matched name with roll regex. Name is {}. Roll is {}.".format(match.group(1), roll))
                    continue


                """
                NAME WITH NON D20 ROLL
                Has form:
                Ash:rolling 1d8
                (
                6
                )
                =6

                OR
                Ash:rolling 2d8
                (
                6
                +
                2
                )
                =8
                """
                match = name_with_non_d20_roll_regex.match(line)
                if match:
                    name = match.group(1)
                    if match.group(2) != "":
                        num_die = int(match.group(2))
                    else:
                        num_die = 1
                    num_mid_lines = 1 + (num_die - 1) * 2

                    # simply consume
                    f.readline() # throw away '('
                    for _ in range(num_mid_lines):
                        f.readline() # throw away mid lines
                    f.readline() # throw away ')'
                    f.readline() # throw away result

                    self.current_state.name(name)

                    self.debug_print("matched name with non-d20 roll regex. consumed.")
                    continue


                """
                ROLL
                Has form:
                rolling d20
                (
                14
                )
                =14

                OR

                rolling 1d20 + 5
                (
                7
                )+5
                =12
                """
                match = roll_regex.match(line)
                if match:
                    f.readline() # throw away '('
                    roll_line = f.readline() # get roll
                    roll = int(roll_line)
                    f.readline() # throw away ')'
                    f.readline() # throw away result

                    self.current_state.roll_command(roll)

                    self.debug_print("matched roll regex. Roll is {}.".format(roll))
                    continue


                """
                ROLL WITH NON D20
                Has form:
                rolling d4
                (
                4
                )
                =4

                OR

                rolling 2d4 + 5
                (
                2
                +
                2
                )+5
                =9
                """
                match = roll_with_non_d20_regex.match(line)
                if match:
                    if match.group(1) != "":
                        num_die = int(match.group(1))
                    else:
                        num_die = 1
                    num_mid_lines = 1 + (num_die - 1) * 2

                    # simply consume
                    f.readline() # throw away '('
                    for _ in range(num_mid_lines):
                        f.readline() # throw away mid lines
                    f.readline() # throw away ')'
                    f.readline() # throw away result

                    self.debug_print("matched roll with non-d20 regex. consumed.")
                    continue


                """
                RAW NUMBER
                Has form:
                5
                """
                match = raw_number_regex.match(line)
                if match:
                    number = int(match.group(0))

                    self.current_state.raw_number(number)

                    self.debug_print("matched raw number regex. Number is {}".format(number))
                    continue


                """
                RAW NUMBER PLUS RAW NUMBER
                Has form:
                20 + 2
                """
                match = raw_number_plus_raw_number_regex.match(line)
                if match:
                    number_one = int(match.group(1))
                    number_two = int(match.group(2))

                    self.current_state.raw_number_plus_raw_number(number_one, number_two)

                    self.debug_print("matched raw number plus raw number regex. Number one is {}. Number two is {}".format(number_one, number_two))
                    continue


                """
                RAW NUMBER SPACE RAW NUMBER
                Has form:
                20 2
                """
                match = raw_number_space_raw_number_regex.match(line)
                if match:
                    number_one = int(match.group(1))
                    number_two = int(match.group(2))

                    self.current_state.raw_number_space_raw_number(number_one, number_two)

                    self.debug_print("matched raw number space raw number regex. Number one is {}. Number two is {}".format(number_one, number_two))
                    continue


                """
                TEXT MOD
                Has form:
                Light Crossbow (+4)

                OR 

                Light Crossbow (-1)
                """
                match = text_mod_regex.match(line)
                if match:
                    if match.group(1) is not None:
                        plus_minus = match.group(1)
                        number = match.group(2)
                        mod = int(plus_minus + number)
                    else:
                        mod = int(match.group(2))

                    self.current_state.text_mod(mod)

                    self.debug_print("matched text mod regex. Mod is {}.".format(mod))
                    continue

                
                """
                INITIATIVE
                Has form:
                14.14
                INITIATIVE (2.14)
                """
                match = initiative_part_one_regex.match(line)
                if match:
                    number = int(match.group(1))
                    
                    mod_line = f.readline()
                    match_mod_line = initiative_part_two_regex.match(mod_line)
                    if match_mod_line:
                        mod = int(match_mod_line.group(1))

                        self.current_state.initiative(number, mod)

                        self.debug_print("matched initiative regex. Number is {}. Mod is {}".format(number, mod))
                        continue
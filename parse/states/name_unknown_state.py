

class Name_Unknown_State:
    def __init__(self, statistics, parser):
        self.statistics = statistics
        self.parser = parser

    def name(self, name):
        self.parser.set_name(name)
        self.parser.change_to_name_known_state()

    def name_with_roll_comand(self, name, roll):
        self.parser.set_name(name)
        self.statistics.add_roll(name, roll)
        self.parser.change_to_name_known_state()

    def roll_command(self, roll):
        pass

    def raw_number(self, number):
        pass

    def raw_number_plus_raw_number(self, number_one, number_two):
        pass

    def raw_number_space_raw_number(self, number_one, number_two):
        pass

    def text_mod(self, mod):
        pass

    def initiative(self, number, mod):
        pass
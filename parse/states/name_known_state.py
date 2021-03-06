

class Name_Known_State:
    def __init__(self, statistics, parser):
        self.statistics = statistics
        self.parser = parser

    def name(self, name):
        self.parser.set_name(name)

    def name_with_roll_comand(self, name, roll):
        self.parser.set_name(name)
        self.statistics.add_roll(name, roll)

    def roll_command(self, roll):
        name = self.parser.get_name()
        self.statistics.add_roll(name, roll)

    def raw_number(self, number):
        self.parser.set_raw_number_one(number)
        self.parser.change_to_result_or_damage_state()

    def raw_number_plus_raw_number(self, number_one, number_two):
        self.parser.set_raw_number_one(number_one)
        self.parser.set_raw_number_two(0)
        self.parser.change_to_result_or_damage_state()

    def raw_number_space_raw_number(self, number_one, number_two):
        self.parser.set_raw_number_one(number_one)
        self.parser.set_raw_number_two(number_two)

    def text_mod(self, mod):
        name = self.parser.get_name()

        number_one = self.parser.get_raw_number_one()
        self.statistics.add_roll(name, number_one - mod)

        number_two = self.parser.get_raw_number_two()
        if number_two != 0:
            self.statistics.add_roll(name, number_two - mod)
            self.parser.set_raw_number_two(0)

    def initiative(self, number, mod):
        name = self.parser.get_name()
        self.statistics.add_roll(name, number - mod)
import pylab

class DiceArray:
    def __init__(self, sides, rest_of_dice):
        self.sides = sides
        self.rest_of_dice = rest_of_dice
        self.possibility_array = []
        self.nested = len(self.rest_of_dice) > 0

    def generate_nested_array(self):
        new_dice_array = DiceArray(self.rest_of_dice[0],
                                   self.rest_of_dice[1:]).get_array()
        for side_value in range(self.sides):
            self.possibility_array.append(new_dice_array)

    def generate_simple_array(self):
        for side_value in range(self.sides):
            self.possibility_array.append(side_value + 1)

    def generate_array(self):
        self.possibility_array = []
        if self.nested:
            self.generate_nested_array()
        else:
            self.generate_simple_array()

    def get_array(self):
        self.generate_array()
        self.collapse_array()
        return self.possibility_array

    def collapse_array(self):
        if self.nested:
            collapsed_array = []
            for value1, possibilities in enumerate(self.possibility_array):
                value1 += 1
                for value2 in possibilities:
                    collapsed_array.append(value1 + value2)
            self.possibility_array = collapsed_array

        
def ask_for_dice():
    answer = "invalid"
    while input_is_invalid(answer):
        print("Enter your desired dice. For each dice, type the amount of sides.")
        print("Seperate each dice with a dash. Example: '6-6-4' means two")
        print("six-sided dice and a four-sided dice.")
        answer = input("Enter here: ").strip()
    return get_dice_list(answer)


def get_dice_list(text):
    return [int(dice_sides) for dice_sides in text.split("-")]


def input_is_invalid(text):
    valid_characters = list("0123456789-")
    for character in text:
        if character not in valid_characters:
            return True
    return False

def get_dice_probabilities(dice_list):
    dice_counts = get_dice_counts(dice_list)
    total_possibilities = get_total_possibilities(dice_counts)
    probabilities = {}
    for value, count in dice_counts.items():
        probabilities[value] = [float(count / total_possibilities),
                                "{}/{}".format(count, total_possibilities)]
    return probabilities


def get_total_possibilities(dice_counts):
    total = 0
    for count in dice_counts.values():
        total += count
    return total


def get_dice_counts(dice_list):
    possibilities = DiceArray(dice_list[0], dice_list[1:]).get_array()
    counts = {}
    for value in possibilities:
        if value not in counts.keys():
            counts[value] = 0
        counts[value] += 1
    return counts


def print_probabilities(probabilities):
    for total, probability in probabilities.items():
        probability = [round(probability[0] * 100, 5), probability[1]]
        print("Likelyhood of totalling {}: {}%  ({})".format(total,
                                                             probability[0],
                                                             probability[1]))


def graph(probabilities, dice_list):
    x_axis = list(probabilities.keys())
    x_axis.sort()
    y_axis = [prob[0] * 100 for prob in probabilities.values()]
    pylab.plot(x_axis, y_axis)
    pylab.xlabel("Dice Total")
    pylab.ylabel("Percent Chance")
    pylab.title("Dice: " + str(dice_list))
    pylab.grid(True)
    pylab.show()


def main():
    print("WELCOME TO THE DICE MACHINE\n\n")
    while True:
        print("=====================================")
        dice_list = ask_for_dice()
        print("Calculating...")
        probabilities = get_dice_probabilities(dice_list)
        print_probabilities(probabilities)
        graph(probabilities, dice_list)


if __name__ == "__main__":
    main()

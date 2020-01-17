import tkinter as tk

WINDOW_BACKGROUND = "#f1f1f1"


class IncCommand:
    def __init__(self, register, return_line=0):
        self.register = register
        self.start_line = 1
        self.return_line = return_line

    def get_rodrego_code(self):
        if not self.return_line:
            next_line = self.start_line + 1
        else:
            next_line = self.return_line
        return "{line} inc {register} {next_line}".format(line=self.start_line, register=self.register,
                                                          next_line=next_line)

    def get_next_line(self):
        return self.start_line + 1


class StopCommand:
    def __init__(self, return_line=0):
        self.start_line = 1
        self.return_line = return_line

    def get_rodrego_code(self):
        return "{line} end".format(line=self.start_line)

    def get_next_line(self):
        return self.start_line + 1


class DebCommand:
    def __init__(self, register, command_list, return_line=0):
        self.register = register
        self.start_line = 1
        self.command_list = command_list
        self.return_line = return_line
        self.next_line_bias = 0

        if command_list[-1] == ['loop']:
            self.loop = True
        else:
            self.loop = False

    def convert_code(self):
        main_command_list, zero_command_list = self.get_nested_command_lists()

        # Getting code length
        main_command_objects = get_command_objects(main_command_list)
        zero_command_objects = get_command_objects(zero_command_list)

        main_length = len(generate_rodrego_code(main_command_objects, nested=True).split("\n"))
        zero_length = len(generate_rodrego_code(zero_command_objects, nested=True).split("\n"))

        last_line = self.start_line + main_length + zero_length

        # Line variables
        second_line = self.start_line + 1
        zero_second_line = second_line + main_length
        if not self.return_line:
            next_line = last_line + 1
        else:
            next_line = self.return_line

        # Code generation
        if self.loop and len(main_command_objects) > 0:
            main_command_objects[-1].return_line = self.start_line
        elif len(main_command_objects) > 0:
            main_command_objects[-1].return_line = next_line
        else:
            zero_second_line = second_line
            next_line -= 1
            if self.loop:
                second_line = self.start_line
            else:
                second_line = next_line

        if len(zero_command_objects) > 0:
            zero_command_objects[-1].return_line = next_line
        else:
            next_line -= 1
            zero_second_line = next_line
            if not self.loop and len(main_command_objects) > 0:
                main_command_objects[-1].return_line -= 1
            elif not self.loop:
                second_line = next_line


        main_code = generate_rodrego_code(main_command_objects, nested=True, start_line=second_line)
        zero_code = generate_rodrego_code(zero_command_objects, nested=True, start_line=zero_second_line)

        first_line = "{start_line} deb {register} {second_line} {zero_second_line}".format(
            start_line=self.start_line,
            register=self.register,
            second_line=second_line,
            zero_second_line=zero_second_line)

        code = "{first_command}\n{main_code}\n{zero_code}".format(first_command=first_line,
                                                                  main_code=main_code,
                                                                  zero_code=zero_code)
        while "\n\n" in code:
            code = code.replace("\n\n", "\n")
        if code[-1] == "\n":
            code = code[:-1]

        return code

    def get_rodrego_code(self):
        return self.convert_code()

    def get_next_line(self):
        code = self.convert_code()
        return self.start_line + len(code.split("\n"))

    def get_nested_command_lists(self):
        main_list = []
        nested_degree = 1
        for command_index, command in enumerate(self.command_list[:-1]):
            if command[0] == "deb":
                nested_degree += 1
            elif command[0] == "zero":
                nested_degree -= 1

            if nested_degree == 0:
                zero_list = self.command_list[command_index+1:]
                return main_list, zero_list
            main_list.append(command)


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.config(bg=WINDOW_BACKGROUND)
        self.root.title("PaBlo")
        self.is_running = False

        # Widget setup

        # Text box
        self.input_text = tk.Text(self.root, width=80, highlightthickness=2, highlightbackground="black")
        self.input_text.grid(row=0, column=0, columnspan=10, rowspan=10)

        self.output_text = tk.Text(self.root, width=30, highlightthickness=2, highlightbackground="black")
        self.output_text.grid(row=0, column=10, columnspan=10, rowspan=10)

        # Control Buttons
        generate_button = tk.Button(self.root, text="Generate", bg="green", command=self.convert_code)
        generate_button.grid(column=0, columnspan=20, row=11, sticky=tk.E+tk.W)

        # Error Message
        self.error_message = tk.Label(self.root, text="", fg="red", bg=WINDOW_BACKGROUND, font="Helvetica 14 bold")
        self.error_message.grid(column=0, row=10, columnspan=10, sticky=tk.W)

        # Window Start
        self.root.mainloop()

    def convert_code(self):
        self.is_running = True
        self.display_error_message("")
        lines = self.input_text.get("1.0", tk.END).split("\n")[:-1]
        command_list = self.process_lines(lines)

        if not self.is_running:
            return

        command_objects = get_command_objects(command_list)
        new_code = generate_rodrego_code(command_objects)
        self.display_code(new_code)

    def process_lines(self, lines):
        command_list = []

        for line_num, line in enumerate(lines):
            if not syntax_is_ok(line):
                self.is_running = False
                self.display_error_message("Invalid syntax on line {}".format(line_num + 1))
                break
            raw_command = get_raw_command(line)
            if raw_command:
                command_list.append(raw_command)
        return command_list

    def display_error_message(self, text):
        self.error_message.config(text=text)

    def display_code(self, text):
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, text)


def syntax_is_ok(line):
    try:
        get_raw_command(line)
        return True
    except RuntimeError:
        return False


def get_raw_command(line):
    if line == "":
        return []
    while line.startswith(" "):
        line = line[1:]
    if line.startswith("#"):
        return []

    line_parts = line.split(" ")
    raw_command = []
    if len(line_parts) >= 1:
        if line_parts[0] == "inc" and len(line_parts) == 2 and is_int(line_parts[1]):
            raw_command.append("inc")
            raw_command.append(int(line_parts[1]))
        elif line_parts[0] == "deb" and len(line_parts) == 2 and is_int(line_parts[1]):
            raw_command.append("deb")
            raw_command.append(int(line_parts[1]))
        elif line_parts[0] == "stop" and len(line_parts) == 1:
            raw_command.append("stop")
        elif line_parts[0] == "zero" and len(line_parts) == 1:
            raw_command.append("zero")
        elif line_parts[0] == "loop" and len(line_parts) == 1:
            raw_command.append("loop")
        elif line_parts[0] == "end" and len(line_parts) == 1:
            raw_command.append("end")
        else:
            raise RuntimeError
    else:
        raise RuntimeError
    return raw_command


def get_command_objects(command_list):
    command_objects = []
    command_index = 0
    while command_index < len(command_list):
        command = command_list[command_index]
        if len(command) == 0:
            command_index += 1
            continue
        elif command[0] == "inc":
            command_objects.append(IncCommand(command[1]))
        elif command[0] == "stop":
            command_objects.append(StopCommand())
        elif command[0] == "deb":
            nested_command_list = get_nested_command(command_index, command_list)
            command_objects.append(DebCommand(command[1], nested_command_list))
            command_index += len(nested_command_list) + 1
            continue

        command_index += 1

    return command_objects


def get_nested_command(command_index, command_list):
    nested_list = []
    nested_degree = 1
    for command in command_list[command_index+1:len(command_list)]:
        if command[0] == "deb":
            nested_degree += 1
        elif command[0] == "loop":
            nested_degree -= 1
        elif command[0] == "end":
            nested_degree -= 1

        nested_list.append(command)
        if nested_degree == 0:
            return nested_list


def generate_rodrego_code(command_objects, nested=False, start_line=1):
    text = []
    current_line_number = start_line
    for command in command_objects:
        command.start_line = current_line_number
        text.append(command.get_rodrego_code())

        current_line_number = command.get_next_line()

    if not nested:
        text.append("{line} end".format(line=current_line_number))

    return "\n".join(text)


def is_int(num):
    try:
        int(num)
        return True
    except ValueError:
        return False


if __name__ == '__main__':
    Window()

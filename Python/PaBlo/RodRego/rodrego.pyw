import tkinter as tk
import time
import threading

LABEL_BACKGROUND = "#7a7a7a"
ACTIVE_LABEL_FOREGROUND = "#ffb12b"
PASSIVE_LABEL_FOREGROUND = "#ffffff"
WINDOW_BACKGROUND = "#a5a5a5"
BUTTON_BACKGROUND = "#bcbcbc"

WAIT_TIME = 0.5
SCRIPT_LOCK = threading.Lock()


class Window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.config(bg=WINDOW_BACKGROUND)
        self.root.title("RodRego")
        self.running = False

        # Widget setup

        # Text box
        self.text = tk.Text(self.root, width=30, highlightthickness=2, highlightbackground="black")
        self.text.grid(row=0, column=0, columnspan=10, rowspan=10)

        # Registers
        self.registers = self.get_registers(40)

        for reg_num, reg in enumerate(self.registers):
            column = (reg_num // 10)*4 + 11
            row = (reg_num % 10)
            minus_button = tk.Button(self.root, text="-", bg=BUTTON_BACKGROUND,
                                     command=lambda index=reg_num: self.change_register(index, -1))
            plus_button = tk.Button(self.root, text="+", bg=BUTTON_BACKGROUND,
                                    command=lambda index=reg_num: self.change_register(index, 1))

            reg[0].grid(column=column, row=row, padx=10, sticky=tk.W)
            minus_button.grid(column=column+1, row=row, sticky=tk.W)
            plus_button.grid(column=column+2, row=row, sticky=tk.W)

        # Control Buttons
        start_button = tk.Button(self.root, text="Start", bg="green", command=self.start_script_thread)
        stop_button = tk.Button(self.root, text="Stop", bg="red", command=self.stop_script)

        start_button.grid(column=0, columnspan=5, row=11, sticky=tk.E+tk.W)
        stop_button.grid(column=5, columnspan=5, row=11, sticky=tk.E+tk.W)

        # Error Message
        self.error_message = tk.Label(self.root, text="", fg="red", bg=WINDOW_BACKGROUND, font="Helvetica 14 bold")
        self.error_message.grid(column=11, row=11, columnspan=10, sticky=tk.W)

        # Window Start
        self.root.mainloop()

    def start_script_thread(self):
        thread = threading.Thread(target=lambda: self.execute_script())
        thread.daemon = True
        thread.start()

    def change_register(self, register_number, amount):
        register_widget = self.registers[register_number][0]
        register_quantity = self.registers[register_number][1]
        if amount > 0 or register_quantity > 0:
            register_widget.config(text="  {}:   {}".format(register_number, register_quantity + amount))

            self.registers[register_number] = [register_widget, register_quantity + amount]

    def execute_script(self):
        if not SCRIPT_LOCK.acquire(blocking=False):
            return
        self.running = True
        commands = self.get_commands(self.text.get("1.0", tk.END))
        next_command = 0
        while self.running:
            command = commands[next_command]

            if command[0] == "inc":
                next_command = self.increase(command)
            elif command[0] == "deb":
                next_command = self.decrease_or_branch(command)
            else:
                self.stop_script()

            time.sleep(WAIT_TIME)
        SCRIPT_LOCK.release()

    def increase(self, command):
        register_number = command[1]

        self.highlight_register(register_number)
        self.change_register(register_number, 1)

        return command[2] - 1

    def decrease_or_branch(self, command):

        register_number = command[1]

        self.highlight_register(register_number)

        register_quantity = self.registers[register_number][1]

        if register_quantity > 0:
            self.change_register(register_number, -1)

            return command[2] - 1
        else:
            return command[3] - 1

    def stop_script(self):
        self.highlight_register(-1)
        self.running = False

    def highlight_register(self, register_number):
        for reg_number, register in enumerate(self.registers):
            if register_number == reg_number:
                register[0].config(fg=ACTIVE_LABEL_FOREGROUND)
            else:
                register[0].config(fg=PASSIVE_LABEL_FOREGROUND)

    def get_registers(self, amount):
        registers = []
        for register_number in range(amount):
            register = tk.Label(self.root, text="  {}:   0".format(register_number),
                                bg=LABEL_BACKGROUND, fg=PASSIVE_LABEL_FOREGROUND)
            registers.append([register, 0])
        return registers

    def get_commands(self, text):
        self.clear_error_message()
        lines = text.split("\n")[:-1]
        commands = []
        for line_num, line in enumerate(lines):
            while "  " in line:
                line = line.replace("  ", " ")
            parts = line.split(" ")
            try:
                commands.append(get_command_syntax(parts))
            except (ValueError, AssertionError, RuntimeError):
                self.display_error_message("Invalid syntax on line {}".format(line_num + 1))
                self.running = False

        return commands

    def display_error_message(self, text):
        self.error_message.config(text=text)

    def clear_error_message(self):
        self.display_error_message("")


def get_command_syntax(raw_command):
    command = []
    int(raw_command[0])
    command_type = raw_command[1].lower()

    if command_type == "inc":
        command.append("inc")
        command.append(int(raw_command[2]))
        command.append(int(raw_command[3]))
        assert len(raw_command) == 4

    elif command_type == "deb":
        command.append("deb")
        command.append(int(raw_command[2]))
        command.append(int(raw_command[3]))
        command.append(int(raw_command[4]))
        assert len(raw_command) == 5

    elif command_type == "end":
        command.append("end")
        assert len(raw_command) == 2

    else:
        raise RuntimeError()

    return command


if __name__ == '__main__':
    window = Window()

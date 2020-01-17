#!/usr/bin/env python3.6
""" Basic common functions for the running of Sleuth AI"""
import json


def clear_screen():
    """ Clears terminal by flooding stdout with newlines"""
    print("\n"*80)


def ask_int(prompt, error_message="Input was invalid. Please enter an integer\n"):
    """ Keeps asking for input until the input entered can be coerced into an int"""
    while True:
        answer = input(prompt)
        if isint(answer):
            print(error_message)
            return int(answer)


def isint(string):
    """ Checks if string can be coerced into an int"""
    try:
        int(string)
        return True
    except ValueError:
        return False


def write_to_json(jsonfile, data):
    """ Writes data to a json file in a human readable way"""
    with open(jsonfile, "w") as open_json_file:
        json.dump(data, open_json_file, sort_keys=True, indent=4)
import os

LISTIFY_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "listify.txt")


def main():
    with open(LISTIFY_FILE, "r") as readfile:
        print("[ul]")
        for line in readfile.readlines():
            line = line.strip().replace(" [Details]", "")
            print("[li]{}[/li]".format(line.strip()))
        print("[/ul]")


if __name__ == '__main__':
    main()

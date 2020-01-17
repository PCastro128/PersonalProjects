import os
import argparse
from abc import ABC
from html.parser import HTMLParser
from urllib import request

OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "town.txt")
URL = "https://www.kassoon.com/dnd/town-generator/"


PERMITTED_TAGS = {"h2": "h2",
                  "h1": "h1",
                  "h3": "h3",
                  "p": "p",
                  "br": "br",
                  "hr": "hr",
                  "div": "div",
                  "strong": "b",
                  "ul": "ul",
                  "li": "li",
                  "span": ""}


def get_converted_tag(tag, closing=False):
    if tag == "div":
        return "\n"
    elif (closing and (tag == "br" or tag == "hr")) or tag == "span":
        return ""
    elif closing:
        form = "[/{}]"
    else:
        form = "[{}]"
    return form.format(PERMITTED_TAGS[tag])


class TownParser(HTMLParser, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = ""
        self.opening_tag = []

    def handle_starttag(self, tag, attrs):
        self.opening_tag.append(tag)
        if len(self.opening_tag) > 0 and self.opening_tag[-1] in PERMITTED_TAGS:
            self.result += get_converted_tag(tag)

    def handle_data(self, data):
        if len(self.opening_tag) > 0 and self.opening_tag[-1] in PERMITTED_TAGS:
            self.result += data

    def handle_endtag(self, tag):
        if len(self.opening_tag) > 0 and self.opening_tag[-1] in PERMITTED_TAGS:
            self.result += get_converted_tag(tag, closing=True)
        if len(self.opening_tag) > 0:
            self.opening_tag.pop(-1)


# class MyHTMLParser(HTMLParser):
#     def handle_starttag(self, tag, attrs):
#         print("Encountered a start tag:", tag)
#
#     def handle_endtag(self, tag):
#         print("Encountered an end tag :", tag)
#
#     def handle_data(self, data):
#         print("Encountered some data  :", data)


def get_town_content(url):
    with request.urlopen(url) as web:
        content = web.read().decode('utf-8')
    content = content.split("<h2>")
    content = "<h2>" + "<h2>".join(content[1:])  # Get all html after first <h2> tag
    content = content.split("<h2>Housing</h2>")[0]  # Get all html before <h2>Housing</h2>

    return content.replace("\n", "")


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", "-u", help="Custom town url (optional).")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.url:
        url = args.url
    else:
        url = URL
    content = get_town_content(url)
    parser = TownParser()
    parser.feed(content)
    with open(OUTPUT_FILE, "w") as writefile:
        writefile.write(parser.result)


if __name__ == '__main__':
    main()

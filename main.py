
import random
import requests
from colorama import init, Fore, Style
import curses

word_source = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(word_source)
word_list = response.content.splitlines()
ch_list = []
wrong_list = []
done_list = []

screen = ""

def curses_init():
    curses.noecho()
    curses.cbreak()
    screen = curses.initscr()
    screen.keypad(True)

def color_init():
    curses.start_color()
    if curses.has_colors() == True:
        curses.init_pair(0, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    else:
        curses_print("No color support!") #Placeholder. Will replace with fallback...


def terminate_curses():
    curses.echo()
    curses.nocbreak()
    screen.keypad(False)

def move(inp: list, outp: list):
    outp.append(inp[0])
    inp.pop(0)


def greet():
    print(""" _____                     _             _            
/  ___|                   | |           | |           
\ `--. _ __   ___  ___  __| |_ __  _   _| |_ ___ _ __ 
 `--. \ '_ \ / _ \/ _ \/ _` | '_ \| | | | __/ _ \ '__|
/\__/ / |_) |  __/  __/ (_| | |_) | |_| | ||  __/ |   
\____/| .__/ \___|\___|\__,_| .__/ \__, |\__\___|_|   
      | |                   | |     __/ |             
      |_|                   |_|    |___/              """)
    print("Welcome!")
    print("Press X to exit")


def get_word():
    x = str(random.choice(word_list))
    x = x.replace("b'", "")
    x = x.replace("'", "")
    return x


def convert(x: list):
    out = ''.join(x)
    return out


def print_with_color(x: str, c: int):
    screen.addstr(x, curses.color_pair(c))

def curses_print(x: str):
    screen.addstr(x, curses.color_pair(0))

def pr_all(x: list, y: list, w: list):
    for i in x:
        print_with_color(i, 1)
    for a in w:
        print_with_color(a, 2)
        move(wrong_list, ch_list)
    for j in y:
        print_with_color(j, 0)

def check_input():
    letter = screen.getkey()
    if letter == ch_list[0]:
        move(ch_list, done_list)
        cls()
        pr_all(done_list, ch_list)
    elif letter.lower() == "x":
        terminate_curses()
    elif letter != ch_list[0]:
        move(ch_list, wrong_list)
    if len(ch_list) > 0:
        check_input()

def cls():
    screen.erase()


greet()
input("Press enter to start...")
cls()
curses_init()
color_init()
word = get_word()
ch_list = list(word)
curses_print("Type this word:")
curses_print(word)
check_input()

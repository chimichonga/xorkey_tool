#!/bin/env python3
import curses
import string
"""
Tool for modifying a xor key that is returned by xortool or similar to
    see what modified cipher text will be when changing the key.

Author: Chimi <MindTheBox>
License: Don't sue me
"""

FILE_NAME = 'cipher.bin'
XOR_KEY_START = b'xor_key_goes_here'

UNKNOWN_CHAR = '?'

LEGAL_KEY_CHARS = str(string.ascii_letters + string.digits +
            string.punctuation + " ")
LEGAL_CHARS = str(LEGAL_KEY_CHARS + "\n\t\r")


def get_file_content(filename):
    content = b''
    with open(filename, 'rb') as f:
        content = f.read()
    return content


def xor_cipher(cipher, key):
    content = ''
    i=0
    for c in cipher:
        x = chr(c ^ key[i])
        if x not in LEGAL_CHARS:
            x = UNKNOWN_CHAR
        content += x
        i += 1
        if i >= len(key):
            i = 0
    # \r causes issues with output.. https://stackoverflow.com/questions/28669929
    return content.replace("\r\n", "\n").replace("\r", "\n")


def update_key(key, byte_val, i):
    return key[:i] + bytes([byte_val]) + key[i+1:]


def get_key_str(key):
    output = ''
    for c in key:
        if chr(c) not in LEGAL_KEY_CHARS:
            output += UNKNOWN_CHAR
            continue
        output += chr(c)
    return output
        

def main(screen):
    screen.scrollok(True)
    key = XOR_KEY_START
    cipher = get_file_content(FILE_NAME)
    cursor_index = 0
    while True:
        h,w = screen.getmaxyx()
        screen.clear()
        screen.addstr(get_key_str(key))
        screen.addstr('\n%s^\n%s\n' % (' ' * cursor_index, '=' * w))
        content = xor_cipher(cipher, key)
        screen.addstr(content)
        c = screen.getch()
        if c == curses.KEY_RESIZE:
            pass
        elif c == curses.KEY_LEFT:
            cursor_index = max(0, cursor_index-1)
        elif c == curses.KEY_RIGHT:
            cursor_index = min(len(key)-1, cursor_index+1)
        elif c == curses.KEY_UP:
            byte_val = min(255, key[cursor_index]+1)
            key = update_key(key, byte_val, cursor_index)
        elif c == curses.KEY_DOWN:
            byte_val = max(0, key[cursor_index]-1)
            key = update_key(key, byte_val, cursor_index)
        elif chr(c) in LEGAL_KEY_CHARS:
            byte_val = c
            key = update_key(key, byte_val, cursor_index)


if __name__ == "__main__":
    curses.wrapper(main)


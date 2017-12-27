#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

script = ['#include "Keyboard.h"\n\nvoid typeKey(int key)\n{\n  Keyboard.press(key);\n  delay(50);\n '
          ' Keyboard.release(key);\n}\n\nvoid setup()\n{\n  Keyboard.begin();\n  delay(500);\n']


key_code = {" ": "' '", "SPACE": "' '", "ENTER": "KEY_RETURN", "CTRL": "KEY_LEFT_CTRL",
            "SHIFT": "KEY_LEFT_SHIFT", "ALT": "KEY_LEFT_ALT", "GUI": "KEY_LEFT_GUI", "WINDOWS": "KEY_LEFT_GUI",
            "RIGHT": "KEY_RIGHT_ARROW", "RIGHTARROW": "KEY_RIGHT_ARROW", "LEFT": "KEY_LEFT_ARROW",
            "LEFTARROW": "KEY_LEFT_ARROW", "DOWN": "KEY_DOWN_ARROW", "DOWNARROW": "KEY_DOWN_ARROW",
            "UP": "KEY_UP_ARROW", "UPARROW": "KEY_UP_ARROW", "ESC": "KEY_ESC", "ESCAPE": "KEY_ESC",
            "BACK": "KEY_BACKSPACE", "TAB": "KEY_TAB", "INSERT": "KEY_INSERT", "HOME": "KEY_HOME",
            "PAGEUP": "KEY_PAGE_UP", "DELETE": "KEY_DELETE", "END": "KEY_END", "PAGEDOWN": "KEY_PAGE_DOWN",
            "CAPS": "KEY_CAPS_LOCK", "F1": "KEY_F1", "F2": "KEY_F2", "F3": "KEY_F3", "F4": "KEY_F4", "F5": "KEY_F5",
            "F6": "KEY_F6", "F7": "KEY_F7", "F8": "KEY_F8", "F9": "KEY_F9", "F10": "KEY_F10", "F11": "KEY_F11",
            "F12": "KEY_F12"}

in_file = ''
out_file = ''
add = ''


def logo():
    print('     _                _             ______   _               ')
    print('    | |              | |           (_____ \ (_)              ')
    print('  __| | _   _   ____ | |  _  _   _   ____) ) _  ____    ___  ')
    print(' / _  || | | | / ___)| |_/ )| | | | / ____/ | ||  _ \  / _ \ ')
    print('( (_| || |_| |( (___ |  _ ( | |_| || (_____ | || | | || |_| |')
    print(' \____||____/  \____)|_| \_) \__  ||_______)|_||_| |_| \___/ ')
    print('                            (____/                         \n')




def key(key):
    if key in key_code:
        return key_code[key]
    elif (key >= '0') and (key <= '9') or \
         (key >= 'a') and (key <= 'z') or \
         (key >= 'A') and (key <= 'Z'):
         return "'%s'" % key.lower()
    else:
        #print('Error! Unknown key "%s" ' % key)
        return 0


def open_file(file):
    try:
        in_f = open(file, "r")
    except IOError:
        logo()
        print('Error! file "%s" not found' % file)
        sys.exit()
    line = in_f.readline()
    while line:
        parse(line)
        line = in_f.readline()
    script.append('  Keyboard.end();\n}\n\nvoid loop() {}')
    in_f.close()


def write_file(file):
    try:
        out_f = open(file, "w")
        for item in script:
            out_f.write("%s\n" % item)
    except IOError:
        logo()
        print('Error! file "%s" not saved' % file)
        sys.exit()
    finally:
        logo()
        print('Complete.\nOut saved to "%s"' % file)


def parse(str):
    global add
    com = str.strip().split(' ', 1)
    if com[0] == 'REM':
        try:
            add = '  // ' + com[1].strip()
        except IndexError:
            add = '  //'
        script.append(add)
    elif com[0] == 'DELAY':
        try:
            if (not com[1].isdecimal()):
                raise IndexError
            if (int(com[1]) < 1) or (int(com[1]) > 10000):
                logo()
                print('[*] Error, in line "%s" DELAY time is specified in milliseconds from 1 to 10000' % str.strip())
                sys.exit()
            add = '  delay(%s);' % com[1].strip()
            script.append(add)
        except IndexError:
            print('[*] Error, in line "%s" invalid value of milliseconds' % str.strip())
            sys.exit()
    elif com[0] == 'STRING':
        try:
            add = '  Keyboard.print(F("' + com[1].strip().replace('\"', '\\\"') + '"));\n'
            script.append(add)
        except IndexError:
            print('[*] Error, in line "%s" invalid value' % str.strip())
            sys.exit()
    elif com[0] == 'GUI' or com[0] == 'WINDOWS':
        try:
            add = '  typeKey(KEY_LEFT_GUI);\n'
            k = com[1].strip()
            if (len(k) == 1) and (key(k) != 0):
                add = ('  Keyboard.press(KEY_LEFT_GUI);\n  Keyboard.press(%s);\n  Keyboard.releaseAll();\n' %
                       key(com[1].strip().upper()))
                script.append(add)
            else:
                print('[*] Error, in line "%s" invalid value' % str.strip())
                sys.exit()

        except IndexError:
            script.append(add)
    elif com[0] == 'MENU' or com[0] == 'APP':
        add = '  typeKey(229);\n'
        script.append(add)
    elif com[0] == 'SHIFT':
        try:
            add = '  typeKey(KEY_LEFT_SHIFT);\n'
            k = com[1].strip()
            if (len(k) == 1) and (key(k) != 0):
                add = '  Keyboard.press(KEY_LEFT_SHIFT);\n  Keyboard.press(%s);\n  Keyboard.releaseAll();\n' % key(com[1].strip().upper())
                script.append(add)
            else:
                print('[*] Error, in line "%s" invalid value' % str.strip())
                sys.exit()
        except IndexError:
            script.append(add)
    elif com[0] == 'ALT':
        try:
            add = '  typeKey(KEY_LEFT_ALT);\n'
            k = com[1].strip()
            if (len(k) == 1) and (key(k) != 0):
                add = '  Keyboard.press(KEY_LEFT_ALT);\n  Keyboard.press(%s);\n  Keyboard.releaseAll();\n' % key(com[1].strip().upper())
                script.append(add)
            else:
                print('[*] Error, in line "%s" invalid value' % str.strip())
                sys.exit()
        except IndexError:
            script.append(add)
    elif com[0] == 'CONTROL' or com[0] == 'CTRL':
        try:
            add = '  typeKey(KEY_LEFT_CTRL);\n'
            k = com[1].strip()
            if (len(k) == 1) and (key(k) != 0):
                add = '  Keyboard.press(KEY_LEFT_CTRL);\n  Keyboard.press(%s);\n  Keyboard.releaseAll();\n' % key(com[1].strip().upper())
                script.append(add)
            else:
                print('[*] Error, in line "%s" invalid value' % str.strip())
                sys.exit()
        except IndexError:
            script.append(add)
    elif com[0].strip() == 'UP' or com[0].strip() == 'UPARROW':
        add = '  typeKey(KEY_UP_ARROW);\n'
        script.append(add)
    elif com[0].strip() == 'DOWN' or com[0].strip() == 'DOWNARROW':
        add = '  typeKey(KEY_DOWN_ARROW);\n'
        script.append(add)
    elif com[0].strip() == 'LEFT' or com[0].strip() == 'LEFTARROW':
        add = '  typeKey(KEY_LEFT_ARROW);\n'
        script.append(add)
    elif com[0].strip() == 'RIGHT' or com[0].strip() == 'RIGHTARROW':
        add = '  typeKey(KEY_RIGHT_ARROW);\n'
        script.append(add)
    elif com[0].strip() == 'CAPSLOCK':
        add = '  typeKey(KEY_CAPS_LOCK);\n'
        script.append(add)
    elif com[0].strip() == 'DELETE':
        add = '  typeKey(KEY_DELETE);\n'
        script.append(add)
    elif com[0].strip() == 'END':
        add = '  typeKey(KEY_END);\n'
        script.append(add)
    elif com[0].strip() == 'ESC' or com[0].strip() == 'ESCAPE':
        add = '  typeKey(KEY_ESC);\n'
        script.append(add)
    elif com[0].strip() == 'PAGEUP':
        add = '  typeKey(KEY_PAGE_UP);\n'
        script.append(add)
    elif com[0].strip() == 'PAGEDOWN':
        add = '  typeKey(KEY_PAGE_DOWN);\n'
        script.append(add)
    elif com[0].strip() == 'PRINTSCREEN':
        add = '  typeKey(206);\n'
        script.append(add)
    elif com[0].strip() == 'SPACE':
        add = "  typeKey(' ');\n"
        script.append(add)
    elif com[0].strip() == 'TAB':
        add = '  typeKey(KEY_TAB);\n'
        script.append(add)
    elif com[0].strip() == 'ENTER':
        add = '  typeKey(KEY_RETURN);\n'
        script.append(add)
    elif com[0].strip() == 'REPEAT':
        try:
            if (not com[1].strip().isdecimal()):
                raise IndexError
            add = '  for(int i = 0; i < ' + com[1].strip() + '; i++) {\n    %s  \n  }\n' % add.strip()
            script.append(add)
        except IndexError:
            print('[*] Error, in line "%s" invalid value' % str.strip())
            sys.exit()
    elif com[0].strip()[:1] == 'F':
        if com[0].strip().upper() not in key_code:
            print('[*] Error, in line "%s" invalid value' % str.strip())
            sys.exit()
        add = "  typeKey('%s');\n" % key(com[0].strip().upper())
        script.append(add)


if __name__ == "__main__":
    if len(sys.argv) > 3 or len(sys.argv) <= 2:
        logo()
        print('ver 0.1 beta  2017')
        print('usage: ducky2ino.py [infile] [outfile]\n')
        sys.exit()

    try:
        in_file = sys.argv[1]
        out_file = sys.argv[2]
    except IndexError:
        pass

    open_file(in_file)
    write_file(out_file)




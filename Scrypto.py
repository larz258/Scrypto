#!/usr/bin/python
"""
Scrypto - Secure Substitution Cipher
Copyright 2012 Lars Schweighauser

This work is licensed under the GPLv3
A version should have been included with Scrypto (LICENSE.txt)
If you cannot find it, you can read the full license at:
http://opensource.org/licenses/gpl-3.0.html

---
So far I've got an offset range of 2 - 11.
"""

Version = "1.6.4"
Version_Status = "Stable"
#Python_2_7_Status = "Stable"
#Python_3_0_Status = "Stable"
#Python_3_3_Status = "Stable"

from decimal import *
from random import randrange
import sys
import codecs

if sys.version_info[0] == 1:
    print("The 90s called they want their Python 1 back.")
    sys.exit(1)

elif sys.version_info[0] == 2 and sys.version_info[1] >= 7:
    from Tkinter import *
    from tkMessageBox import askquestion
    from tkSimpleDialog import askstring
    import tkFileDialog

elif sys.version_info[0] == 3:
    from tkinter import *
    from tkinter.messagebox import askquestion
    from tkinter.simpledialog import askstring
    import tkinter.filedialog as tkFileDialog

else:
    print("Scrypto does not support Python " + sys.version[0:5:1] + ".\n")
    sys.exit(1)


getcontext().prec = 100


class CORE(object):
    def __init__(self, root):
        self.root = root

    def add_gui(self, gui):
        self.gui = gui

    def encode(self, string, off_set):
        result = []
        for char in string:
            str_ord = ord(char)

            if (256 - off_set) <= str_ord <= 256:
                str_chr = (str_ord - 224 - off_set)

            elif str_ord >= 32:
                str_chr = str_ord + off_set + 1

            else:
                str_chr = str_ord

            result.append(chr(str_chr))
        return ''.join(result)

    def encode_file(self, file, off_set):

        encode_result = ""
        encode_result = []
        file_read = codecs.open(file, 'r', encoding="utf-8")
        lines = file_read.readlines()

        for l in lines:
            encode_result.append(self.encode(l, int(off_set)))
        file_read.close()

        file_write = codecs.open(file, 'w', encoding="utf-8")
        file_write.writelines(''.join(encode_result))
        self.gui.write(''.join(encode_result) + "\n")

    def decode_new_key(self, line, big_key, user_guess, off_set):
        decode_result = []
        for char in line:
            str_ord = ord(char)

            if 32 <= str_ord <= (32 + off_set):
                str_chr = (str_ord + off_set + 206)

            elif str_ord >= (32 + off_set + 1):
                str_chr = (str_ord - off_set - 1)

            else:
                str_chr = str_ord

            decode_result.append(chr(str_chr))
        return ''.join(decode_result)

    def decode_file_new_key(self, file, guess_numb, lines_dependant, off_set):
        guess_result = ""
        big_key = lines_dependant[1]
        small_key = int(lines_dependant[2]) / int(lines_dependant[0])
        key_guess = self.gui.get_string("Guess", "Give me a key to try: ")

        if key_guess is not None and key_guess != "":

            for item in key_guess:
                ord_ = ord(item)
                guess_result += str(ord_)

            if Decimal(big_key) / Decimal(guess_result) == int(small_key):
                file_read = codecs.open(file, 'r', encoding="utf-8")
                lines = file_read.readlines()
                new_result = []

                for item in lines:
                    new_result.append(self.decode_new_key(item, big_key,
                                                          guess_result,
                                                          int(off_set)))
                file_read.close()

                file_write = codecs.open(file, 'w', encoding="utf-8")
                file_write.writelines(''.join(new_result))
                self.gui.write(''.join(new_result) + "\n")
                return

            if guess_numb < 1:
                self.gui.write("You have no more guesses.\n")
                replace_lines = []
                file_write = codecs.open(file, 'w', encoding="utf-8")
                file_write.writelines(replace_lines)
                file_write.close()
                self.gui.quit()
                return

            elif guess_numb == 1:
                self.gui.write("You have " + str(guess_numb)
                                + " guess left.\n")
                guess_numb -= 1
                self.decode_file_new_key(file, guess_numb,
                                         lines_dependant, off_set)

            else:
                self.gui.write("You have "
                                + str(guess_numb)
                                + " guesses left.\n")
                guess_numb -= 1
                self.decode_file_new_key(file, guess_numb,
                                         lines_dependant, off_set)
        return

    def create_key(self, file):
        off_set = self.gui.get_string("Off Set",
                                       "Enter the desired offset (2 - 11)")
        if off_set is not None:

            try:
                if 2 <= int(off_set) <= 12:

                    user_input = self.gui.get_string("Custom Key",
                                                      "Enter a desired key:\n"
                                                      + "alpha-numeric support"
                                                      " since beta 0.7.2)\n")

                    if user_input is not None:
                        write_string = ("Your new key is: "
                                        + user_input +
                                        "\nDon't lose it.\n")
                        self.gui.write(write_string)
                        depend = codecs.open(file, 'r', encoding="utf-8")
                        result = ""

                        for item in user_input:
                            ord_ = ord(item)
                            result += str(ord_)

                        random_mutiplier = randrange(200000, 1500000)
                        new_big_key = int(result) * random_mutiplier
                        write_multiplier = random_mutiplier * int(off_set)

                        new_lines_depend = []
                        new_lines_depend.append(str(off_set) + "\n")
                        new_lines_depend.append(str(new_big_key) + "\n")
                        new_lines_depend.append(str(write_multiplier))

                        depend = codecs.open(file, 'w', encoding="utf-8")
                        depend.writelines(new_lines_depend[::1])
                    depend.close()
                    self.gui.refresh_time(2500)

                else:
                    self.gui.write("The off set is out of range.\n"
                                    + "I need a number betweem 2 and 11\n")

            except ValueError:
                self.gui.write("The off set has to be an integer.\n")
        return

    def create_key_check(self, file):

        depend = codecs.open(file, 'r', encoding="utf-8")
        lines_depend = depend.readlines()

        if lines_depend[1] != "\n":
            guess_result = ""
            big_key = lines_depend[1]
            small_key = int(lines_depend[2]) / int(lines_depend[0])
            check_small_key = Decimal(big_key) / Decimal(str(small_key))
            key_guess = self.gui.get_string("!",
                                             "Please enter the current user"
                                             + " key first.")

            if key_guess is not None:

                if key_guess != '':

                    for item in key_guess:
                        ord_ = ord(item)
                        guess_result += str(ord_)

                    if check_small_key == int(guess_result):
                        self.create_key(file)

                    else:
                        self.gui.write("Sorry, that is not" +
                                        " the current user key.\n")

                else:
                    self.gui.write("You did not enter a key. Try again.\n")

        else:
            self.create_key(file)


class GUI(Frame):
    def __init__(self, core):
        self.core = core
        
    def init_ui(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent

        depend_file = "Depend.txt"
        dependant = codecs.open(depend_file, 'r', encoding="utf-8")
        self.lines_dependant = dependant.readlines()

        title_string = "Scrypto Version " + Version
        self.parent.title(title_string)
        self.pack(fill=BOTH, expand=1)

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        Encode_button = Button(self, text="Encode",
                               command=self.file_dialogue_encode)
        Encode_button.pack()

        Decode_button = Button(self, text="Decode",
                               command=lambda:
                               self.file_dialogue_decode_user_key
                              (self.lines_dependant))
        Decode_button.pack()

        Switch_mode_button = Button(self, text="Set Custom Key",
                                    command=lambda:
                                    self.create_and_quit(depend_file))
        Switch_mode_button.pack()

        self.output = Text(self)
        self.output.pack()
        self.pack()

    def file_dialogue_encode(self):

        if self.lines_dependant[0] != "\n":
            dlg = tkFileDialog.Open(self)
            file = dlg.show()

            if file != "":
                self.core.encode_file(file, self.lines_dependant[0])

        else:
            self.write("Please create a key first.\n")

    def file_dialogue_decode_user_key(self, lines_dependant):
        if self.lines_dependant[0] != "\n":
            dlg = tkFileDialog.Open(self)
            file = dlg.show()

            if file != "":
                self.core.decode_file_new_key(file, 3,
                                                        lines_dependant,
                                                        self.lines_dependant[0]
                                                        )

        else:
            self.write("Please create a key first.\n")

    def create_and_quit(self, depend_file):

        if self.lines_dependant[1] != "\n":
            Overwrite_key_Option = askquestion("User Key Found!", "There is"
                                               + " already a user key, would you"
                                               + " like to overwrite it?")

            if Overwrite_key_Option == "yes":
                self.core.create_key_check(depend_file)

        else:
            self.core.create_key_check(depend_file)

    def write(self, txt):
        self.output.insert(END, str(txt))

    def get_string(self, win_title, win_question):
        string = askstring(win_title, win_question)
        return string

    def refresh(self):
        self.pack_forget()
        self.init_ui(self.parent)

    def refresh_time(self, time_to_sleep):
        sys.stdout.flush()
        self.after(time_to_sleep, self.refresh)


def __main__():
    root = Tk()
    core = CORE(root)
    gui = GUI(core)
    core.add_gui(gui)
    gui.init_ui(root)
    root.geometry("300x250+300+300")
    root.mainloop()

if __name__ == "__main__":
    __main__()
    
    

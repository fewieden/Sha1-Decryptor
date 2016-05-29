from itertools import *
import os
import threading
import queue
import hashlib
import string
import sys
import getopt


class Decryptor:
    UPPERCASE = string.ascii_uppercase
    LOWERCASE = string.ascii_lowercase
    SPACE = string.whitespace
    NUMBERS = string.digits
    SPECIALCHARS = string.punctuation

    def __init__(self, hashcode, options):
        self.hashcode = hashcode

        if 'MAXLENGTH' in options and isinstance(options['MAXLENGTH'], int):
            self.maxlength = options['MAXLENGTH'] + 1
        else:
            self.maxlength = 10

        self.chars = ''
        if 'UPPERCASE' in options and options['UPPERCASE']:
            self.chars += Decryptor.UPPERCASE
        if 'LOWERCASE' in options and options['LOWERCASE']:
            self.chars += Decryptor.LOWERCASE
        if 'SPACE' in options and options['SPACE']:
            self.chars += Decryptor.SPACE
        if 'NUMBERS' in options and options['NUMBERS']:
            self.chars += Decryptor.NUMBERS
        if 'SPECIALCHARS' in options and options['SPECIALCHARS']:
            self.chars += Decryptor.SPECIALCHARS

        self.flag = True
        self.queue = queue.Queue()
        self.pool = []
        for i in range(0, os.cpu_count()):
            t = threading.Thread(target=self.handle)
            t.start()
            self.pool.append(t)

    def decrypt(self):
        for i in range(0, self.maxlength):
            for combination in product(self.chars, repeat=i):
                if not self.flag:
                    break
                self.queue.put(combination)
            else:
                continue
            break
        for i in range(0, len(self.pool)):
            self.queue.put('POISONPILL')

    def handle(self):
        while self.flag:
            combination = self.queue.get()
            password = ''.join(combination)
            h = hashlib.sha1()
            h.update(password.encode('utf-8'))
            password_hash = h.hexdigest()
            if password_hash == self.hashcode:
                self.flag = False
                print(password + ' : ' + password_hash)


def print_help():
    print("\ncommand line arguments:\n" +
          "--help: shows all possible options\n" +
          "-m/--max NUMBER: max length of password\n" +
          "-u/--uppercase: enables uppercase letters\n" +
          "-l/--lowercase: enables lowercase letters\n" +
          "-w/--whitespace: enables whitespace\n" +
          "-n/--lowercase: enables numbers\n" +
          "-s/--specialchars: enables special characters\n" +
          "-h/--hash SHA1HASH: password to decrypt\n")


def main(argv):
    try:
        opts, args = getopt.getopt(argv, "m:ulwnsh:",
                                   [
                                       "help", "max=", "uppercase", "lowercase",
                                       "whitespace", "numbers", "specialchars", "hash="
                                   ])
    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    options = {
        'MAXLENGTH': 8,
        'UPPERCASE': False,
        'LOWERCASE': False,
        'SPACE': False,
        'NUMBERS': False,
        'SPECIALCHARS': False
    }

    sha_hash = ''

    for opt, arg in opts:
        if opt == "--help":
            print_help()
            sys.exit()
        elif opt in ("-m", "--max"):
            options['MAXLENGTH'] = int(arg)
        elif opt in ("-u", "--uppercase"):
            options['UPPERCASE'] = True
        elif opt in ("-l", "--lowercase"):
            options['LOWERCASE'] = True
        elif opt in ("-w", "--whitespace"):
            options['SPACE'] = True
        elif opt in ("-n", "--numbers"):
            options['NUMBERS'] = True
        elif opt in ("-s", "--specialchars"):
            options['SPECIALCHARS'] = True
        elif opt in ("-h", "--hash"):
            sha_hash = arg

    if not sha_hash == '':

        machine = Decryptor(sha_hash, options)

        machine.decrypt()

if __name__ == "__main__":
    main(sys.argv[1:])


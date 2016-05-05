from itertools import *
import os, threading, queue, hashlib


class Decryptor:
    UPPERCASE = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    LOWERCASE = 'abcdefghijklmnopqrstuvwxyz'
    SPACE = ' '
    NUMBERS = '0123456789'
    SPECIALCHARS = '!.:_-,;#?$§&"^°%/()=`*+~<>|²³{[]}\'\\'

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

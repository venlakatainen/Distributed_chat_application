from os import system
from sys import stdout

class Screen:
    def __init__(self):
        self.screen_rows = [" "*119 for _ in range(28)]
        self.rows()
    
    def print(self, *args):
        for arg in args:
            self.screen_rows.pop(0)
            self.screen_rows.append(str(arg))
        self.rows()
        stdout.write("> ")

    def clear(self):
        system('cls')
    
    def refresh(self):
        self.clear()
        self.rows()
        stdout.write("> ")

    def rows(self):
        self.clear()
        stdout.write("\n" + "#"*55 + " chachat " + "#"*55 + "\n")
        for row in self.screen_rows:
            stdout.write(row + "\n")

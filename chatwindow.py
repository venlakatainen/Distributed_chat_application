import curses
import curses.textpad
from message import Message
from datetime import datetime

MY_USERNAME = "Me"

class ChatWindow:
    def __init__(self, user=None, group=None):
        if not (user or group):
            raise ValueError("User or group must be provided")
        elif user and group:
            raise ValueError("Only user or group can be provided. Not both.")
        
        if user:
            self.target = user
        else:
            self.target = group

        self.history = self.get_history_from_log()
        self.other_name = f"[{self.target}]> "
        self.x_buff = len(self.other_name)
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()

    def get_history_from_log(self):
        try:
            with open(f"{self.target}.log", "r") as f:
                #timestamp, user, message
                return f.readlines()
        except FileNotFoundError:
            return []
        
    def add_message(self, message: Message):
        self.chat_window.addstr(f"{message}\n")
        self.chat_window.refresh()

    def get_message(self):
        self.textpad.edit()
        # Get the user's message
        message = self.textpad.gather().strip()

        # Get timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

        # Display the message in the chat window
        self.chat_window.addstr(f"[{timestamp}] {MY_USERNAME}: "+  message + "\n")

        self.clear_input(len(message))

    def clear_input(self, msglen):
        for _ in range(msglen):
            self.textpad.do_command(curses.KEY_BACKSPACE)
        self.chat_window.refresh()
        
    def start(self):
        # Clear screen
        self.stdscr.clear()

        # Set up the chat window
        self.chat_window = curses.newwin(curses.LINES - 5, curses.COLS, 2, 0)
        self.chat_window.scrollok(True)
        self.chat_window.refresh()

        for msg in self.history:
            self.chat_window.addstr(f"{msg}")
        self.chat_window.addstr("\n")
        self.chat_window.refresh()

        # Set up the input box
        self.input_window = curses.newwin(1, curses.COLS-self.x_buff, curses.LINES - 3, self.x_buff)
        self.input_window.refresh()

        name_label = curses.newwin(1, self.x_buff+1, curses.LINES - 3, 0)
        name_label.addstr(0, 0, self.other_name[:19])
        name_label.refresh()

        # Set up textpad for input
        self.textpad = curses.textpad.Textbox(self.input_window, insert_mode=True)

    def end(self):
        curses.nocbreak()
        self.stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        
        

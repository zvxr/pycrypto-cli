
import atexit
import getpass
import platform
import subprocess
import sys
import termios
import tty


class Interface(object):
    """Base class for all commandline interfaces."""
    def __init__(self):
        pass

    def cleanup(self):
        """This is typically called last."""
        pass


class DataInterface(Interface):
    def __init__(
        self,
        clear_on_exit=None,
        clipboard_input=None,
        clipboard_output=None,
        data=None,
        *args,
        **kwargs
    ):
        super(DataInterface, self).__init__()

        self.clear_on_exit = clear_on_exit
        self.clipboard_input = clipboard_input
        self.clipboard_output = clipboard_output
        self.data = data

        if self.clear_on_exit:
            atexit.register(self._clear_screen)

    def _clear_screen(self):
        """Registers an OS clear screen command on application exit."""
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def _get_char(self):
        """Fetch and return a single character input from terminal."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            char = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return char

    def cleanup(self):
        if self.clear_on_exit:
            raw_input("Press ENTER key or CTRL+C to complete.")

    def get_bool_from_prompt(self, prompt="Please type Y or N:"):
        """Locks terminal screen until user enters Y/N. Returns boolean."""
        print(prompt),
        while True:
            char = self._get_char().upper()
            if char in ("Y", "N"):
                print("\r{} {}".format(prompt, char))
                return True if char == "Y" else False

    def get_data(self):
        """Sets data-- prioritizes clipboard, but also will get from prompt. Returns value."""
        if self.clipboard_input:
            self.set_data_from_clipboard()
        if not self.data:
            self.data = self.read_from_file()

        return self.data

    def get_from_prompt(self, prompt="Please enter value: "):
        """A very simple method for inputting data from getpass."""
        return getpass.getpass(prompt)

    def read_from_file(self, path):
        """Return the first non-empty line of a file as a string."""
        with open(path, 'rb') as f:
            return f.read()

    def set_data_from_clipboard(self):
        """Sets data to contents of clipboard."""
        process = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE, close_fds=True)
        stdout, stderr = process.communicate()
        self.data = stdout.decode('utf-8')

    def set_data_from_prompt(self):
        """Prompts for raw input and sets data."""
        data = ""
        print("Please type data. Press ENTER twice or CTRL+C to end.")

        while data[-2:] != "\n\n":
            try:
                data += raw_input()
                data += "\n"
            except KeyboardInterrupt:
                break

        self.data = data.rstrip("\n")

    def store_data_in_clipboard(self):
        """Store data in clipboard."""
        process = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
        stdoutdata, stderrdata = process.communicate(
            input=self.data.encode('utf-8')
        )

    def write_to_file(self, path, data):
        """Write data to file path."""
        with open(path, 'wb') as f:
            f.write(data)


def execute(args):
    """Instantiates interface from argparse namespace and executes.
    Typically child parsers will override this method. Executing at this level
    will simply echo commands in a debug fashion.
    """
    interface = DataInterface(**vars(args))
    data = interface.get_data()

    print "DATA: {}".format(data)

    interface.cleanup()


def add_parser_args(parser):
    """Adds DataInterface related arguments to ArgumentParser and sets execute method.
    Adds positional argument 'xor'.
    Uses switches (d, v, x).
    """
    parser.set_defaults(execute=execute)

    parser.add_argument(
        "--clipboard-input",
        "-x",
        action="store_true",
        help="Data is pulled from clipboard."
    )

    parser.add_argument(
        "--clipboard-output",
        "-v",
        action="store_true",
        help="Data response is stored in clipboard."
    )

    parser.add_argument(
        "--data",
        "-d",
        help="Path to data to manipulate."
    )

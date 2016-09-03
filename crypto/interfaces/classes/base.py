
import atexit


class DataInterface(object):
    def __init__(self, args):
        """args namespace should be derived from add_parser_args."""
        self.data = args.data
        self.clipboard_input = args.clipboard_input
        self.clipboard_output = args.clipboard_output
        if args.clear_on_exit:
            atextit.register(self._clear_screen)

    @staticmethod
    def add_parser_args(parser):
        """Add DataInterface related arguments to ArgumentParser.
        Uses switches (d, x, v, c).
        """
        parser.add_argument(
            "--data",
            "-d",
            help="Raw (string) data to manipulate."
        )

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
            "--clear-on-exit",
            "-c",
            action="store_true",
            help="When True will clear the screen when script completes."
        )

    def _clear_screen(self):
        """Registers an OS clear screen command on application exit."""
        if platform.system() == "Windows":
            os.system("cls")
        else:
            os.system("clear")

    def set_data(self):
        """Takes in raw input and sets data attribute."""
        data = ""
        print("Please type data. Press ENTER twice or CTRL+C to end.")

        while data[-2:] != "\n\n":
            try:
                data += raw_input()
                data += "\n"
            except KeyboardInterrupt:
                break

        self.data = data.rstrip("\n")

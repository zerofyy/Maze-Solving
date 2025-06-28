import os
from sty import fg as Text, bg as Back, ef as Form, rs as Rest


class Coloring:
    """ Utilities for coloring text in the terminal. """

    codes = {
        'fb' : Form.bold, 'fi' : Form.italic, 'fu' : Form.underl, 'fs' : Form.strike, 'rs' : Rest.all,
        'lr' : Text.li_red, 'bglr' : Back.li_red,
        'r' : Text.red, 'bgr' : Back.red,
        'lg' : Text.li_green, 'bglg' : Back.li_green,
        'g' : Text.green, 'bgg' : Back.green,
        'ly' : Text.li_yellow, 'bgly' : Back.li_yellow,
        'y' : Text.yellow, 'bgy' : Back.yellow,
        'lb' : Text.li_blue, 'bglb' : Back.li_blue,
        'b' : Text.blue, 'bgb' : Back.blue,
        'lm' : Text.li_magenta, 'bglm' : Back.li_magenta,
        'm' : Text.magenta, 'bgm' : Back.magenta,
        'lc' : Text.li_cyan, 'bglc' : Back.li_cyan,
        'c' : Text.cyan, 'bgc' : Back.cyan
    }


    @staticmethod
    def init() -> None:
        """ Run a system call to enable colors in the terminal. """

        os.system('')


    @staticmethod
    def color(string: str) -> str:
        """
        Color a string.

        Arguments:
            string: A string containing color codes.

        Returns:
            The same string with the color codes replaced by actual color values.
        """

        for code, color in Coloring.codes.items():
            string = string.replace(f'[{code}]', color)

        return string


    @staticmethod
    def uncolor(string: str) -> str:
        """
        Remove all color codes from a string.

        Arguments:
            string: A string containing color codes.

        Returns:
            The same string with the color codes removed.
        """

        for code in Coloring.codes:
            string = string.replace(f'[{code}]', '')

        return string


    @staticmethod
    def length(string: str) -> int:
        """
        Get the length of a string with color codes.

        Arguments:
             string: A string containing color codes.

        Returns:
            The length of the string while ignoring color codes.
        """

        string = Coloring.uncolor(string)
        return len(string)


    @staticmethod
    def _parse_tokens(string: str) -> list[str]:
        """ Helper function for parsing strings containing color codes. """

        tokens = []
        char_idx = -1
        while char_idx + 1 < len(string):
            char_idx += 1
            char = string[char_idx]

            if char != '[':
                tokens.append(char)
                continue

            end_tag = string.find(']', char_idx + 1)
            if end_tag == -1:
                tokens.append(char)
                continue

            code = string[char_idx + 1 : end_tag]
            if code in Coloring.codes:
                tokens.append(f'[{code}]')
                char_idx = end_tag
                continue

            tokens.append(char)
            continue

        return tokens


    @staticmethod
    def cut(string: str, length: int | list[int, int]) -> str:
        """
        Cut a string with color codes.

        Arguments:
             string: A string containing color codes.
             length: Maximum length of the string or a list with indexes (from, to).

        Returns:
            The same string cut to fit the given length while ignoring color codes.
            The returned string will always end with a reset code.
        """

        if isinstance(length, int):
            length = [0, length]

        str_len = Coloring.length(string)
        if length[0] < 0:
            length[0] = str_len + length[0]
        if length[1] < 0:
            length[1] = str_len + length[1]
        length[1] = length[1] + 1

        if length[0] >= length[1]:
            return '[rs]'

        new_str = ''
        char_idx = 0
        for char in Coloring._parse_tokens(string):
            is_code = len(char) > 1

            if is_code:
                if char_idx >= length[0]:
                    new_str += char
                continue

            if char_idx >= length[1]:
                break

            if char_idx >= length[0]:
                new_str += char
            char_idx += 1

        return new_str + '[rs]'


    @staticmethod
    def chars(string: str) -> list[str]:
        """
        Get a list of characters along with color codes.

        Arguments:
             string: A string containing color codes.

        Returns:
            A list of characters where some characters are paired along with color codes.
        """

        chars = []
        pending_code = ''
        for char in Coloring._parse_tokens(string):
            is_code = len(char) > 1

            if is_code:
                pending_code += char
                continue

            if pending_code:
                chars.append(f'{pending_code}{char}')
                pending_code = ''
                continue

            chars.append(char)

        if pending_code:
            chars[-1] += pending_code

        return chars


__all__ = ['Coloring']

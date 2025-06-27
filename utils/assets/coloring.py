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

        colored_str = ''
        color_code, reading_code = '', False

        for char in string:
            if char == '[':
                if reading_code:
                    colored_str += f'[{color_code}'
                color_code, reading_code = '', True
                continue

            if char == ']':
                colored_str += Coloring.codes.get(color_code, f'[{color_code}]' if color_code else ']')
                color_code, reading_code = '', False
                continue

            if reading_code:
                color_code += char
            else:
                colored_str += char

        return colored_str


    @staticmethod
    def uncolor(string: str) -> str:
        """
        Remove all color codes from a string.

        Arguments:
            string: A string containing color codes.

        Returns:
            The same string with the color codes removed.
        """

        new_str = ''
        color_code, reading_code = '', False

        for char in string:
            if char == '[':
                if reading_code:
                    new_str += f'[{color_code}'
                color_code, reading_code = '', True
                continue

            if char == ']':
                if color_code not in Coloring.codes:
                    new_str += f'[{color_code}]' if color_code else ']'

                color_code, reading_code = '', False
                continue

            if reading_code:
                color_code += char
            else:
                new_str += char

        return new_str


    @staticmethod
    def length(string: str) -> int:
        """
        Get the length of a string with color codes.

        Arguments:
             string: A string containing color codes.

        Returns:
            The length of the string while ignoring color codes.
        """

        length = 0
        color_code, reading_code = '', False

        for char in string:
            if char == '[':
                if reading_code:
                    length += len(color_code) + 1
                color_code, reading_code = '', True
                continue

            if char == ']':
                if color_code not in Coloring.codes:
                    length += len(color_code) + (2 if color_code else 1)
                color_code, reading_code = '', False
                continue

            if reading_code:
                color_code += char
            else:
                length += 1

        return length


    @staticmethod
    def _cut_invalid_code(invalid_code: str, str_idx: int, length: list[int, int]) -> tuple[str, int]:
        """ Helper function for cutting invalid color codes to fit within the specified length. """

        if str_idx == length[1]:
            return '', str_idx

        cut_code = ''
        for char in invalid_code:
            str_idx += 1
            if str_idx >= length[0]:
                cut_code += char
            if str_idx == length[1]:
                break

        return cut_code, str_idx


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

        new_str, str_idx = '', -1
        color_code, reading_code = '', False

        for char in string:
            if char == '[':
                if reading_code:
                    chars, str_idx = Coloring._cut_invalid_code(f'[{color_code}', str_idx, length)
                    new_str += chars

                color_code, reading_code = '', True
                continue

            if char == ']':
                if color_code in Coloring.codes:
                    new_str += f'[{color_code}]'
                elif reading_code:
                    chars, str_idx = Coloring._cut_invalid_code(f'[{color_code}]', str_idx, length)
                    new_str += chars
                else:
                    chars, str_idx = Coloring._cut_invalid_code(']', str_idx, length)
                    new_str += chars

                color_code, reading_code = '', False
                continue

            if reading_code:
                color_code += char
                continue

            str_idx += 1
            if str_idx >= length[0]:
                new_str += char
            if str_idx == length[1]:
                break

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
        color_code, reading_code = '', False

        for char in string:
            if char == '[':
                if reading_code:
                    chars.extend(list(f'[{color_code}'))

                color_code, reading_code = '', True
                continue

            if char == ']':
                if color_code and color_code in Coloring.codes:
                    pass
                elif reading_code:
                    chars.extend(list(f'[{color_code}]'))
                    color_code = ''
                else:
                    chars.append(']')
                    color_code = ''

                reading_code = False
                continue

            if reading_code:
                color_code += char
                continue

            if color_code:
                chars.append(f'[{color_code}]{char}')
                color_code = ''
            else:
                chars.append(char)

        if color_code:
            chars[-1] = f'{chars[-1]}[{color_code}]'

        return chars


__all__ = ['Coloring']

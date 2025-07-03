import re

from .coloring import Coloring


class ListMaker:
    """ Making visually appealing lists from strings by filling blank spaces with information. """

    @staticmethod
    def fill(text: str, info: list[tuple[str, str]]) -> str:
        """
        Fill in the blanks of a string.

        Functionality:
            The function will iterate through each item in the information list
            and replace the first found blank space with the current information
            until there are no more items or blank spaces.

        Information List:
            Items in the information list must in order of blank spaces in the
            string. Each item must contain two strings: replacement text and a
            direction. The replacement text is what blank spaces are replaced
            with, while the direction is which way to align the text after it
            is replaced ("left" or "right").

        Arguments:
             text: A string with blank spaces ( _ ).
             info: An ordered list containing replacement strings and alignment directions.
        """

        sections = [len(match) for match in re.findall(r'_+', text)]
        index = 0

        for rp_text, direction in info:
            section = '_' * sections[index]
            offset = len(rp_text) - Coloring.length(rp_text)

            if direction == 'left':
                text = text.replace(section, f'{rp_text:<{sections[index] + offset}}', 1)
            else:
                text = text.replace(section, f'{rp_text:>{sections[index] + offset}}', 1)
            index += 1

        return text



__all__ = ['ListMaker']

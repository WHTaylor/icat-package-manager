import re

version_patt = re.compile(r"^(\d+)\.(\d+)\.(\d+)(-(.+))?")


class Version:
    def __init__(self, string):
        m = version_patt.match(string)
        self._x = m.group(1)
        self._y = m.group(2)
        self._z = m.group(3)
        self._suffix = m.group(5)

    def __repr__(self):
        v = f"{self._x}.{self._y}.{self._z}"
        return v if not self._suffix else f"{v}-{self._suffix}"

    @staticmethod
    def is_valid(string):
        """Check if a string is a valid version number

        >>> test="1.1.1"
        >>> missing_one = [test[:i] + test[i + 1:] for i in range(len(test))]
        >>> all(not Version.is_valid(tc) for tc in missing_one)
        True
        >>> valid_strings = ["1.2.3", "20.50.1", "1.1.000-ASDF"]
        >>> all(Version.is_valid(tc) for tc in valid_strings)
        True
        """
        return version_patt.match(string) is not None


if __name__ == "__main__":
    import doctest

    doctest.testmod()

class DiffRange:
    """
    This class stores the output of the lhdiff script. It contains a list of tuples that represent the line
    number in the left revision and the corresponding line number in the right revision, and vice-versa.

    Attributes
    ----------
    range: tuple
        the list of tuples. The first element is the line number on the left, while the second is the line number
        on the right.
    """

    def __init__(self, range):
        self.range = range
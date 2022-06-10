from src.change.revision import CommitFile


class ModifiedFile(CommitFile):
    """
    This class represents a file which has been modified in a commit. It is part of the initial
    vulnerability evidence.

    Attributes
    ----------
    added_lines: list of Line
        the list of code lines which has been added in the commit
    removed_lines: list of Line
        the list of code lines which has been removed in the commit
    slice: list of Line
        the slice obtained by running the added and removed lines through the slicing algorithm.
        It constitutes the initial vulnerability evidence which is searched backwards in the
        commit history to determine if a given commit still contains the vulnerability
    is_present: bool
        this flag is true if at least one line of the slice is still present in the evidence
    """
    __doc__ += CommitFile.__doc__

    def __init__(self, commit_hash, file_name, parent, diff, added_lines, removed_lines, new_revision, old_revision, method_list=[], slice=[], is_present=True):
        CommitFile.__init__(self, commit_hash, file_name, parent, diff, new_revision, old_revision, method_list)
        self.added_lines = added_lines
        self.removed_lines = removed_lines
        self.slice = slice
        self.is_present = is_present

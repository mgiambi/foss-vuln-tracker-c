class CommitFile:
    """
    This class represents a single file in a given commit.

    Attributes
    ----------
    commit_hash: str
        the hash of the commit which the file is a part of
    file_name: str
        the name of the file, including path
    new_revision: list of Line
        the list of code lines present in the file, AFTER the commit changes
    old_revision: list of Line
        the list of code lines present in the file, BEFORE the commit changes
    parent: str
        the hash of the parent commit
    method_list: list of str
        the list of names of the methods in the file, both before and after the commit
    diff: list of tuple
        the list of lines as extracted by lhdiff tool
    """

    def __init__(self, commit_hash, file_name, parent, diff = [], new_revision = [], old_revision = [], method_list = []):
        self.commit_hash = commit_hash
        self.file_name = file_name
        self.new_revision = new_revision
        self.old_revision = old_revision
        self.parent = parent
        self.method_list = method_list
        self.diff = diff

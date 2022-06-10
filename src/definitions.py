import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
LEFT_REVISION_FILE = os.path.join(ROOT_DIR, "left_revision.txt")
RIGHT_REVISION_FILE = os.path.join(ROOT_DIR, "right_revision.txt")
LHDIFF_PATH = os.path.join(ROOT_DIR, "ldiff_wrapper/lhdiff_2020.jar")
EXTENSIONS = [".c", ".cpp", ".cc", ".cxx", ".h", ".hpp", ".hxx", ".hh"]
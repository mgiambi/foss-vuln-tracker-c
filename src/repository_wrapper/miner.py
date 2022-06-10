from pydriller import RepositoryMining
from src.change.line import Line
from src.change.change import ModifiedFile
from src.change.revision import CommitFile
from src.ldiff_wrapper.diff import Diff
from src.definitions import LEFT_REVISION_FILE, RIGHT_REVISION_FILE
import os

class RepositoryMiner:

    def __init__(self, repo_path):
        self.repo_path = repo_path

    def __filter_lines(self, revision_lines, seed_lines):
        """
        This method is used when gathering the initial vulnerability evidence. It filters the
        code lines of the modified file to exclude the lines that are not part of the the modified
        methods. This greatly improves the performance of the slicing algorithm.

        Parameters
        ----------
        revision_lines: list of Line
            the lines to filter
        seed_lines: list of Line
            the collection of added and removed lines from the commit

        Returns
        -------
        list of Line:
            the list of filtered lines
        """
        seed_method_names = [line.method_name for line in seed_lines]
        return [line for line in revision_lines if line.method_name in seed_method_names]

    def __get_line_with_method(self, line, method_list):
        """
        This method is used to create a Line object from the line text extracted by the repository miner.
        It loops through the methods in the commit to find to which method the line belongs; if no method
        is found, None is returned.

        Parameters
        ----------

        line: str
            the line text
        method_list: list of Method
            the list of methods

        Returns
        -------
        Line:
            the line object created, or None
        """
        line_number = line[0]
        line_code = ' '.join(line[1].split())

        for method in method_list:
            if line_number in range(method.start_line, method.end_line + 1):
                return Line(line_number, line_code, method.start_line, method.end_line, method.name)

        return None

    def __format_source(self, source_code, method_list):
        """
        This method takes the code lines from a revision and put them into Line objects, leaving out
        the lines that are not included in a method (due to the limitations of intra-procedural slicing).
        Thus, such lines will not be included in the initial vulnerability evidence.

        Parameters
        ----------
        source_code: list
            list of code lines from the revision, each element is a list with two items: the line number
            and the line text.
        method_list:
            the list of methods

        Returns
        -------
        list of Line:
            the list of Line objects
        """
        if source_code is None:
            return []

        code_lines = source_code.splitlines()
        code_list = []
        index = 1

        for line in code_lines:
            code_list.append([index, line])
            index += 1

        return_list = [self.__get_line_with_method(element, method_list) for element in code_list]
        return [i for i in return_list if i]

    def get_commit_changes(self, extensions, commit_hash, initial, evidence_list=None):
        """
        This method traverse a single commit to find the list of files that are relevant for the
        program execution.

        Parameters
        ----------
        extensions: list of str
            the list of files extensions to consider. All files whose extention is not included in
            the list will be ignored
        commit_hash: str
            the hash of the commit to traverse
        initial: bool
            if true, this method is called to gather the initial evidence
        evidence_list: list of CommitFile
            contains the list of files in the vulnerability evidence. All files in the commit that
            are not also in this list are ignored (they do not contain tainted lines). If initial
            is true, the list is empty and it is ignored for this iteration

        Returns
        -------
        list of CommitFile:
            the list of relevant files in the commit. If initial is true, all the modified files
            in the commit are returned. Otherwise, the files included in the initial evidence are
            returned instead.
        """

        for commit in RepositoryMining(self.repo_path, single=commit_hash).traverse_commits():

            modified_files = []
            diff_maker = Diff()

            if len(commit.parents):
                parent = commit.parents[0]
            else:
                parent = None

            for m in commit.modifications:
                filename, file_extension = os.path.splitext(m.filename)

                if initial or (m.new_path in [ev.file_name for ev in evidence_list] and not initial):
                    added_lines = []
                    removed_lines = []

                    if file_extension in extensions and commit.in_main_branch:
                        if m.old_path is not None and m.old_path != m.new_path:
                            file_name = m.old_path
                        else:
                            file_name = m.new_path

                        # Saves the entire file content into a new file so it can be opened by the
                        # lhdiff tool
                        with open(LEFT_REVISION_FILE, "w") as file:
                            file.write(m.source_code_before if m.source_code_before is not None else "")
                        with open(RIGHT_REVISION_FILE, "w") as file:
                            file.write(m.source_code if m.source_code is not None else "")

                        diff = diff_maker.make_diff(LEFT_REVISION_FILE, RIGHT_REVISION_FILE)

                        if initial:
                            for element in m.diff_parsed['added']:
                                line = self.__get_line_with_method(element, m.changed_methods)
                                if line is not None:
                                    added_lines.append(line)
                            for element in m.diff_parsed['deleted']:
                                line = self.__get_line_with_method(element, m.methods_before)
                                if line is not None:
                                    removed_lines.append(line)

                            old_revision = self.__format_source(m.source_code_before, m.methods_before)
                            new_revision = self.__format_source(m.source_code, m.methods)

                            modified_lines = added_lines
                            modified_lines.extend(removed_lines)
                            old_revision = self.__filter_lines(old_revision, modified_lines)
                            new_revision = self.__filter_lines(new_revision, modified_lines)
                            modified_files.append(ModifiedFile(commit_hash, file_name, parent, diff, added_lines, removed_lines, new_revision, old_revision))
                        else:                           
                            modified_files.append(CommitFile(commit_hash, file_name, parent, diff))

            return modified_files, parent

    def get_commits_to_traverse(self, target_commit):
        """
        This method returns the list of commits prior to the input commit, ingoring merge commits.

        Parameters
        ----------
        target_commit: str
            the commit hash of the target commit

        Returns
        -------
        list of str:
            the list of commit hashes of all previous commits
        """

        commit_list = []

        for commit in RepositoryMining(self.repo_path, to_commit=target_commit, only_no_merge=True).traverse_commits():
            if(commit.hash != target_commit):
                commit_list.append(commit.hash)

        return reversed(commit_list)

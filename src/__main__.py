from src.repository_wrapper.miner import RepositoryMiner
from src.lexer.tokenizer import Tokenizer
from src.slicer.slicer import Slicer
from src.tracker.tracker import VulnerabilityTracker
from src.change.revision import CommitFile
from src.definitions import LEFT_REVISION_FILE, RIGHT_REVISION_FILE, EXTENSIONS
from typing import List
from datetime import datetime
import time
import sys
import argparse
import json
import os


def find_present_evidence(evidence_list: List[CommitFile]) -> List[CommitFile]:
    return [evidence for evidence in evidence_list if evidence.is_present is True]


"""
MAIN PROGRAM


Workflow:

    1.  Traverse the target commit, or the commit in which the vulnerability is fixed
        1.1.    Extract the initial vulnerability evidence (slice) from the commit

    2.  Get all commits previous to the one that contains the initial evidence. For each commit:
        2.2.    Traverse it to get the information needed
        2.3.    Check whether any of the lines in the initial evidence is present in the commit. All
                the lines that are not present are removed from the evidence

    3.  When a commit is reached where none of the lines in the initial evidence are present, or
        when the first commit is reached, or if the target commit contains no changes, the program stops
"""

def main():

    tokenizer = Tokenizer()
    slicer = Slicer()
    tracker = VulnerabilityTracker()

    output_dict = {}

    start_time = datetime.now()

    # User input processing with argparse
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('output_file_path', type=str, help="path to the output json file")
    parser.add_argument('repository_path', type=str, help="path to the repository to check for vulnerabilities")
    parser.add_argument('commit_hash', type=str, help="hash of the commit that fixed the vulnerability")
    parser.add_argument('--test_hash', type=str, help="hash of the commit preceeding the one that introduced the vulnerability, used for testing purposes")
    args = parser.parse_args()
    extensions = EXTENSIONS
    repo_path = args.repository_path
    commit_hash = args.commit_hash
    test_first_non_vuln_commit = args.test_hash if args.test_hash is not None else ""

    if not os.path.isabs(repo_path):
        repo_path = os.getcwd() + "/" + repo_path

    repo_miner = RepositoryMiner(repo_path)

    print("\nPROGRAM STARTED! PLEASE WAIT...\n")

    # Point 1
    changes, parent_hash = repo_miner.get_commit_changes(extensions, commit_hash, True)

    if not changes:
        print("NO MODIFICATIONS IN TARGET COMMIT. EXITING...\n")

    else:
        final_evidence = []
        output_dict["initial_evidence"] = {}
        output_dict["initial_evidence"]["commit_hash"] = changes[0].commit_hash
        print("GATHERING INITIAL EVIDENCE FROM COMMIT " + changes[0].commit_hash + "...")
        # Point 1.1
        output_dict["initial_evidence"]["files"] = []
        for change in changes:
            change_dict = {}
            change_dict["file_name"] = change.file_name
            change.new_revision = tokenizer.tokenize(change.new_revision)
            change.old_revision = tokenizer.tokenize(change.old_revision)
            change.added_lines = slicer.remove_useless_lines(tokenizer.tokenize(change.added_lines))
            change.removed_lines = slicer.remove_useless_lines(tokenizer.tokenize(change.removed_lines))
            change.slice = slicer.make_slice(change, True)
            change_dict["slice"] = []
            for line in sorted(change.slice, key=lambda x: x.line_number):
                slice_dict = {}
                slice_dict["method_name"] = line.method_name
                slice_dict["line_number"] = line.line_number
                slice_dict["line_text"] = line.line_text
                change_dict["slice"].append(slice_dict)
            output_dict["initial_evidence"]["files"] .append(change_dict)
            if len(change.slice):
                final_evidence.append(change)
        print("EVIDENCE GATHERED FROM " + str(len(changes)) + " MODIFIED FILES!\n")

        # Point 2
        commits = repo_miner.get_commits_to_traverse(commit_hash)

        count = 1
        first_non_vulnerable_commit = "None"

        output_dict["commit_list"] = []
        for commit in commits:
            if not(len(find_present_evidence(final_evidence))):
                break

            else:
                # Point 2.2
                revision, parent_hash = repo_miner.get_commit_changes(extensions, commit, False, [ev for ev in find_present_evidence(final_evidence)])
                if parent_hash is not None:
                    count += 1

                    commit_dict = {}
                    commit_dict["commit_hash"] = commit
                    commit_dict["evidence"] = []
                    print("TRACKING COMMIT: " + commit + " (ITERATION " + str(count) + ")")
                    for evidence in final_evidence:
                        if evidence.is_present:
                            evidence_dict = {}
                            evidence_dict["file_name"] = evidence.file_name
                            evidence_dict["changes"] = []
                            for change in revision:
                                if change.file_name == evidence.file_name and len(evidence.slice):
                                    
                                    # Point 2.3
                                    evidence.slice = tracker.find_evidence(change, evidence.slice)
                                    if len(evidence.slice):
                                        for line in evidence.slice:
                                            change_dict = {}
                                            change_dict["method_name"] = line.method_name
                                            change_dict["line_number"] = line.line_number
                                            change_dict["line_text"] = line.line_text
                                            evidence_dict["changes"].append(change_dict)
                                    else:
                                        evidence.is_present = False
                                commit_dict["evidence"].append(evidence_dict)

                    first_non_vulnerable_commit = parent_hash

            output_dict["commit_list"].append(commit_dict)

        if test_first_non_vuln_commit != "":
            if first_non_vulnerable_commit == test_first_non_vuln_commit:
                test_first_string = "TEST SUCCESSFUL!\n"
                test_first_bool = "true"
            else:
                test_first_string = "TEST FAILED!\n"
                test_first_bool = "false"

        output_dict["commits_traversed"] = count
        output_dict["start_time"] = start_time.strftime('%c')
        output_dict["end_time"] = datetime.now().strftime('%c')
        output_dict["first_non_vulnerable_commit"] = first_non_vulnerable_commit
        
        print("\nEND OF EXECUTION!")
        print("COMMITS TRAVERSED: " + str(count))
        print("FIRST NON-VULNERABLE COMMIT: " + first_non_vulnerable_commit)

        if test_first_non_vuln_commit != "":
            output_dict["test_passed"] = test_first_bool
            print(test_first_string)

        os.remove(LEFT_REVISION_FILE)
        os.remove(RIGHT_REVISION_FILE)

    with open(args.output_file_path, 'w') as output_file:
        json.dump(output_dict, output_file, indent=4, sort_keys=True)

## About

This is an implementation of [foss-vuln-tracker](https://github.com/standash/foss-vuln-tracker) that works with projects written in C/C++. It should be noted that the currently the tool does not handle pointers when performing the slicing of vulnerable code.

The project uses the [LHDiff](https://muhammad-asaduzzaman.com/research/) executable to make comparisons between the different revisions of the same file.

## Usage

#### Prerequisites

1. Python version between 3.0 and 3.8
2. [PyDriller](https://github.com/ishepard/pydriller) version 1.15
3. [Ply](https://pypi.org/project/ply/)
4. Java compiler and runtime (tested with version 16)

#### Installation

1. Clone the repository: ```git clone https://github.com/mgiambi/foss-vuln-tracker-C.git```
2. Move into the project folder and install the tool with the command: ```python setup.py install```

#### Basic usage

If you successfullt completed the installation, you can run the tool from the terminal with the command ```vuln-tracker-c```. You also need to add a few parameters, which are, in order:

1. The path to the output (JSON) file
2. The path to the git project which is to be searched for the vulnerability
3. The hash of the commit in which the vulnerability has been fixed
4. (optional) the hash of the latest commit which does not contain the vulnerability. Used for testing

To display the list of options, just add the "-h" option when running the command.

The output JSON file has the following structure:

```
{ 
    commit_list: [                                          -> the list of commits traversed by the tool
        {
            commit_hash: str                                -> the commit hash
            evidence: [                                     -> the list of files included in the initial 
                                                               vulnerability evidence that have been modified 
                                                               in this commit
                            changes: [                      -> the list of code lines in the initial 
                                                               vulnerability evidence that are still present 
                                                               in this commit
                                        line_number: int    -> the line number
                                        line_text: str      -> the line text
                                        method_name: str    -> name of the method containing the line
                            ]
                            file_name: str                  -> name of the file
            ]
        }
    ]
    commits_traversed: int                                  -> number of commits traversed
    end_time: str                                           -> time when the program ended
    first_non_vulnerable_commit: str                        -> hash of the most recent non-vulnerable commit
    initial_evidence: [                                     -> list of files in the initial vulnerability 
                                                               evidence
        {
            file_name: str                                  -> name of the file
            slice: [                                        -> list of code lines tat constitute the slice for 
                                                               each file
                        line_number: int                    -> the line number
                        line_text: str                      -> the line text
                        method_name: str                    -> name of the method containing the line
            ]
        }
    ]
    start_time: str                                         -> time when the program started
    test_passed: str                                        -> if "test_hash" was provided, indicates whether 
                                                               the test has been passed or not
}
```

NOTE: the program needs to read and write some files to allow the lhdiff tool to work correctly; thus, depending on where it is installed, it will probably need to be launched with administrator privleges.

NOTE: in some machines the tool return the following error message: ```SHA could not be resolved```. This is due to some bug in GitPython, a library used by PyDriller. To fix this, you need to modify the PyDriller files. Find git_repository.py (in linux distros, it is probably located in a path similar to this: /usr/local/lib/<your-python-version>/dist-packages/<your-pydriller-version.egg>/pydriller) and make the following changes:

Line 0
``` diff
+ import git
```

Line 100
```diff
- self._repo = Repo(str(self.path))
+ self._repo = Repo(str(self.path), odbt=git.db.GitDB)
```

## References

S. Dashevskyi, A. D. Brucker and F. Massacci, "A Screening Test for Disclosed Vulnerabilities in FOSS Components," in IEEE Transactions on Software Engineering. doi: 10.1109/TSE.2018.2816033 URL: http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=8316943&isnumber=4359463

https://github.com/standash/foss-vuln-tracker

https://muhammad-asaduzzaman.com/research/

## License

This project is licensed under the [GPL 3.0 License](https://www.gnu.org/licenses/gpl-3.0.en.html).

import pathlib
from setuptools import find_packages, setup

setup(
    name="vuln-tracker-c",
    version="1.0.0",
    #long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/mgiambi/vuln-tracker-c",
    author="Michael Giambi",
    author_email="michael.giambi@studenti.unitn.it",
    license_files=('LICENSES/LICENSE.txt'),
    packages=["src", "src.change", "src.ldiff_wrapper", 
        "src.lexer", "src.repository_wrapper", "src.slicer", "src.tracker"],
    python_requires='>=3.0, <3.9',
    data_files=[("src/ldiff_wrapper/", ["src/ldiff_wrapper/lhdiff_2020.jar"])],
    install_requires=[
        "pydriller==1.15",
        "ply"],
    entry_points={
        "console_scripts": [
            "vuln-tracker-c=src.__main__:main",
        ]
    },
)

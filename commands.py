import json
import subprocess
from pathlib import Path

import fire


COLAB_TEMPLATE = """`{}`: [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/girafe-ai/ml-course/blob/{}/{}/{})\n"""
MODES = {"overwrite": "w", "append": "a"}


def read_json(filename, **kwargs):
    """Reads data from json-file.

    Args:
        filename: name of the json-file.
        **kwargs: arguments from ``json.load()`` method.

    Returns:
        Data from json-file.
    """
    with open(filename) as file:
        return json.load(file, **kwargs)


def write_json(data, filename, *, newline: bool = False, **kwargs):
    """Writes dictionary to json-file.

    Args:
        data: dictionary to save.
        filename: name of the json-file.
        newline: to put neline symbol at the end of the file or not
        **kwargs: arguments from ``json.dump()`` method.

    Returns:
        Path to saved file (may differ in suffix from original)
    """
    filename = Path(filename)
    if not len(filename.suffix):
        filename = filename.with_suffix(".json")
    with open(filename, "w") as file:
        json.dump(data, file, **kwargs)
        if newline:
            file.write("\n")
    return filename


def backslash_fix(*fnames: tuple):
    """Replaces all the backslashes in notebook's markdown cells to break tag.

    Needed since Github don't render backslashes correctly =(

    Args:
        fname: path to jupyter notebook (.ipynb) to process
    """
    BACKSLASH = "\\\n"
    TWO_BACKSLASHES = "\\\\\n"
    BR_TAG = "<br>\n"

    for fname in fnames:
        notebook = read_json(fname)

        for cell in notebook["cells"]:
            if cell["cell_type"] != "markdown":
                continue

            fixed = []
            for line in cell["source"]:
                if line.endswith(BACKSLASH) and not line.endswith(TWO_BACKSLASHES):
                    line = line.replace(BACKSLASH, BR_TAG)
                fixed.append(line)
            cell["source"] = fixed

        write_json(notebook, fname, newline=True, ensure_ascii=False, indent=1)


def colab(directory: str, branch: str = "current", mode: str = "overwrite"):
    """Creates README file with links to Colab

    Args:
        directory: path in root of ml-mipt repo to generate README file for
        branch: branch for which generate links, should be name of existing branch or 'current'
        mode: 'overwrite' or 'append' - way to deal with README

    Example:
        >>> python commands.py colab week0_01_knn_naive_bayes
    """
    dir_path = Path(directory)
    if branch == "current":
        completed = subprocess.run("git rev-parse --abbrev-ref HEAD".split(), capture_output=True)
        branch = completed.stdout.strip().decode("utf-8")

    links = [
        COLAB_TEMPLATE.format(path.stem, branch, dir_path.name, path.name)
        for path in sorted(dir_path.glob("*.ipynb"))
    ]

    with open(dir_path / "README.md", MODES[mode]) as file:
        file.write("\n".join(links))


if __name__ == "__main__":
    fire.Fire()

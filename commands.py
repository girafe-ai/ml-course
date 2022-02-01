import subprocess
from pathlib import Path

import fire


COLAB_TEMPLATE = """`{}`:[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/girafe-ai/ml-mipt/blob/{}/{}/{})\n"""
MODES = {"overwrite": "w", "append": "a"}


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

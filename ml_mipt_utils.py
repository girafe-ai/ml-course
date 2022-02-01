from pathlib import Path
from typing import Optional

import requests
import tqdm


def download_file(url: str, save_path: Optional[str] = None, verbose: bool = False) -> Path:
    """Download file with `requests` visualizing progressbar with `tqdm`

    Args:
        url: web adress to download file from
        save_path: address on local filesystem to save downloaded file to.
            If this is directory or None - original filename will be used.
        verbose: Show progressbar or not

    Returns:
        Path object leading to saved file

    Example:
        saved_fname = download_file("https://gin.g-node.org/v-goncharenko/ml-mipt/raw/master/data/Train_rev1.csv.zip")
    """
    chunk_size = 1024  # one kilobyte

    if save_path is None:
        path = Path()
    else:
        path = Path(save_path)
    if path.is_dir():
        path = path / url.split("/")[-1]

    req = requests.get(url, stream=True)
    file_size = int(req.headers["Content-Length"])
    num_bars = int(file_size / chunk_size)

    with open(path, "wb") as file:
        for chunk in tqdm.tqdm(
            req.iter_content(chunk_size=chunk_size),
            total=num_bars,
            unit="KB",
            desc=path,
            leave=True,
        ):
            file.write(chunk)

    return path

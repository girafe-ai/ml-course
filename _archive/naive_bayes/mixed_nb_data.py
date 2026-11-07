"""Dataset plumbing shared by the notebook, the data preparation script and the grader.

Three things live here, and nothing else:

- `normalize_frame` — splits a raw dataframe into a string block (categorical features) and a
  float block (continuous features), which is the only representation the rest of the problem
  works with.
- `hash_split` — a content-addressed train/test split. The side a row lands on is a function of
  the row's own values, so the split is reproducible across runs, machines and library versions,
  and duplicated rows always land together.
- `save_fixture` / `load_fixture` — the `.npz` container the private test data is stored in.

The module deliberately knows nothing about any particular dataset: the registry of datasets is
in `scripts/naive_bayes_mixed.py`, which students never see.
"""

from __future__ import annotations

import dataclasses
import hashlib
import json
import pathlib
from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from collections.abc import Iterable, Mapping, Sequence

    import pandas as pd
    from numpy.typing import NDArray

SPLIT_BUCKETS = 10_000
"""Number of hash buckets a row can fall into. Fixes the split's resolution at 0.01%."""

DEFAULT_SALT = "nb-mixed-v1"
"""Personalisation string for the row hash. Changing it reshuffles every split."""

FIELD_SEPARATOR = "\x1f"
"""ASCII unit separator, used to join a row's fields so no value can forge a boundary."""

REGIMES: tuple[str, ...] = ("categorical", "continuous", "mixed")
"""The three feature regimes every dataset is tested under."""


@dataclasses.dataclass(frozen=True)
class Fixture:
    """One prepared dataset: normalized features, labels and a frozen train/test mask."""

    name: str
    categorical_names: tuple[str, ...]
    continuous_names: tuple[str, ...]
    categorical_values: NDArray[np.str_]
    continuous_values: NDArray[np.float64]
    target: NDArray[np.str_]
    is_test: NDArray[np.bool_]
    meta: Mapping[str, object]

    @property
    def n_rows(self) -> int:
        """Number of rows kept after dropping incomplete ones."""
        return int(self.target.shape[0])

    def matrix(self, regime: str) -> NDArray[np.object_]:
        """Builds the feature matrix for one feature regime.

        Args:
            regime: `"categorical"`, `"continuous"` or `"mixed"`.

        Returns:
            An object matrix whose categorical columns hold strings and whose continuous columns
            hold floats, with the categorical columns first.
        """
        blocks = {
            "categorical": [self.categorical_values],
            "continuous": [self.continuous_values],
            "mixed": [self.categorical_values, self.continuous_values],
        }[regime]
        return np.concatenate([block.astype(object) for block in blocks], axis=1)

    def categorical_indices(self, regime: str) -> list[int]:
        """Returns the positions of the categorical columns in `matrix(regime)`."""
        if regime == "continuous":
            return []
        return list(range(len(self.categorical_names)))

    def feature_names(self, regime: str) -> list[str]:
        """Returns the column names of `matrix(regime)`, in the same order."""
        names = {
            "categorical": self.categorical_names,
            "continuous": self.continuous_names,
            "mixed": self.categorical_names + self.continuous_names,
        }[regime]
        return list(names)

    def split(
        self, regime: str
    ) -> tuple[NDArray[np.object_], NDArray[np.object_], NDArray[np.str_], NDArray[np.str_]]:
        """Returns `(X_train, X_test, y_train, y_test)` for one feature regime."""
        features = self.matrix(regime)
        train = ~self.is_test
        return (
            features[train],
            features[self.is_test],
            self.target[train],
            self.target[self.is_test],
        )


def row_token(values: Iterable[object]) -> str:
    """Renders one row as a canonical string.

    Equal values must render equally whatever their Python or NumPy type, or the same row would
    hash differently depending on how the dataframe was loaded. Floats go through a fixed-width
    scientific format for that reason, and are therefore compared to 10 significant digits.

    Args:
        values: The row's field values, in column order.

    Returns:
        The row's fields joined by the ASCII unit separator.
    """
    fields: list[str] = []
    for value in values:
        if isinstance(value, (bool, np.bool_)):
            fields.append("1" if value else "0")
        elif isinstance(value, (int, np.integer)):
            fields.append(str(int(value)))
        elif isinstance(value, (float, np.floating)):
            fields.append(f"{float(value):.10e}")
        else:
            fields.append(str(value))
    return FIELD_SEPARATOR.join(fields)


def row_bucket(token: str, salt: str = DEFAULT_SALT) -> int:
    """Hashes a row token into `[0, SPLIT_BUCKETS)`.

    BLAKE2b is used rather than `hash()`, which is salted per interpreter process and would make
    the split irreproducible, and rather than MD5, which some hardened builds refuse to provide.

    Args:
        token: Output of `row_token`.
        salt: Personalisation string, at most 16 bytes.

    Returns:
        The row's bucket index.
    """
    digest = hashlib.blake2b(
        token.encode("utf-8"), digest_size=8, person=salt.encode("utf-8")
    ).digest()
    return int.from_bytes(digest, "big") % SPLIT_BUCKETS


def hash_split(
    categorical_values: NDArray[np.str_],
    continuous_values: NDArray[np.float64],
    target: NDArray[np.str_],
    test_fraction: float = 0.25,
    salt: str = DEFAULT_SALT,
) -> NDArray[np.bool_]:
    """Assigns every row to the train or the test side by hashing the row itself.

    The label takes part in the hash, so the mask is a property of the complete record. Class
    balance is only approximately preserved — this is not a stratified split — but it is exactly
    reproducible, which is what the reference metrics need.

    Args:
        categorical_values: String block, shape `(n_rows, n_categorical)`.
        continuous_values: Float block, shape `(n_rows, n_continuous)`.
        target: Labels, shape `(n_rows,)`.
        test_fraction: Expected share of rows on the test side.
        salt: Personalisation string for the row hash.

    Returns:
        A boolean mask that is `True` for the test rows.
    """
    if not 0.0 < test_fraction < 1.0:
        raise ValueError(f"test_fraction must lie in (0, 1), got {test_fraction}")
    threshold = round(test_fraction * SPLIT_BUCKETS)
    tokens = (
        row_token([*categorical_values[row], *continuous_values[row], target[row]])
        for row in range(target.shape[0])
    )
    return np.array([row_bucket(token, salt) < threshold for token in tokens], dtype=bool)


def normalize_frame(
    frame: pd.DataFrame,
    categorical_names: Sequence[str],
    continuous_names: Sequence[str],
) -> tuple[NDArray[np.str_], NDArray[np.float64]]:
    """Splits a dataframe into the string block and the float block.

    Args:
        frame: Feature dataframe.
        categorical_names: Columns to render as strings.
        continuous_names: Columns to render as floats.

    Returns:
        The `(categorical_values, continuous_values)` pair.
    """
    categorical = frame[list(categorical_names)].astype(str).to_numpy(dtype=np.str_)
    continuous = frame[list(continuous_names)].to_numpy(dtype=np.float64)
    return categorical, continuous


def save_fixture(path: str | pathlib.Path, fixture: Fixture) -> None:
    """Writes a fixture to a compressed `.npz` file.

    Only arrays of fixed-width strings, floats and booleans are stored, so the file loads without
    `allow_pickle`.

    Args:
        path: Destination file.
        fixture: The fixture to store.
    """
    np.savez_compressed(
        pathlib.Path(path),
        name=np.array(fixture.name),
        categorical_names=np.array(fixture.categorical_names, dtype=np.str_),
        continuous_names=np.array(fixture.continuous_names, dtype=np.str_),
        categorical_values=fixture.categorical_values,
        continuous_values=fixture.continuous_values,
        target=fixture.target,
        is_test=fixture.is_test,
        meta=np.array(json.dumps(dict(fixture.meta), sort_keys=True)),
    )


def load_fixture(path: str | pathlib.Path) -> Fixture:
    """Reads a fixture written by `save_fixture`.

    Args:
        path: The `.npz` file to read.

    Returns:
        The stored fixture.
    """
    with np.load(pathlib.Path(path)) as archive:
        return Fixture(
            name=str(archive["name"]),
            categorical_names=tuple(str(name) for name in archive["categorical_names"]),
            continuous_names=tuple(str(name) for name in archive["continuous_names"]),
            categorical_values=archive["categorical_values"],
            continuous_values=archive["continuous_values"],
            target=archive["target"],
            is_test=archive["is_test"],
            meta=json.loads(str(archive["meta"])),
        )

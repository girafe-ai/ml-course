"""The measurement protocol shared by the reference run and the grader.

The tests compare a submission against numbers `scripts/naive_bayes_mixed.py build` produced
from the golden solution, so both sides have to measure the same things the same way. That is the
only reason this module exists: `evaluate` is called once with the reference classifier and once
with the student's, and nothing else decides what a metric or a stage timing means.

Timings are the **fastest** of several repeats. The minimum is the right summary for wall-clock
measurements — noise only ever adds time — and it keeps the grader's verdict stable on a machine
that is doing other work at the same time.
"""

from __future__ import annotations

import dataclasses
import math
import time
from typing import TYPE_CHECKING, TypeVar

import numpy as np
from sklearn.metrics import accuracy_score, f1_score, log_loss

if TYPE_CHECKING:
    from collections.abc import Callable, Mapping

    from numpy.typing import ArrayLike

STAGES: tuple[str, ...] = ("init", "fit", "predict")
"""The three stages whose wall-clock time is recorded."""

DEFAULT_REPEATS = 3
"""How many times each stage runs before the fastest run is kept."""

Result = TypeVar("Result")


@dataclasses.dataclass(frozen=True)
class Evaluation:
    """What one `(dataset, feature regime)` run produced.

    Attributes:
        accuracy: Share of correct predictions on the test side.
        macro_f1: Unweighted mean of the per-class F1 scores.
        log_loss: Mean negative log-likelihood of the test labels under `predict_proba`.
        runtime_seconds: Fastest observed wall-clock time per stage, keyed by `STAGES`.
        n_train: Rows on the train side.
        n_test: Rows on the test side.
        n_classes: Number of distinct labels seen while fitting.
    """

    accuracy: float
    macro_f1: float
    log_loss: float
    runtime_seconds: Mapping[str, float]
    n_train: int
    n_test: int
    n_classes: int

    def as_dict(self) -> dict[str, object]:
        """Returns the evaluation as JSON-serialisable plain data."""
        return {
            "accuracy": self.accuracy,
            "macro_f1": self.macro_f1,
            "log_loss": self.log_loss,
            "runtime_seconds": dict(self.runtime_seconds),
            "n_train": self.n_train,
            "n_test": self.n_test,
            "n_classes": self.n_classes,
        }


def measure(  # noqa: UP047 — PEP 695 syntax needs 3.12, and this module runs on the judge
    action: Callable[[], Result], repeats: int = DEFAULT_REPEATS
) -> tuple[float, Result]:
    """Times `action` and returns the fastest run together with its last result.

    Args:
        action: Niladic callable to time.
        repeats: Number of runs; must be at least one.

    Returns:
        The `(seconds, result)` pair.
    """
    if repeats < 1:
        raise ValueError(f"repeats must be at least 1, got {repeats}")
    best = math.inf
    result: Result | None = None
    for _ in range(repeats):
        start = time.perf_counter()
        result = action()
        best = min(best, time.perf_counter() - start)
    return best, result  # type: ignore[return-value]


def evaluate(
    build: Callable[[], object],
    X_train: ArrayLike,
    y_train: ArrayLike,
    X_test: ArrayLike,
    y_test: ArrayLike,
    repeats: int = DEFAULT_REPEATS,
) -> Evaluation:
    """Runs one classifier over one split and records its metrics and stage timings.

    Args:
        build: Builds an unfitted classifier. Called repeatedly, so it must return a fresh
            instance every time — that is what makes the `init` stage measurable.
        X_train: Training features.
        y_train: Training labels.
        X_test: Test features.
        y_test: Test labels.
        repeats: Number of timed runs per stage.

    Returns:
        The evaluation.
    """
    init_seconds, _ = measure(build, repeats)
    fit_seconds, model = measure(lambda: build().fit(X_train, y_train), repeats)
    predict_seconds, predicted = measure(lambda: model.predict(X_test), repeats)
    proba = np.asarray(model.predict_proba(X_test), dtype=np.float64)
    classes = np.asarray(model.classes_)
    return Evaluation(
        accuracy=float(accuracy_score(y_test, predicted)),
        macro_f1=float(f1_score(y_test, predicted, average="macro")),
        log_loss=float(log_loss(y_test, proba, labels=classes)),
        runtime_seconds={
            "init": init_seconds,
            "fit": fit_seconds,
            "predict": predict_seconds,
        },
        n_train=int(np.asarray(y_train).shape[0]),
        n_test=int(np.asarray(y_test).shape[0]),
        n_classes=int(classes.shape[0]),
    )


def probability_report(model: object, X: ArrayLike) -> dict[str, float]:
    """Summarises how well a fitted model's probability outputs agree with each other.

    Args:
        model: A fitted classifier with `predict`, `predict_proba` and `predict_log_proba`.
        X: Features to score.

    Returns:
        The largest deviation of the row sums from one, the largest gap between
        `log(predict_proba)` and `predict_log_proba`, and the share of rows where `predict`
        disagrees with the arg-max of `predict_proba`.
    """
    proba = np.asarray(model.predict_proba(X), dtype=np.float64)
    log_proba = np.asarray(model.predict_log_proba(X), dtype=np.float64)
    classes = np.asarray(model.classes_)
    with np.errstate(divide="ignore"):
        log_gap = np.abs(np.log(proba) - log_proba)
    return {
        "row_sum_deviation": float(np.abs(proba.sum(axis=1) - 1.0).max()),
        "log_gap": float(log_gap[np.isfinite(log_gap)].max(initial=0.0)),
        "argmax_disagreement": float(
            np.mean(classes[proba.argmax(axis=1)] != np.asarray(model.predict(X)))
        ),
    }

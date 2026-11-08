r"""Mixed-feature Naive Bayes — submission template.

Fill in the four places marked `YOUR CODE HERE` and submit **this file** to the contest. Do not
rename the module-level names: the grader imports `MixedNaiveBayes` and `GaussianDensity` from
your upload and calls nothing else.

The model is the textbook Naive Bayes factorisation with one likelihood per feature type. For a
record $x$ whose categorical features are $C$ and whose continuous features are $Q$,

$$\log p(y = c \mid x) = \log \pi_c
    + \sum_{j \in C} \log \hat p_{cj}(x_j)
    + \sum_{j \in Q} \log \hat f_{cj}(x_j) - \log Z(x),$$

with $Z(x)$ the evidence that normalises the posterior. The categorical factor is a
Lidstone-smoothed frequency table,

$$\hat p_{cj}(a) = \frac{N_{cja} + \alpha}{N_c + \alpha K_j},$$

over the $K_j$ categories seen while fitting, and a category first met at prediction time is
scored as a zero-count one, $\alpha / (N_c + \alpha K_j)$. The continuous factor is whatever
density estimator the caller passed, fitted separately for every class and every feature.

Everything that is not the model itself — column plumbing, the posterior normalisation, parameter
validation — is already written.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np
from scipy.special import logsumexp
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.utils.validation import check_is_fitted

if TYPE_CHECKING:
    from collections.abc import Sequence

    from numpy.typing import ArrayLike, NDArray


class GaussianDensity(BaseEstimator):
    """Univariate Gaussian density with `sklearn.neighbors.KernelDensity`'s interface.

    This is the default continuous likelihood. It implements the two methods `MixedNaiveBayes`
    calls — `fit(X)` and `score_samples(X)` — so any object honouring that contract,
    `KernelDensity` included, can replace it.

    Args:
        var_smoothing: Lower bound on the fitted variance, which keeps a feature that is constant
            within a class from producing an infinite log-density.
    """

    def __init__(self, var_smoothing: float = 1e-9) -> None:
        """Stores the hyper-parameters unchanged, as sklearn's estimator contract requires."""
        self.var_smoothing = var_smoothing

    def fit(self, X: ArrayLike, y: ArrayLike | None = None) -> GaussianDensity:
        """Fits the mean and the variance by maximum likelihood.

        Store them as `self.mean_` and `self.var_`, and clamp the variance from below with
        `self.var_smoothing` so a within-class constant feature stays finite.

        Args:
            X: Sample values, shape `(n_samples, 1)` or `(n_samples,)`.
            y: Ignored, present for interface compatibility.

        Returns:
            The fitted estimator.
        """
        values = np.asarray(X, dtype=np.float64).reshape(-1)
        if values.size == 0:
            raise ValueError("GaussianDensity needs at least one sample")
        # YOUR CODE HERE (1/4): set self.mean_ and self.var_, then return self
        raise NotImplementedError

    def score_samples(self, X: ArrayLike) -> NDArray[np.float64]:
        """Evaluates the log-density at the given points.

        Mind that this returns a **log**-density, like `KernelDensity.score_samples`, and that it
        is a density rather than a probability: values above zero are normal for a narrow peak.

        Args:
            X: Query points, shape `(n_samples, 1)` or `(n_samples,)`.

        Returns:
            Log-densities, shape `(n_samples,)`.
        """
        check_is_fitted(self, "var_")
        values = np.asarray(X, dtype=np.float64).reshape(-1)
        # YOUR CODE HERE (2/4): return the Gaussian log-density of `values`
        raise NotImplementedError


class MixedNaiveBayes(ClassifierMixin, BaseEstimator):
    """Naive Bayes classifier for datasets that mix categorical and continuous features.

    Args:
        categorical_features: Column indices or column names to treat as categorical. `None`
            infers them: a column whose every value converts to `float` is continuous, any other
            column is categorical. Integer-coded categories therefore have to be named explicitly.
        density_estimator: Unfitted density estimator for the continuous features, with
            `KernelDensity`'s `fit` / `score_samples` interface. Cloned once per class and
            feature, so one instance is enough. `None` means `GaussianDensity()`.
        alpha: Lidstone smoothing constant for the categorical features. `0.0` disables smoothing.
        priors: Class priors in `classes_` order. `None` uses the training frequencies.

    Attributes:
        classes_: Sorted class labels.
        class_log_prior_: Log priors, shape `(n_classes,)`.
        n_features_in_: Number of features seen while fitting.
        feature_names_in_: Column names, present only when `fit` saw a dataframe.
        categorical_features_: Resolved categorical column indices, sorted.
        continuous_features_: Resolved continuous column indices, sorted.
        categories_: Per categorical feature, the sorted categories seen while fitting.
        feature_log_prob_: Per categorical feature, the `(n_classes, n_categories)` log table.
        unseen_log_prob_: Log-probability of an unseen category, shape
            `(n_classes, n_categorical)`.
        densities_: Per continuous feature, one fitted density estimator per class.
    """

    def __init__(
        self,
        categorical_features: Sequence[int] | Sequence[str] | None = None,
        density_estimator: object | None = None,
        alpha: float = 1.0,
        priors: Sequence[float] | None = None,
    ) -> None:
        """Stores the hyper-parameters unchanged, as sklearn's estimator contract requires."""
        self.categorical_features = categorical_features
        self.density_estimator = density_estimator
        self.alpha = alpha
        self.priors = priors

    def fit(self, X: ArrayLike, y: ArrayLike) -> MixedNaiveBayes:
        """Fits the priors, the categorical tables and the per-class continuous densities.

        Set, in this order: `classes_` and `class_log_prior_`, then for the categorical columns
        `categories_`, `feature_log_prob_` and `unseen_log_prob_`, then `densities_` for the
        continuous ones. Clone `density_estimator` with `sklearn.base.clone` before fitting it, so
        the object the caller handed you is left untouched.

        Args:
            X: Feature matrix, shape `(n_samples, n_features)`. A dataframe, an object array or a
                numeric array.
            y: Labels, shape `(n_samples,)`.

        Returns:
            The fitted classifier.
        """
        matrix, names = _as_matrix(X)
        self.n_features_in_ = matrix.shape[1]
        if names is not None:
            self.feature_names_in_ = names
        categorical, continuous = _resolve_columns(matrix, names, self.categorical_features)
        self.categorical_features_ = categorical
        self.continuous_features_ = continuous

        labels = np.asarray(y)
        if labels.shape[0] != matrix.shape[0]:
            raise ValueError(f"X has {matrix.shape[0]} samples but y has {labels.shape[0]}")
        categorical_values = _categorical_block(matrix, categorical)
        continuous_values = _continuous_block(matrix, continuous)
        # YOUR CODE HERE (3/4): fit the priors, the categorical tables and the
        # densities, then return self. `self._class_priors(class_counts)` already
        # handles the `priors` parameter for you.
        raise NotImplementedError

    def _class_priors(self, class_counts: NDArray[np.float64]) -> NDArray[np.float64]:
        """Returns the class priors, either empirical or the ones the caller supplied.

        Args:
            class_counts: Number of training rows per class, in `classes_` order.

        Returns:
            The priors, shape `(n_classes,)`.
        """
        if self.priors is None:
            return class_counts / class_counts.sum()
        priors = np.asarray(self.priors, dtype=np.float64)
        if priors.shape != class_counts.shape:
            raise ValueError(
                f"priors has length {priors.shape[0]}, expected {class_counts.shape[0]}"
            )
        if np.any(priors <= 0.0) or not np.isclose(priors.sum(), 1.0):
            raise ValueError("priors must be positive and sum to 1")
        return priors

    def _joint_log_likelihood(self, X: ArrayLike) -> NDArray[np.float64]:
        r"""Computes the unnormalised log joint $\log p(x, y = c)$ for every class.

        Start from `class_log_prior_` broadcast over the rows, add one term per categorical
        feature and one per continuous feature. A value absent from `categories_[j]` takes
        `unseen_log_prob_[:, j]` instead of a table lookup.

        Args:
            X: Feature matrix, shape `(n_samples, n_features)`.

        Returns:
            Log joint likelihoods, shape `(n_samples, n_classes)`.
        """
        check_is_fitted(self, "classes_")
        matrix, _ = _as_matrix(X)
        if matrix.shape[1] != self.n_features_in_:
            raise ValueError(f"X has {matrix.shape[1]} features, expected {self.n_features_in_}")
        categorical_values = _categorical_block(matrix, self.categorical_features_)
        continuous_values = _continuous_block(matrix, self.continuous_features_)
        # YOUR CODE HERE (4/4): return the (n_samples, n_classes) log joint likelihood
        raise NotImplementedError

    def predict_log_proba(self, X: ArrayLike) -> NDArray[np.float64]:
        """Returns the log posterior over classes, shape `(n_samples, n_classes)`."""
        joint = self._joint_log_likelihood(X)
        return joint - logsumexp(joint, axis=1, keepdims=True)

    def predict_proba(self, X: ArrayLike) -> NDArray[np.float64]:
        """Returns the posterior over classes, shape `(n_samples, n_classes)`."""
        return np.exp(self.predict_log_proba(X))

    def predict(self, X: ArrayLike) -> NDArray:
        """Returns the most probable class for every row, shape `(n_samples,)`."""
        joint = self._joint_log_likelihood(X)
        return self.classes_[np.argmax(joint, axis=1)]


def _as_matrix(X: ArrayLike) -> tuple[NDArray, NDArray[np.str_] | None]:
    """Normalises any accepted container into a 2-D array plus its column names.

    Args:
        X: Dataframe, object array, numeric array or nested sequence.

    Returns:
        The `(matrix, names)` pair; `names` is `None` unless `X` carried column labels.
    """
    names = None
    if hasattr(X, "columns") and hasattr(X, "to_numpy"):
        names = np.asarray([str(name) for name in X.columns], dtype=np.str_)
        matrix = X.to_numpy()
    else:
        matrix = np.asarray(X)
    if matrix.ndim != 2:
        raise ValueError(f"X must be 2-dimensional, got {matrix.ndim} dimensions")
    return matrix, names


def _is_continuous(column: NDArray) -> bool:
    """Reports whether every value of a column converts to `float`."""
    try:
        np.asarray(column, dtype=np.float64)
    except (TypeError, ValueError):
        return False
    return True


def _resolve_columns(
    matrix: NDArray,
    names: NDArray[np.str_] | None,
    categorical_features: Sequence[int] | Sequence[str] | None,
) -> tuple[NDArray[np.intp], NDArray[np.intp]]:
    """Turns the `categorical_features` parameter into two index arrays.

    Args:
        matrix: The feature matrix, used for inference and for range checks.
        names: Column names, when the caller passed a dataframe.
        categorical_features: Indices, names, or `None` to infer.

    Returns:
        The `(categorical_indices, continuous_indices)` pair, both sorted.
    """
    n_features = matrix.shape[1]
    if categorical_features is None:
        selected = [index for index in range(n_features) if not _is_continuous(matrix[:, index])]
    else:
        requested = list(categorical_features)
        if any(isinstance(item, str) for item in requested):
            if names is None:
                raise ValueError("categorical_features given as names, but X has no column names")
            positions = {name: index for index, name in enumerate(names)}
            missing = [item for item in requested if item not in positions]
            if missing:
                raise ValueError(f"unknown categorical feature names: {missing}")
            selected = [positions[item] for item in requested]
        else:
            selected = [int(item) for item in requested]
            out_of_range = [index for index in selected if not 0 <= index < n_features]
            if out_of_range:
                raise ValueError(f"categorical feature indices out of range: {out_of_range}")
    categorical = np.array(sorted(set(selected)), dtype=np.intp)
    continuous = np.array(
        [index for index in range(n_features) if index not in set(selected)],
        dtype=np.intp,
    )
    return categorical, continuous


def _categorical_block(matrix: NDArray, indices: NDArray[np.intp]) -> NDArray[np.str_]:
    """Extracts the categorical columns as strings, so values compare by their text form."""
    return matrix[:, indices].astype(np.str_)


def _continuous_block(matrix: NDArray, indices: NDArray[np.intp]) -> NDArray[np.float64]:
    """Extracts the continuous columns as floats."""
    return matrix[:, indices].astype(np.float64)

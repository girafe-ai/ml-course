# Week 3: Regularisation + Model Validation

Lecture slides: [`ml-basic_lect03_regularisation_validation.pdf`](ml-basic_lect03_regularisation_validation.pdf)

The lecture continues linear regression. It starts with overfitting and underfitting on polynomials of growing
degree: the training error falls to zero while the error on new data turns back up. Then regularisation: ridge
(L2) and lasso (L1), why lasso sets weights exactly to zero, elastic net, why features are standardised first,
and the penalty as a prior on the weights. The second half is about choosing hyperparameters: validation data,
k-fold cross-validation, the one standard error rule, pipelines, and how to split data that comes in groups or
in time.

Interactive pages, the self-check quiz, the classroom quiz and the game: links in the course chat.

## Seminar notebook

| Notebook | Practice | Solved |
| --- | --- | --- |
| Regularisation and validation: overfitting, ridge, lasso, cross-validation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/girafe-ai/ml-course/blob/26f_ymls_uz/week0_03_regularisation_and_validation/week0_03_01_regularisation_and_validation.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/girafe-ai/ml-course/blob/26f_ymls_uz/week0_03_regularisation_and_validation/week0_03_01_regularisation_and_validation__completed.ipynb) |

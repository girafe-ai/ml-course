# Week 6: Naive Bayes + Probabilistic Classifiers

Lecture slides: [`ml-basic_lect06_naive_bayes.pdf`](ml-basic_lect06_naive_bayes.pdf)

Logistic regression models the probability of a class directly. This lecture takes the other route: model how
each class produces its data, then turn it around with Bayes' rule. It covers the prior, the likelihood and the
posterior on a single word, the naive independence assumption, and naive Bayes by hand with Laplace smoothing.
Multinomial naive Bayes classifies listing texts and turns out to be a linear classifier whose weights come from
counting. Gaussian naive Bayes handles numeric features, next to LDA and QDA. The second half shows what the
assumptions cost: the labels and the ranking mostly hold up while the probabilities suffer. At the end kNN,
logistic regression and naive Bayes are compared on one dataset with stratified cross-validation.

Interactive pages, the self-check quiz, the classroom quiz and the game: links in the course chat.

## Seminar notebook

| Notebook | Practice | Solved |
| --- | --- | --- |
| Naive Bayes: Bayes' rule, naive Bayes from scratch, calibration, three classifiers compared | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/girafe-ai/ml-course/blob/26f_ymls_uz/week0_06_naive_bayes/week0_06_01_naive_bayes.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/girafe-ai/ml-course/blob/26f_ymls_uz/week0_06_naive_bayes/week0_06_01_naive_bayes__completed.ipynb) |

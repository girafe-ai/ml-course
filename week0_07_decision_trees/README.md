# Week 7: Decision Trees

Lecture slides: [`ml-basic_lect07_decision_trees.pdf`](ml-basic_lect07_decision_trees.pdf)

Every classifier so far draws one smooth boundary or measures distances. A decision tree asks questions one at
a time and answers in a leaf. This lecture covers how to read a tree, how it cuts the plane into rectangles, and
how it is grown greedily: try every feature and every threshold, keep the question that leaves the purest
groups. Gini impurity is computed by hand on ten listings, with entropy as the other common measure. Trees for
regression predict the mean of a leaf and draw a staircase. The second half is about depth and overfitting, the
settings that hold a tree back, what trees are good and bad at, and why one tree is unstable while many trees
voting together are steadier.

Interactive pages, the self-check quiz, the classroom quiz and the game: links in the course chat.

## Seminar notebook

| Notebook | Practice | Solved |
| --- | --- | --- |
| Decision trees: Gini and the best split by hand, depth and cross-validation, a regression tree, trees against logistic regression, unstable trees | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/girafe-ai/ml-course/blob/26f_ymls_uz/week0_07_decision_trees/week0_07_01_decision_trees.ipynb) | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/girafe-ai/ml-course/blob/26f_ymls_uz/week0_07_decision_trees/week0_07_01_decision_trees__completed.ipynb) |

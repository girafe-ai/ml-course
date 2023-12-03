# Экзаменационная программа:

0. Задача обучения c учителем. Регрессия, Классификация.
1. Как измерить качество в классификации: точность, сбалансированная точность, прецизионность, полнота, f1-скор, ROC-AUC, расширения для многоклассовой классификации.
2. Как измерить качество в регрессии: MSE, MAE, R2.
3. Оценка максимального правдоподобия, как она связана с регрессией и классификацией
4. Наивный байесовский классификатор, как он работает
5. Классификатор ближайших соседей, как он работает
6. Линейная регрессия. Формулировка задачи для случая функции потерь MSE. Аналитическое решение. Теорема Гаусса-Маркова. Градиентный подход в линейной регрессии.
7. Регуляризация в линейных моделях: L1 \(\Leftrightarrow\) L2, их свойства. Вероятностная интерпретация.
8. Логистическая регрессия. Эквивалентность подходов MLE и минимизации логистических потерь.
9. Многоклассовая классификация. Один-против-одного, один-против-всех, их свойства.
10. Метод опорных векторов. Задача оптимизации для SVM. Трюк с ядром. Свойства ядра.
11. Анализ главных компонент. Связь с SVD. Теорема Эккарта-Янга. Как применять PCA на практике.
12. Этапы обучения, валидации и тестирования модели. Проблема переобучения, способы её обнаружения.
13. Стратегии валидации. Кросс-валидация. Утечки данных.
14. Компромисс смещения-дисперсии.
15. Процедура построения дерева решений.
16. Критерии информации. Критерии энтропии, неопределенности Джини.
17. Ансамблевые методы. Бутстрап. Бэггинг.
18. Случайный лес, метод случайных подпространств.
19. Бустинг и градиентный бустинг. Основная идея, производная градиента.
20. Матричное исчисление и производные матриц. Как получить производную матричного/скалярного произведения, напр.: $ \mathbf{a}^T \mathbf{x}$, $\mathbf{Ax}$.
21. Обратное распространение ошибки.
22. Концепция нейронной сети. Полносвязный слой (FC).
23. Логистическая регрессия как простая нейронная сеть.
24. Функции потерь для НС в задаче классификации.
25. Функции активации, их влияние на сеть, вычислительная сложность. Функции Softmax и LogSoftmax, численная стабильность.
26. Методы оптимизации в глубоком обучении. Градиентный спуск, SGD, его улучшения: Momentum, RMSProp, Adam.
27. Регуляризация в глубоком обучении: Dropout, Batch Normalization. Различия в стадиях обучения и оценки.
28. Классическая рекурсивная НС. Обратное распространение через RNN. Проблема затухающего градиента.
29. LSTM/GRU, концепция памяти, идеи вентилей (gates).
30. Операция свертки. Свёрточный слой, обратное распространение через него. Гиперпараметры свёрток. Сравнение 1x1 свёрток и полносвязных слоёв. Пулинг: max/average.
31. Основные идеи AlexNet, VGG, Inception (GoogLeNet), архитектуры ResNet.
32. Геометрические методы в машинном обучении. Задача кластеризации. IsoMap, LLE, DBSCAN, k-средние, t-SNE.

## Теоретический минимум
1. Задача обучения с учителем
2. Задача обучения без учителя. Предоставьте по крайней мере две проблемы-примера.
3. Что такое i.i.d. данные?
4. Как работает наивный байесовский классификатор? Почему он наивный?
5. Модель линейной регрессии для минимизации проблемы MSE. Запишите формулу и производную функции потерь по весам.
6. Запишите шаг градиентного спуска. Как его адаптировать для больших наборов данных?
7. Что такое правдоподобие? Где обычно используется Максимальное Правдоподобие (MLE)?
8. Что такое кросс-валидация? Как количество фолдов влияет на валидацию?
9. Что такое переобучение и недообучение? Как их обнаружить?
10. В чем разница между параметрами и гиперпараметрами? Приведите пример для линейных моделей/деревьев решений.
11. Что такое регуляризация? В чем разница между L1 и L2 регуляризацией в линейных моделях? Это единственный способ ограничить решение?
12. Регуляризует ли L2 регуляризация член смещения (w_0 или b)? Почему?
13. Почему хорошая идея нормализовать данные перед применением линейной модели?
14. Сформулируйте задачу линейной классификации. Что такое маржа?
15. Что такое точность и полнота? Как их использовать для оценки качества модели?
16. Предположим, что набор данных для бинарной классификации несбалансирован, так что 95% данных относятся к первому классу. Как скорректировать меры качества классификации для работы с такими данными? Почему?
17. Что такое ROC AUC? Как построить ROC-кривую?
18. Функция потерь логистической регрессии. Как она связана с оценкой максимального правдоподобия?
19. Основная идея машины опорных векторов. Функционал оптимизации для линейно разделимого случая.
20. Опишите жадный оптимизационный алгоритм для дерева решений.
21. Почему неконстреинированное дерево решений может достичь нулевой ошибки на обучающем наборе с уникальными объектами?
22. Как присвоить метку класса объекту в листе дерева в классификации?
23. Как присвоить метку класса объекту в листе дерева в регрессии? Зависит ли это от информационного критерия?
24. Что такое бэггинг?
25. Что такое Случайный лес? Чем он отличается от Бэггинга над деревьями решений?
26. Как обучаются базовые алгоритмы в градиентном бустинге?
27. Как работает обратное распространение ошибок в нейронных сетях? Что будет вектор-векторная производная?
28. Как работает свёрточный слой? Что такое свёрточная операция?
29. Почему полносвязные (плотные) сети не лучший выбор для работы с изображениями? Почему лучше работают свёрточные нейронные сети (CNN)?
30. Как работает базовая RNN (Vanilla RNN)?
31. Как работает Dropout?
32. Как Dropout и пакетная нормализация меняют свое поведение на этапе вывода?
33. В чем состоит формулировка задачи для Анализа Главных Компонентов?


# Exam program:
0. Machine Learning problem statement. Regression, Classification, examples.
1. How to measure quality in classification: accuracy, balanced accuracy, precision, recall, f1-score, ROC-AUC, multiclass extensions.
2. How to measure quality in regression: MSE, MAE, R2.
3. Maximum likelihood estimation, how is it related to regression and classification
4. Naive bayesian classifier, how does it work
5. K-nearest neighbours classifier, how does it work
6. Linear regression. Problem statement for the MSE loss function case. Analytical solution. Gauss-Markov theorem. Gradient approach in linear regression.
7. Regularization in linear models: L1 \(\Leftrightarrow\) L2, their properties. Probabilistic interpretation.
8. Logistic regression. Equivalence of MLE approach and logistic loss minimization.
9. Multiclass classification. One-vs-one, one-vs-all, their properties.
10. Support vector machine. Optimization problem for SVM. Kernel trick. Kernel properties.
11. Principal component analysis. Relations to SVD. Eckart-Young theorem. How to apply PCA in practice.
12. Train, validation and test stages of model development. Overfitting problem, ways to detect it.
13. Validation strategies. Cross validation. Data leaks.
14. Bias-variance tradeoff.
15. Decision tree construction procedure.
16. Information criteria. Entropy criteria, Giny impurity.
17. Ensembling methods. Bootstrap. Bagging.
18. Random Forest, Random subspace method.
19. Boosting and gradient boosting. Main idea, gradient derivation.
20. Matrix calculus and matrix derivatives. How to get the derivative of matrix/dot product, e.g.: \( \mathbf{a}^T \mathbf{x}, \mathbf{Ax} \).
21. Backpropagation, chain rule.
22. Neural network concept. Fully-Connected layer (FC).
23. Logistic regression as simple NN.
    XOR problem.
24. Losses for NNs: logistic loss, cross-entropy.
25. Activation functions, their impact on the network, computational complexity. Softmax and LogSoftmax activations, numerical stability.
26. Optimization methods in Deep Learning. Gradient descent, SGD, it upgrades: Momentum, RMSProp, Adam.
27. Regularization in Deep Learning: Dropout, Batch Normalization. Differences in training and evaluation stages.
28. Vanilla Recursive NN cell. Backpropagation through RNN.
    Vanishing gradient problem. Potential solutions.
29. LSTM/GRU, memory concept, gates ideas.
30. Matrix convolution. Convolutional layer, backpropagation through it. Hyperparameters of Convs. 1x1 convolutions, comparison to FC layers. Max/Average Pooling.
31. Main ideas of AlexNet, VGG, Inception (GoogLeNet), ResNet architectures.
32. Geometrical methods in ML. Clustering problem. IsoMap, LLE, DBSCAN, k-means, t-SNE.

## Theoretical minimum
1. Supervised learning problem statement
2. Unsupervised learning problem statement. Provide at least two example problems.
3. What is i.i.d. data?
4. How does a Naive Bayesian Classifier work? Why is it naive?
5. Linear regression model for MSE minimization problem. Write down the formula and the derivative of the loss function w.r.t. weights.
6. Write down a gradient descent step. How to adjust it for huge datasets?
7. What is the likelihood? Where is Maximum Likelihood Estimation (MLE) usually used?
8. What is cross-validation? How does the number of folds affect the validation?
9. What is overfitting and underfitting? How to detect them?
10. What is the difference between parameters and hyperparameters? Provide an example for linear models/decision trees.
11. What is a regularization? What is the difference between L1 and L2 regularization in linear models? Is it the only way to constrain the solution?
12. Does L2 regularization regularize the bias term (w_0 or b)? Why?
13. Why is it a good idea to normalize data before applying a linear model?
14. Provide a linear classification problem statement. What is a margin?
15. What are precision and recall? How to use them to measure the model quality?
16. Assume the dataset for binary classification is imbalanced, so 95% of data belong to the first class. How to adjust the classification quality measures, to work with such data? Why?
17. What is ROC AUC? How to build the ROC curve?
18. Logistic loss function. How is it related to Maximum likelihood estimation?
19. Support Vector Machine main idea. The optimization functional for linearly separable case.
20. Describe the greedy optimization algorithm for the decision tree.
21. Why can an unconstrained decision tree achieve zero error on the training set with unique objects?
22. How to assign a class label for the object in the tree leaf in classification?
23. How to assign a class label for the object in the tree leaf in regression? Does it depend on the information criterion?
24. What is bagging?
25. What is Random Forest? How does it differ from Bagging over decision trees?
26. How are base algorithms being trained in gradient boosting?
27. How does backpropagation work in neural networks? What will be vector by vector derivative?
28. How does the Convolutional layer work? What is the convolution operation?
29. Why fully connected (dense) networks are not the best choice to work with image data? Why do CNNs perform better?
30. How does basic RNN (Vanilla RNN) work?
31. How does dropout work?
32. How do dropout and batch normalization change their behaviour on the inference stage?
33. What is the problem statement for the Principal Component Analysis?

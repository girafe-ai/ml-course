from math import isnan

from scipy.stats import pearsonr


# Получить список фильмов, оцененных обоими
def similar_films(critics_dict, person1, person2):
    # создаем пустой список фильмов
    sim_film = []

    # для всех фильмов у person1...
    for film in critics_dict[person1]:
        # если такой фильм оценивался person 2...
        if film in critics_dict[person2]:
            # добавляем этот фильм в список sim_film
            sim_film.append(film)

    return sim_film


# Подсчета сходства двух критиков на основе расстояния Евклида
def sim_distance(critics_dict, person1, person2):
    # используем написанную функцию для получения фильмов, оцененных обоими критиками
    sim_films = similar_films(critics_dict, person1, person2)

    # если нет ни одной общей оценки, то есть длина sim_film равна 0 - вернуть 0
    if len(sim_films) == 0:
        return 0

    # для каждого фильма из sim_film посчитаем евклидово расстояние и просуммируем все полученные значения
    sum_of_euclead_dist = 0

    for film in sim_films:
        sum_of_euclead_dist += pow(critics_dict[person1][film] - critics_dict[person2][film], 2)

    # считаем похожесть
    return 1 / (1 + sum_of_euclead_dist)


# Возвращает коэффициент корреляции Пирсона между person1 и person2
def sim_pearson(critics_dict, person1, person2):
    # получить список фильмов, оцененных обоими критиками
    sim_films = similar_films(critics_dict, person1, person2)

    # если нет ни одной общей оценки, вернуть 0
    if len(sim_films) < 2:
        return 0

    # получим оценки критиков для фильмов из пересечения
    scores1 = []
    scores2 = []
    for film in sim_films:
        scores1.append(critics_dict[person1][film])
        scores2.append(critics_dict[person2][film])

    # посчитаем коэффициент корреляции
    # берем [0] от результата, так как функция pearsonr() возвращает еще значение p-value
    print("&&&&&&&&&&")
    print(critics_dict)
    print(scores1, scores2)
    r = pearsonr(scores1, scores2)[0]

    # если вдруг было деление на ноль и функция вернула nan, то присваиваем ноль
    if isnan(r):
        r = 0
    return r


# возвращает топ-n наиболее похожих на person человек из critics_dict
def top_matches(critics_dict, person, n=5, similarity=sim_pearson):
    # инициализируем лист оценок похожести
    scores = []

    # для каждого человека в словаре критиков
    for other in critics_dict:

        # если этот человек не тот, для которого мы подбираем соответствия
        if other != person:
            # добавить в scores похожесть, вычисленную с помощью функции, записанной в similarity, и имя человека
            scores.append((similarity(critics_dict, person, other), other))

    # отсортировать список по убыванию оценок
    scores.sort(reverse=True)  # аргумент reverse=True отвечает за убывающий порядок

    # возвращаем первые n человек
    return scores[0:n]


# Получить рекомендации для заданного человека, пользуясь взвешенным средним
# оценок, данных всеми остальными пользователями
def get_recommendations(prefs, person, similarity=sim_pearson):
    # инициализируем словари
    totals = {}
    sim_sums = {}

    # для каждого пользователя
    for other in prefs:
        # сравнивать person с person не нужно
        if other == person:
            continue
        # считаем похожесть
        sim = similarity(prefs, person, other)

        # игнорировать нулевые и отрицательные значения похожести
        if sim <= 0:
            continue

        # для каждого фильма в оцененных other
        for item in prefs[other]:
            # оценивать только фильмы, которые я еще не смотрел
            if item not in prefs[person] or prefs[person][item] == 0:

                # коэффициент подобия * Оценка
                totals.setdefault(item, 0)
                totals[item] = totals[item] + prefs[other][item] * sim

                # cумма коэффициентов подобия
                sim_sums.setdefault(item, 0)
                sim_sums[item] = sim_sums[item] + sim
    # создать нормированный список
    rankings = [(total / sim_sums[item], item) for item, total in totals.items()]

    # вернуть отсортированный список
    rankings.sort(reverse=True)
    return rankings


# обращает матрицу предпочтений, чтобы строки соответствовали образцам
def transform_prefs(critics_dict):
    # инициилизируем новый словарь с фильмами и их оценками
    result = {}

    # для каждого критика в словаре
    for person in critics_dict:
        # для каждого оцененного им фильма
        for item in critics_dict[person]:
            # добавляем такой объект в словарь
            result.setdefault(item, {})
            # меняеи местами человека и предмет
            result[item][person] = critics_dict[person][item]
    return result


# Создать словарь, содержащий для каждого образца те образцы, которые больше всего похожи на него.
def calculate_similar_items(prefs, n=10):
    result = {}
    # обращаем матрицу предпочтений, чтобы строки соответствовали образцам
    item_prefs = transform_prefs(prefs)

    c = 0
    for item in item_prefs:
        # проверка состояния для больших наборов данных
        c = c + 1
        if c % 100 == 0:
            print("%d / %d" % (c, len(item_prefs)))

        # найти образцы, максимально похожие на данный
        scores = top_matches(item_prefs, item, n=n, similarity=sim_distance)
        result[item] = scores
    return result


# Получить рекомендации для заданного человека, пользуясь взвешенным средним
# оценок, похожих на оцененные пользователем объектов
def get_recommended_items(prefs, item_match, user):
    # инициализируем словари
    user_ratings = prefs[user]
    scores = {}
    total_sim = {}

    # цикл по образцам, оцененным данным пользователем (хранятся в user_ratings)
    for (item, rating) in user_ratings.items():
        # цикл по образцам, похожим на данный (хранятся в словаре item_match)
        for (similarity, item2) in item_match[item]:
            # пропускаем объект, если пользователь уже оценивал данный образец
            if item2 in user_ratings:
                continue
            # взвешенная суммы оценок, умноженных на коэффициент подобия
            scores.setdefault(item2, 0)
            scores[item2] = scores[item2] + similarity * rating
            # сумма всех коэффициентов подобия
            total_sim.setdefault(item2, 0)
            total_sim[item2] = total_sim[item2] + similarity
            if total_sim[item2] == 0:
                total_sim[item2] = 0.0000001  # чтобы избежать деления на ноль
    # делим каждую итоговую оценку на взвешенную сумму, чтобы вычислить среднее
    rankings = [(score / total_sim[item], item) for item, score in scores.items()]

    # возвращает список rankings, отсортированный по убыванию
    rankings.sort(reverse=True)
    return rankings


# Функция для загрузки данных MovieLens
def load_movie_lens():
    # получить названия фильмов
    movies = {}
    for line in open("u.item", encoding="ISO-8859-1"):
        (id, title) = line.split("|")[0:2]
        movies[id] = title

    # загрузить данные
    prefs = {}
    for line in open("u.data"):
        (user, movieid, rating, ts) = line.split("\t")
        prefs.setdefault(user, {})
        prefs[user][movies[movieid]] = float(rating)

    return prefs

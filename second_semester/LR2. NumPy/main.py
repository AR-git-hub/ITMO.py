import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ============================================================
# 1. СОЗДАНИЕ И ОБРАБОТКА МАССИВОВ
# ============================================================

def create_vector(n: int) -> np.ndarray:
    """
    Создает массив от 0 до n-1. 

    Args:
        n (int): длина вектора.

    Returns:
        numpy.ndarray: массив чисел [0, 1, ..., n-1].

    Example:
        >>> create_vector(5)
        array([0, 1, 2, 3, 4])
    """
    return np.arange(n)


def create_matrix(shape: list[int]) -> np.ndarray:
    """
    Создает матрицу заданной формы со случайными числами [0,1).

    Args:
        shape (list[int]): размеры матрицы, например [3,4].

    Returns:
        numpy.ndarray: матрица случайных чисел.

    Example:
        >>> np.random.seed(42)
        >>> create_matrix([2,2])
        array([[0.37454012, 0.95071431],
               [0.73199394, 0.59865848]])
    """
    return np.random.rand(*shape)


def reshape_vector(vec_og: np.ndarray, shapes: list[int] | tuple[int]) -> np.ndarray:
    """
    Изменяет форму массива.

    Args:
        vec_og (numpy.ndarray): исходный массив.
        shapes (list[int] | tuple[int]): новая форма.

    Returns:
        numpy.ndarray: массив новой формы.

    Example:
        >>> v = np.arange(10)
        >>> reshape_vector(v, (2,5))
        array([[0, 1, 2, 3, 4],
               [5, 6, 7, 8, 9]])
    """
    return np.reshape(vec_og, tuple(shapes))


def transpose_matrix(mat: np.ndarray) -> np.ndarray:
    """
    Транспонирует матрицу.

    Args:
        mat (numpy.ndarray): входная матрица.

    Returns:
        numpy.ndarray: транспонированная матрица.

    Example:
        >>> m = np.array([[1,2],[3,4]])
        >>> transpose_matrix(m)
        array([[1, 3],
               [2, 4]])
    """
    return mat.T


# ============================================================
# 2. ВЕКТОРНЫЕ ОПЕРАЦИИ
# ============================================================

def vector_add(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Поэлементное сложение двух массивов.

    Args:
        a (numpy.ndarray): первый массив.
        b (numpy.ndarray): второй массив.

    Returns:
        numpy.ndarray: результат сложения.

    Example:
        >>> vector_add(np.array([1,2]), np.array([3,4]))
        array([4, 6])
    """
    return a + b


def scalar_multiply(vec: np.ndarray, scalar: int | float) -> np.ndarray:
    """
    Умножение вектора на скаляр.

    Args:
        vec (numpy.ndarray): исходный вектор.
        scalar (int | float): число.

    Returns:
        numpy.ndarray: результат умножения.

    Example:
        >>> scalar_multiply(np.array([1,2,3]), 2)
        array([2, 4, 6])
    """
    return vec * scalar


def elementwise_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Поэлементное умножение двух массивов.

    Args:
        a (numpy.ndarray): первый массив.
        b (numpy.ndarray): второй массив.

    Returns:
        numpy.ndarray: результат умножения.

    Example:
        >>> elementwise_multiply(np.array([1,2]), np.array([3,4]))
        array([3, 8])
    """
    return a * b


def dot_product(a: np.ndarray, b: np.ndarray) -> float:
    """
    Скалярное произведение двух векторов.

    Args:
        a (numpy.ndarray): первый вектор.
        b (numpy.ndarray): второй вектор.

    Returns:
        float: скалярное произведение.

    Example:
        >>> dot_product(np.array([1,2]), np.array([3,4]))
        11
    """
    return np.dot(a, b)


# ============================================================
# 3. МАТРИЧНЫЕ ОПЕРАЦИИ
# ============================================================

def matrix_multiply(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Умножение матриц.

    Args:
        a (numpy.ndarray): первая матрица.
        b (numpy.ndarray): вторая матрица.

    Returns:
        numpy.ndarray: произведение матриц.

    Example:
        >>> A = np.array([[1,2],[3,4]])
        >>> B = np.array([[2,0],[1,2]])
        >>> matrix_multiply(A, B)
        array([[ 4,  4],
               [10,  8]])
    """
    return a @ b


def matrix_determinant(a: np.ndarray) -> float:
    """
    Вычисляет определитель квадратной матрицы.

    Args:
        a (numpy.ndarray): квадратная матрица.

    Returns:
        float: определитель.

    Example:
        >>> matrix_determinant(np.array([[1,2],[3,4]]))
        -2.0
    """
    return np.linalg.det(a)


def matrix_inverse(a: np.ndarray) -> np.ndarray:
    """
    Вычисляет обратную матрицу.

    Args:
        a (numpy.ndarray): квадратная матрица.

    Returns:
        numpy.ndarray: обратная матрица.

    Example:
        >>> A = np.array([[1,2],[3,4]])
        >>> matrix_inverse(A)
        array([[-2. ,  1. ],
               [ 1.5, -0.5]])
    """
    return np.linalg.inv(a)


def solve_linear_system(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """
    Решает систему линейных уравнений Ax = b.

    Args:
        a (numpy.ndarray): матрица коэффициентов.
        b (numpy.ndarray): вектор свободных членов.

    Returns:
        numpy.ndarray: решение x.

    Example:
        >>> A = np.array([[2,1],[1,3]])
        >>> b = np.array([5,10])
        >>> solve_linear_system(A, b)
        array([1., 3.])
    """
    return np.linalg.solve(a, b)


# ============================================================
# 4. СТАТИСТИЧЕСКИЙ АНАЛИЗ
# ============================================================

def load_dataset(path: str) -> np.ndarray:
    """
    Загружает CSV‑файл и возвращает данные в виде numpy‑массива.

    Args:
        path (str): путь к CSV‑файлу.

    Returns:
        numpy.ndarray: загруженные данные.

    Example:
        >>> # создадим временный файл для примера
        >>> with open('test.csv', 'w') as f:
        ...     f.write('a,b\\n1,2\\n3,4')
        >>> load_dataset('test.csv')
        array([[1, 2],
               [3, 4]])
        >>> import os; os.remove('test.csv')
    """
    return pd.read_csv(path).to_numpy()


def statistical_analysis(data: np.ndarray) -> dict:
    """
    Вычисляет основные статистические характеристики данных.

    Args:
        data (numpy.ndarray): одномерный массив данных.

    Returns:
        dict: словарь с показателями.

    Example:
        >>> data = np.array([10,20,30])
        >>> statistical_analysis(data)   # doctest: +SKIP
        {'mean': 20.0, 'median': 20.0, 'std': 8.164..., 'min': 10, 'max': 30, '25th': 15.0, '75th': 25.0}
    """
    return {
        'mean': np.mean(data),
        'median': np.median(data),
        'std': np.std(data),
        'min': np.min(data),
        'max': np.max(data),
        '25th': np.percentile(data, 25),
        '75th': np.percentile(data, 75)
    }


def normalize_data(data: np.ndarray) -> np.ndarray:
    """
    Min‑Max нормализация данных в диапазон [0,1].

    Args:
        data (numpy.ndarray): входные данные.

    Returns:
        numpy.ndarray: нормализованные данные.

    Example:
        >>> normalize_data(np.array([0,5,10]))
        array([0. , 0.5, 1. ])
    """
    minn = np.min(data)
    maxx = np.max(data)
    return (data - minn) / (maxx - minn)


# ============================================================
# 5. ВИЗУАЛИЗАЦИЯ
# ============================================================

def plot_histogram(data: np.ndarray) -> None:
    """
    Строит гистограмму распределения данных и сохраняет в файл.

    Args:
        data (numpy.ndarray): данные для гистограммы.

    Example:
        >>> data = np.array([78,85,92,70,88,95,60,73,84,90])
        >>> plot_histogram(data)
        # файл 'plots/histogram.png' создан
    """
    plt.figure()
    plt.hist(data, bins=10)
    plt.title('Распределение оценок по математике')
    plt.xlabel('Оценка')
    plt.ylabel('Частота')
    plt.savefig("plots/histogram.png")
    plt.close()


def plot_heatmap(matrix: np.ndarray) -> None:
    """
    Строит тепловую карту корреляционной матрицы и сохраняет в файл.

    Args:
        matrix (numpy.ndarray): матрица корреляции.

    Example:
        >>> corr = np.array([[1.0, 0.5], [0.5, 1.0]])
        >>> plot_heatmap(corr)
        # файл 'plots/heatmap.png' создан
    """
    plt.figure()
    sns.heatmap(matrix,
                annot=True,
                cmap='coolwarm',
                square=True,
                fmt='.2f')
    plt.title('Корреляция между предметами')
    plt.savefig('plots/heatmap.png')
    plt.close()


def plot_line(x: np.ndarray, y: np.ndarray) -> None:
    """
    Строит линейный график зависимости y от x и сохраняет в файл.

    Args:
        x (numpy.ndarray): координаты по оси X.
        y (numpy.ndarray): координаты по оси Y.

    Example:
        >>> x = np.array([1,2,3,4,5])
        >>> y = np.array([78,85,92,88,95])
        >>> plot_line(x, y)
        # файл 'plots/line_plot.png' создан
    """
    plt.figure()
    plt.plot(x, y, marker='o', linestyle='-', color='blue')
    plt.title('Оценки студентов по математике')
    plt.xlabel('Номер студента')
    plt.ylabel('Оценка')
    plt.grid(True)
    plt.savefig('plots/line_plot.png')
    plt.close()
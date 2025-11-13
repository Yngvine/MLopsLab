"""
Data preprocessing functions for cleaning and transforming datasets.
"""
import math
import re
from typing import Any
import random


def clean_values(data: list) -> list:
    """
    Cleans the input list by removing missing values like None, '' and nan.

    Parameters
    ----------
    data : list
        The input list containing various data types.

    Returns
    -------
    list
        A new list with cleaned values.

    Examples
    --------
    >>> clean_values([1, 2, None, '', 3, float('nan')])
    [1, 2, 3]
    """
    cleaned_data = []
    for item in data:
        if item is None or item == "":
            continue
        if (isinstance(item, float) or isinstance(item, int)) and math.isnan(item):
            continue
        cleaned_data.append(item)

    return cleaned_data


def fill_values(data: list, fill_value: Any = 0) -> list:
    """
    Fills missing values in the input list with a specified fill value, by default 0.

    Parameters
    ----------
    data : list
        The input list containing various data types.
    fill_value : Any, default 0
        The value to replace missing values with. Default is 0.

    Returns
    -------
    list
        A new list with missing values filled.

    Examples
    --------
    >>> fill_values([1, 2, None, '', 3, float('nan')], fill_value=-1)
    [1, 2, -1, -1, 3, -1]
    """
    filled_data = []
    for item in data:
        if item is None or item == "":
            filled_data.append(fill_value)
        elif (isinstance(item, float) or isinstance(item, int)) and math.isnan(item):
            filled_data.append(fill_value)
        else:
            filled_data.append(item)
        
    return filled_data


def remove_duplicates(data: list) -> list:
    """
    Removes duplicate values from the input list.
    Parameters
    ----------
    data : list
        The input list containing various data types.

    Returns
    -------
    list
        A new list with duplicates removed.

    Examples
    --------
    >>> remove_duplicates([1, 2, 2, 3, 1, 4])
    [1, 2, 3, 4]
    """
    return list(set(data))


def minmax_normalize(data: list, min_val: float = 0.0, max_val: float = 1.0) -> list:
    """
    Normalizes the input list using Min-Max normalization.

    Parameters
    ----------
    data : list
        The input list containing numerical values.
    min_val : float, default 0.0
        The minimum value for normalization. Default is 0.0.
    max_val : float, default 1.0
        The maximum value for normalization. Default is 1.0.

    Returns
    -------
    list
        A new list with normalized values.

    Examples
    --------
    >>> minmax_normalize([1, 2, 3, 4, 5])
    [0.0, 0.25, 0.5, 0.75, 1.0]
    """
    if not data:
        return data

    min_val = min(data)
    max_val = max(data)
    if min_val == max_val:
        return [0.0 for _ in data]  # Avoid division by zero if all values are the same

    normalized_data = [(item - min_val) / (max_val - min_val) for item in data]
    return normalized_data


def z_score_standardize(data: list) -> list:
    """
    Standardizes the input list using Z-score standardization.

    Parameters
    ----------
    data : list
        The input list containing numerical values.

    Returns
    -------
    list
        A new list with standardized values.

    Examples
    --------
    >>> z_score_standardize([1, 2, 3, 4, 5])
    [-1.2649110640673518, -0.6324555320336759, 0.0, 0.6324555320336759, 1.2649110640673518]
    """
    if not data:
        return data

    mean_val = sum(data) / len(data)
    variance = sum((item - mean_val) ** 2 for item in data) / len(data)
    std_dev = variance**0.5
    if std_dev == 0:
        return [0.0 for _ in data]  # Avoid division by zero if all values are the same

    standardized_data = [(item - mean_val) / std_dev for item in data]
    return standardized_data


def clip_values(data: list, min_threshold: float, max_threshold: float) -> list:
    """
    Clips the values in the input list to be within the specified min and max thresholds.

    Parameters
    ----------
    data : list
        The input list containing numerical values.
    min_threshold : float
        The minimum threshold value.
    max_threshold : float
        The maximum threshold value.

    Returns
    -------
    list
        A new list with clipped values.

    Examples
    --------
    >>> clip_values([1, 5, 10, 15, 20], min_threshold=5, max_threshold=15)
    [5, 5, 10, 15, 15]
    """
    clipped_data = [max(min(item, max_threshold), min_threshold) for item in data]
    return clipped_data


def lst_to_ints(data: list[str]) -> list[int]:
    """
    Converts all elements in the input list to integers if possible. 
    Non-convertible elements are excluded.

    Parameters
    ----------
    data : list[str]
        The input list containing strings.

    Returns
    -------
    list[int]
        A new list with all elements converted to integers.

    Examples
    --------
    >>> lst_to_ints(['1', '2', 'three', '4', '5five'])
    [1, 2, 4]
    """
    return [int(item) for item in data if item.isdigit()]


def log_transform(data: list) -> list:
    """
    Applies logarithmic transformation to the input list.

    Parameters
    ----------
    data : list[float]
        The input list containing numerical values.

    Returns
    -------
    list[float]
        A new list with log-transformed values. Negative or zero values are excluded.

    Examples
    --------
    >>> log_transform([1, 10, 100, 1000])
    [0.0, 2.302585092994046, 4.605170185988092, 6.907755278982137]
    """
    transformed_data = [math.log(item) for item in data if item > 0]
    return transformed_data


def special_tokenization(text: str) -> list:
    """
    Tokenizes the input text into words, selecting only alphanumeric 
    characters and lowercasing words.

    Parameters
    ----------
    text : str
        The input text string.

    Returns
    -------
    list[str]
        A list of tokenized words.

    Examples
    --------
    >>> special_tokenization("Hello, World! This is a test.")
    ['hello', 'world', 'this', 'is', 'a', 'test']
    """

    tokens = re.findall(r"\b\w+\b", text.lower())
    return tokens


def clean_text(text: str) -> str:
    """
    Cleans the input text by removing special characters and extra spaces.

    Parameters
    ----------
    text : str
        The input text string.

    Returns
    -------
    str
        The cleaned text string.

    Examples
    --------
    >>> clean_text("Hello,   World! This is a test.")
    'Hello World This is a test'
    """
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)  # Remove special characters
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text


def clean_stop_words(text: str, stopwords: set) -> str:
    """
    Removes stopwords from the input text.

    Parameters
    ----------
    text : str
        The input text string.
    stopwords : set
        A set of stopwords to be removed.

    Returns
    -------
    str
        The text string with stopwords removed.

    Examples
    --------
    >>> stopwords = {'is', 'a', 'the', 'this'}
    >>> clean_stop_words("This is a test of the stopword removal.", stopwords)
    'test of stopword removal.'
    """
    words = text.split()
    cleaned_text = " ".join([word for word in words if word.lower() not in stopwords])
    return cleaned_text


def lst_flatten(nested_list: list[list[Any]]) -> list[Any]:
    """
    Flattens a nested list into a single list.

    Parameters
    ----------
    nested_list : list[list[Any]]
        The input nested list.

    Returns
    -------
    list[Any]
        A flattened list.

    Examples
    --------
    >>> lst_flatten([[1, 2], [3, 4], [5]])
    [1, 2, 3, 4, 5]
    """
    flattened_list = [item for sublist in nested_list for item in sublist]
    return flattened_list


def lst_shuffle(data: list, seed: int | None = None) -> list:
    """
    Shuffles the elements in the input list randomly.

    Parameters
    ----------
    data : list
        The input list.
    seed : int | None, default None
        The random seed for reproducibility.

    Returns
    -------
    list
        A new list with shuffled elements.

    Examples
    --------
    >>> lst_shuffle([1, 2, 3, 4, 5], seed=42)
    [3, 5, 2, 1, 4]
    """
    if seed is not None:
        random.seed(seed)
    shuffled_data = data[:]
    random.shuffle(shuffled_data)
    return shuffled_data

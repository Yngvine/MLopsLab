"""
Test suite for data preprocessing functions.
"""
import pytest

from src import (
    clean_values,
    fill_values,
    minmax_normalize,
    z_score_standardize,
    clip_values,
    lst_to_ints,
    log_transform,
    special_tokenization,
    clean_text,
    clean_stop_words,
    lst_shuffle,
    lst_flatten,
    remove_duplicates,
)

@pytest.fixture
def sample_number_list():
    return [1, 2, 3, 4, 5]

@pytest.mark.parametrize("input_data, expected", [
    ([1, 2, None, 4, '', 5, float('nan'), 6], [1, 2, 4, 5, 6]),
    (['a', '', 'b', None, 'c'], ['a', 'b', 'c']),
])
def test_clean_values(input_data, expected):
    values = clean_values(input_data)
    print(values)
    assert values == expected
    

@pytest.mark.parametrize("input_data, fill_value, expected", [
    ([1, 2, None, 4, '', 5, float('nan'), 6], -1, [1, 2, -1, 4, -1, 5, -1, 6]),
    (['a', '', 'b', None, 'c'], 'x', ['a', 'x', 'b', 'x', 'c']),
])
def test_fill_values_custom(input_data, fill_value, expected):
    assert fill_values(input_data, fill_value) == expected

@pytest.mark.parametrize("input_data, expected", [
    ([1, 2, None, 4, '', 5, float('nan'), 6], [1, 2, 0, 4, 0, 5, 0, 6]),
    (['a', '', 'b', None, 'c'], ['a', 0, 'b', 0, 'c']),
])
def test_fill_values_default(input_data, expected):
    assert fill_values(input_data) == expected


def test_minmax_normalize(sample_number_list):
    input_data = sample_number_list
    expected = [0.0, 0.25, 0.5, 0.75, 1.0]
    assert minmax_normalize(input_data) == expected

def test_z_score_standardize(sample_number_list):
    input_data = sample_number_list
    mean = sum(input_data) / len(input_data)
    std_dev = (sum((x - mean) ** 2 for x in input_data) / len(input_data)) ** 0.5
    expected = [(x - mean) / std_dev for x in input_data]
    assert z_score_standardize(input_data) == expected

def test_clip_values(sample_number_list):
    input_data = sample_number_list
    min_threshold = 2
    max_threshold = 4
    expected = [2, 2, 3, 4, 4]
    assert clip_values(input_data, min_threshold, max_threshold) == expected

def test_lst_to_ints():
    input_data = ['1', '2', '3']
    expected = [1, 2, 3]
    assert lst_to_ints(input_data) == expected

def test_log_transform():
    input_data = [1, 10, 100]
    expected = [0.0, 2.302585092994046, 4.605170185988092]
    assert log_transform(input_data) == expected

def test_special_tokenization():
    input_data = "Hello, world! This is a test."
    expected = ['hello', 'world', 'this', 'is', 'a', 'test']
    assert special_tokenization(input_data) == expected

def test_clean_text():
    input_data = " Hello, World! "
    expected = "Hello World"
    assert clean_text(input_data) == expected

def test_clean_stop_words():
    input_data = "Hello, world! This is a test."
    stop_words = set(['this', 'is', 'a', ',', '!'])
    expected = 'Hello, world! test.'
    assert clean_stop_words(input_data, stop_words) == expected

def test_lst_shuffle():
    input_data = [1, 2, 3, 4, 5]
    shuffled = lst_shuffle(input_data)
    assert len(shuffled) == len(input_data)
    assert shuffled != input_data
    assert sorted(shuffled) == sorted(input_data)

def test_lst_flatten():
    input_data = [[1, 2], [3, 4], [5]]
    expected = [1, 2, 3, 4, 5]
    assert lst_flatten(input_data) == expected

def test_remove_duplicates():
    input_data = [1, 2, 2, 3, 1, 4]
    expected = [1, 2, 3, 4]
    assert sorted(remove_duplicates(input_data)) == sorted(expected)

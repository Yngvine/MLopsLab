"""
Test suite for command-line interface (CLI) functions of the data preprocessing module.
"""
from click.testing import CliRunner
import pytest

from src.cli import cli

@pytest.fixture
def runner():
    return CliRunner()


@pytest.mark.parametrize("command, input_data, expected_output", [
    ("cleaning clean", [1, 2, None, 4, '', 5, float('nan'), 6], "Cleaned Data: ['1', '2', 'None', '4', '5', 'nan', '6']\n"),
    ("cleaning clean", ['a', '', 'b', None, 'c'], "Cleaned Data: ['a', 'b', 'None', 'c']\n"),
])
def test_cli_clean_command(runner, command, input_data, expected_output):
    data_as_strings = [str(item) for item in input_data]
    result = runner.invoke(cli, command.split() + data_as_strings)
    assert result.exit_code == 0
    assert result.output == expected_output


@pytest.mark.parametrize("command, input_data, options, expected_output", [
    ("cleaning fill", [1, 2, None, 4, '', 5, float('nan'), 6], ["--fill_value", "-1"], "Filled Data: ['1', '2', 'None', '4', -1, '5', 'nan', '6']\n"),
    ("cleaning fill", ['a', '', 'b', None, 'c'], ["--fill_value", "x"], "Filled Data: ['a', 'x', 'b', 'None', 'c']\n"),
])
def test_cli_fill_command_custom(runner, command, input_data, options, expected_output):
    data_as_strings = [str(item) for item in input_data]
    result = runner.invoke(cli, command.split() + options + data_as_strings)
    assert result.exit_code == 0
    assert result.output == expected_output
    
@pytest.mark.parametrize("command, input_data, expected_output", [
    ("cleaning fill", [1, 2, None, 4, '', 5, float('nan'), 6], "Filled Data: ['1', '2', 'None', '4', 0, '5', 'nan', '6']\n"),
    ("cleaning fill", ['a', '', 'b', None, 'c'], "Filled Data: ['a', 0, 'b', 'None', 'c']\n"),
])
def test_cli_fill_command_default(runner, command, input_data, expected_output):
    data_as_strings = [str(item) for item in input_data]
    result = runner.invoke(cli, command.split() + data_as_strings)
    assert result.exit_code == 0
    assert result.output == expected_output


def test_cli_minmax_normalize_command(runner):
    input_data = [1, 2, 3, 4, 5]
    data_as_strings = [str(item) for item in input_data]
    result = runner.invoke(cli, ["numeric", "normalize"] + data_as_strings)
    assert result.exit_code == 0
    output_list = eval(result.output.split(": ")[1].strip())
    expected = [0.0, 0.25, 0.5, 0.75, 1.0]
    assert all(abs(a - b) < 1e-6 for a, b in zip(output_list, expected))

def test_cli_z_score_standardize_command(runner):
    input_data = [1, 2, 3, 4, 5]
    data_as_strings = [str(item) for item in input_data]
    result = runner.invoke(cli, ["numeric", "standardize"] + data_as_strings)
    assert result.exit_code == 0
    output_list = eval(result.output.split(": ")[1].strip())
    mean = sum(input_data) / len(input_data)
    std_dev = (sum((x - mean) ** 2 for x in input_data) / len(input_data)) ** 0.5
    expected = [(x - mean) / std_dev for x in input_data]
    assert all(abs(a - b) < 1e-6 for a, b in zip(output_list, expected))

def test_cli_clip_values_command(runner):
    input_data = [1, 2, 3, 4, 5]
    data_as_strings = [str(item) for item in input_data]
    result = runner.invoke(cli, ["numeric", "clip"] + data_as_strings + ["--min_threshold", "2", "--max_threshold", "4"])
    assert result.exit_code == 0
    output_list = eval(result.output.split(": ")[1].strip())
    expected = [2, 2, 3, 4, 4]
    assert output_list == expected

def test_cli_lst_to_ints_command(runner):
    input_data = ['1', '2', '3']
    result = runner.invoke(cli, ["numeric", "to-int"] + input_data)
    assert result.exit_code == 0
    output_list = eval(result.output.split(": ")[1].strip())
    expected = [1, 2, 3]
    assert output_list == expected

def test_cli_log_transform_command(runner):
    input_data = ['1', '10', '100']
    result = runner.invoke(cli, ["numeric", "log-scale"] + input_data)
    assert result.exit_code == 0
    output_list = eval(result.output.split(": ")[1].strip())
    import math
    expected = [math.log(1), math.log(10), math.log(100)]
    assert all(abs(a - b) < 1e-6 for a, b in zip(output_list, expected))

def test_cli_special_tokenization_command(runner):
    input_data = ["Hello, world! This is a test."]
    result = runner.invoke(cli, ["text", "tokenize"] + input_data)
    assert result.exit_code == 0
    output_list = eval(result.output.split(": ")[1].strip())
    expected = ['hello', 'world', 'this', 'is', 'a', 'test']
    assert output_list == expected

def test_cli_clean_text_command(runner):
    input_data = ["  Hello!!! This is a TEST...  "]
    result = runner.invoke(cli, ["text", "clean-punctuation"] + input_data)
    assert result.exit_code == 0
    output_text = result.output.split(": ")[1].strip()
    expected = "Hello This is a TEST"
    assert output_text == expected

def test_cli_clean_stop_words_command(runner):
    input_data = ["This is a sample sentence with some stop words"]
    stop_words = "is,a,with,some"
    result = runner.invoke(cli, ["text", "clean-stopwords", "--stopwords", stop_words] + input_data)
    assert result.exit_code == 0
    output_text = result.output.split(": ")[1].strip()
    expected = "This sample sentence stop words"
    assert output_text == expected

def test_cli_lst_shuffle_command(runner):
    input_data = ['1', '2', '3', '4', '5']
    result = runner.invoke(cli, ["struct", "shuffle"] + input_data)
    assert result.exit_code == 0
    output_list = eval(result.output.split(": ")[1].strip())
    assert len(output_list) == len(input_data)
    assert output_list != input_data  # Ensure the list is shuffled
    assert sorted(output_list) == sorted(input_data)  # Ensure all elements are present

def test_cli_lst_flatten_command(runner):
    input_data = ['[1, 2]', '[3, 4]', '[5]']
    result = runner.invoke(cli, ["struct", "flatten"] + input_data)
    assert result.exit_code == 0
    output_list = eval(result.output.split(": ")[1].strip())
    expected = [1, 2, 3, 4, 5]
    assert output_list == expected

def test_cli_remove_duplicates_command(runner):
    input_data = [1, 2, 2, 3, 1, 4]
    data_as_strings = [str(item) for item in input_data]
    result = runner.invoke(cli, ["struct", "deduplicate"] + data_as_strings)
    assert result.exit_code == 0
    output_list = eval(result.output.split(": ")[1].strip())
    assert sorted(output_list) == sorted(['1', '2', '3', '4'])

def test_cli_invalid_command(runner):
    result = runner.invoke(cli, ["nonexistent", "command"])
    assert result.exit_code != 0
    assert "No such command" in result.output
    
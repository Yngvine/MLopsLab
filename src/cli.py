"""
CLI application for data preprocessing tasks.
Wraps functions from preprocessing.py using Click.
"""
import ast
import click

from .preprocessing import (
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



@click.group()
def cli():
    """A simple CLI application."""


@cli.group()
def cleaning():
    """Data cleaning operations."""


@cleaning.command()
@click.argument("data", nargs=-1)
def clean(data):
    """Cleans the input data by removing None, empty strings, and NaN values."""
    data_list = list(data)
    cleaned_data = clean_values(data_list)
    click.echo(f"Cleaned Data: {cleaned_data}")


@cleaning.command()
@click.argument("data", nargs=-1)
@click.option("--fill_value", default=0, help="Value to fill missing entries with.")
def fill(data, fill_value):
    """Fills missing values in the input data with a specified fill value."""
    data_list = list(data)
    filled_data = fill_values(data_list, fill_value)
    click.echo(f"Filled Data: {filled_data}")


@cli.group()
def numeric():
    """Numeric data operations."""


@numeric.command()
@click.argument("data", nargs=-1)
@click.option("--min_value", default=0, help="Minimum value for normalization.")
@click.option("--max_value", default=1, help="Maximum value for normalization.")
def normalize(data, min_value, max_value):
    """Normalizes the input data to a specified range."""
    data_list = list(data)
    normalized_data = minmax_normalize(data_list, min_value, max_value)
    click.echo(f"Normalized Data: {normalized_data}")


@numeric.command()
@click.argument("data", nargs=-1)
def standardize(data):
    """Standardizes the input data to have a mean of 0 and standard deviation of 1."""
    data_list = list(data)
    standardized_data = z_score_standardize(data_list)
    click.echo(f"Standardized Data: {standardized_data}")


@numeric.command()
@click.argument("data", nargs=-1)
@click.option("--min_threshold", default=0, help="Lower threshold for clipping.")
@click.option("--max_threshold", default=1, help="Upper threshold for clipping.")
def clip(data, min_threshold, max_threshold):
    """Clips the input data to a specified range."""
    data_list = list(data)
    clipped_data = clip_values(data_list, min_threshold, max_threshold)
    click.echo(f"Clipped Data: {clipped_data}")


@numeric.command()
@click.argument("data", nargs=-1)
def to_int(data):
    """Converts the input data to integers."""
    data_list = list(data)
    int_data = lst_to_ints(data_list)
    click.echo(f"Integer Data: {int_data}")


@numeric.command()
@click.argument("data", nargs=-1)
def log_scale(data):
    """Applies logarithmic scaling to the input data."""
    data_list = list(data)
    log_scaled_data = log_transform(data_list)
    click.echo(f"Log Scaled Data: {log_scaled_data}")


@cli.group()
def text():
    """Text data operations."""


@text.command()
@click.argument("data", nargs=-1)
def tokenize(data):
    """Tokenizes the input text data."""
    tokenized_data = special_tokenization(data)
    click.echo(f"Tokenized Data: {tokenized_data}")


@text.command()
@click.argument("data", nargs=-1)
def clean_punctuation(data):
    """Cleans punctuation from the input text data."""
    cleaned_data = clean_text(data)
    click.echo(f"Cleaned Text Data: {cleaned_data}")


@text.command()
@click.argument("data", nargs=-1)
@click.option(
    "--stopwords", default="", help="Comma-separated list of stopwords to remove."
)
def clean_stopwords(data, stopwords):
    """Cleans stopwords from the input text data."""
    stopwords_list = set(stopwords.split(",")) if stopwords else set()
    cleaned_data = clean_stop_words(data, stopwords_list)
    click.echo(f"Cleaned Text Data: {cleaned_data}")


@cli.group()
def struct():
    """Structure data operations."""


@struct.command()
@click.argument("data", nargs=-1)
@click.option("--seed", default=None, type=int, help="Random seed for shuffling.")
def shuffle(data, seed):
    """Shuffles the input structured data."""
    data_list = list(data)
    shuffled_data = lst_shuffle(data_list, seed)
    click.echo(f"Shuffled Data: {shuffled_data}")


@struct.command()
@click.argument("data", nargs=-1)
def flatten(data):
    """Flattens the input nested structured data."""
    # Assuming input is a string representation of nested lists
    nested_list = [ast.literal_eval(item) for item in data]
    flattened_data = lst_flatten(nested_list)
    click.echo(f"Flattened Data: {flattened_data}")


@struct.command()
@click.argument("data", nargs=-1)
def deduplicate(data):
    """Deduplicates the input structured data."""
    data_list = list(data)
    deduplicated_data = remove_duplicates(data_list)
    click.echo(f"Deduplicated Data: {deduplicated_data}")

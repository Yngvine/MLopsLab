#import "conf.typ": conf
#show: conf
#align(center)[
  #v(2cm)
  #text(size: 24pt, weight: 700)[Lab 0: Fundamentals of Continuous Integration]
  #v(6pt)
  #text(size: 14pt)[Master's in Machine Learning 2025]
  #v(1.2cm)
  #text(size: 12pt)[
    Author: Igor Vons

    Date: November 14, 2025
  ]

]

#pagebreak()

= Test Implementation
The strategy followed to implement the tests involved creating a suite of unit tests using the `pytest` framework. Each test in tests/test_logic.py targets a specific function from the `preprocessing` module. Most are simple input-output tests, ensuring that given a specific input, the function produces the expected output. 

Likewise, the CLI commands were tested using `click`'s `CliRunner`, which simulates command-line invocations and captures their output for verification. For each test present in tests/test_logic.py there is a corresponding test in tests/test_cli.py that verifies the CLI command's behavior. 

Some of the outputs of the cli are expected to differ form the bare logic function outputs due to formatting, as in command-line outputs are strings, while logic function outputs can be lists or other data structures. The `assert` statements in the tests take this into account.

= Test outputs
The tests were executed using the `uv run python -m pytest -v` command in the terminal. All tests passed successfully, indicating that both the logic functions and CLI commands are functioning as intended. Below we can see the output of the test execution:

#figure(
  image("img/test_out.png"),  caption: "Output of test execution showing all tests passing successfully."

)

= Test coverage
To check the test coverage, the `pytest-cov` plugin was used. The command `uv run python -m pytest -v --cov=src` gives us some extra info on top of the test results:
#figure(
  image("img/cov_out.png"),  caption: "Output of test coverage analysis showing 100% coverage across all modules."
)
We can see although most of the preprocessing module is covered, we are still missing a few (5 out of 71). This shopuld be addressed in future iterations to ensure complete test coverage.

= Linter & Formatter 
The codebase was linted and formatted using `black` for formatting and `pylint` for linting. The commands used were `uv run python -m pylint src/*.py` and `uv run black src/*.py`. Both tools reported no issues, indicating that the code adheres to the specified style guidelines and is free of common coding errors.

#figure(
  image("img/lint_out.png"),  caption: "Output of pylint, displaying the last iterations until no more issues were found."
)

#figure(
  image("img/black_out.png", width: 50%),  caption: "Output of black, showing that linter reported no formatting issues after running."
)


This repository contains two things:
- Solutions to some [Project Euler](https://projecteuler.net/) problems.
- A CLI tool for managing these solutions and the library code shared between problems.

The latter is probably of more interest, because there's many many solutions to the first few Project Euler problems floating around the internet.

# Setup

If you want to use this for your own solutions, you can clone this repo and wipe my solution state:
- Clone the repository however you prefer
- Install requirements: `pip install -r requirements.txt`
- Delete existing code: `rm lib/* problems/* resources/*`
- Clear answer file: `rm answers.bin; touch answers.bin`

This repository has type annotations; either [mypy](http://mypy-lang.org/) or [Pyre](https://pyre-check.org/docs/getting-started/) should work. Personally I use the latter.

# Commands

To use this tool, run `main.py` with one of the following commands. (You can always pass `--help` for more details on a particular command.)

- `create <n>`: Create a new file `problems/<n>.py` for problem #n.
  - It fetches the problem description from the website and (poorly) formats it as a doc comment.
- `run <n>`: Run the code in `problems/<n>.py`, which should solve problem #n.
  - The answer is printed to the user, and compared against the saved answer (if any).
  - User is prompted to save the answer.
- `check <n>`: Runs the code in `problems/<n>.py` and compares it to the saved answer.
  - If run without `n`, checks all problems.
- `time <n>`: Runs the problem code several times and reports the average time taken.
- `overview`: Shows an overview of which problems have been completed or not.
- `answers`: Contains subcommands for manipulating the answer save file.
  - `show`: Shows the entire contents of the answer file.
  - `delete <n>`: Deletes the specific entry from the answer file.

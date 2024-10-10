This repository contains two things:
- A CLI tool for managing solutions to [Project Euler](https://projecteuler.net/) problems.
- Solutions to the first 100 problems, and also some shared math library code.

The former is probably of more interest, because there's many many solutions to the first 100 Project Euler problems floating around the internet.

# Setup

If you want to use this for your own solutions, you can clone this repo and wipe my solution state:
- Clone the repository however you prefer
- Install requirements: `pip install -r requirements.txt`
- Delete existing code: `rm lib/* problems/*`
  - You can keep `resources/`
- Clear answer file: `rm answers.bin; touch answers.bin`

This repository has type annotations; either [mypy](http://mypy-lang.org/) or [Pyre](https://pyre-check.org/docs/getting-started/) should work. Personally I use the latter.

# Commands

To use this tool, run `main.py` with one of the following commands.

> [!NOTE]
> Most of these commands also take arguments of the form `a-b`, indicating problems _a_ to _b_, inclusive, and the special value `all`, which has slightly different meanings for different commands.

Lastly, you can always pass `--help` for more details on a particular command.

- `create <n>`: Create a new file `problems/<n>.py` for problem #n.
  - Fetches the 'minimal' problem page from the Project Euler website, formats it into plaintext (poorly), and puts it into the template as a doc comment.
  - Cannot take `'all'` as argument.
- `run <n>`: Run the solution code for problem #n
  - The answer is printed to the user, and compared against the saved answer (if any).
  - User is prompted to save the answer.
- `check <n>`: Runs the solution code for problem #n and compares it to the saved answer.
  - If run without `n`, checks all problems.
- `time <n>`: Runs the problem code several times and reports the average time taken.
  - Can only take a single integer as its argument.
- `overview`: Shows an overview of which problems have been completed or not.
- `answers`: Contains subcommands for manipulating the answer save file.
  - `show <n>`: Shows the saved entries from the answer file.
  - `delete <n>`: Deletes the specific entries from the answer file.

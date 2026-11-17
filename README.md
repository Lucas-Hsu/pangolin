# Pangolin

A small PyQt6 desktop app that builds passwords from a word list.

## Start on macOS

Requires **macOS 14 or newer** with this Qt dependency version, an internet
connection for the first setup, and either `uv` or Python 3.10+.
Python 3.12 is the default; Python 3.15 is no longer required.

After extracting the ZIP, open Terminal in `pangolin-main` and run:

```bash
uv run pangolin
```

Or double-click **Start-Pangolin.command**. This launcher changes to the correct
folder, uses `uv` when available, or creates a local `.venv` and installs the
project with an existing Python installation. It does not install Python or uv
globally. If the launcher loses its executable permission during extraction:

```bash
bash ./Start-Pangolin.command
```

If you do not have uv, a manual setup works too:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --only-binary=PyQt6,PyQt6-Qt6,PyQt6-sip -e .
.venv/bin/python main.py
```

`python3` must be Python 3.10 or newer; substitute `python3.12` if needed.
Dependency installation uses prebuilt Qt wheels. You do not need to compile Qt
or install Homebrew Qt or `qmake`. On an unsupported OS/Python combination,
installation stops instead of attempting a large Qt source build.

## Use

- Choose a minimum length and the character types to include, then Generate.
- Copy Password copies the displayed result to the system clipboard.
- Word List lets you add, edit, or delete words. Enter also adds a word.
- Whole words are retained, so a password can be longer than the requested minimum.
- Word lists are kept for the current session only. Generated passwords are not
  saved by the app; copying puts them on the system clipboard.

The five starting words are examples. Add a much larger, varied word list for
real use; length alone does not measure a word-based password's strength.
Random choices use Python's `secrets` module.

## Project layout

| File | Purpose |
| --- | --- |
| `main.py` | Source-folder launcher; opens the same GUI as `pangolin` |
| `Start-Pangolin.command` | macOS setup and launch helper |
| `pyproject.toml` | Python requirements, dependencies, build backend, entry point |
| `src/pangolin/__main__.py` | Enables `python -m pangolin` after installation |
| `src/pangolin/app.py` | Main window and GUI connections |
| `src/pangolin/generator.py` | Password generation; no Qt dependencies |
| `src/pangolin/mainpage.py` | Generator page |
| `src/pangolin/wordlist.py` | Word list page |
| `examples/original_prototype.py` | Original root script, preserved unchanged |
| `tests/` | Generator and headless Qt integration tests |

The original root script mixed a standalone password prototype with unfinished
Fernet encryption code. It failed at import because its key was invalid, and
`cryptography` was undeclared. The GUI did not call that generator: its button
printed the selected settings instead. The running app now uses the separate
generator module. The archived prototype still contains its original errors
and is not an app entry point; encryption is not part of this app's setup.

## Develop and verify

```bash
uv run python -m unittest discover -s tests -v
uv build
```

The Qt tests use the offscreen platform and exercise generation, navigation,
clipboard copying, word list editing, and the empty-list error. To run only the
generator tests without installing Qt:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p test_generator.py -v
```

Equivalent installed launch commands are `pangolin`, `python -m pangolin`, and
`python main.py` when run with the project environment's Python. If Qt cannot
be imported, check that your editor uses `.venv/bin/python`.

## Dependency references

- [PyQt6 release files and Python requirement](https://pypi.org/project/PyQt6/6.12.1/)
- [uv project setup](https://docs.astral.sh/uv/guides/projects/)
- [Python secrets module](https://docs.python.org/3/library/secrets.html)

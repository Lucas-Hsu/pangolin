# Pangolin

A desktop password generator using the three supplied drawings as its interface.

## Start on macOS

Requires macOS 14+, an internet connection for first setup, and either `uv` or
Python 3.10+. Python 3.12 is the default; Python 3.15 is not required.

Extract the ZIP and double-click **Start-Pangolin.command**. The launcher uses
`uv` if available, otherwise it creates a local `.venv` using an existing Python
installation and installs the dependencies. It does not install global tools.

Or, from the extracted `pangolin-main` folder:

```bash
uv run pangolin
```

Without uv:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --only-binary=PyQt6,PyQt6-Qt6,PyQt6-sip,cryptography -e .
.venv/bin/python main.py
```

Use Python 3.10+ for `python3`. If the launcher loses its executable permission
when extracted, run `bash ./Start-Pangolin.command`. Qt and cryptography use
prebuilt wheels; the launcher does not attempt to compile Qt or Rust.

## Screens

1. An empty bank shows the welcome drawing. Click its **Set Up** button.
2. Answer all fourteen questions in the scrolling form. The same **Set Up** button
   at the bottom becomes available when every answer is nonblank. It saves the
   answers and opens the password screen.
3. At the start of every session, the new main drawing appears with its original
   **CLICK2COPY** and **Password here** text. No password is generated or copied
   automatically. Press the pangolin, labeled **GENERATE** in curved coral text
   matching the supplied color swatch, to generate immediately and start a
   two-turn spin. It starts fast and only eases out over 1.1 seconds. Each further
   press generates again and restarts that coast from the current angle, without
   resetting or pausing, so continued clicks keep it spinning. Once clicks stop,
   it coasts to an upright finish so GENERATE stays readable. Generating leaves the
   clipboard alone. Click the bubble to copy the displayed password; the bubble
   flashes green and fades back to confirm success. Clicking the placeholder
   before generating does not copy its text.

   Uppercase, Digits, Symbols, and Minimum length remain real controls placed
   over the drawing. The arrows change the length; the number can also be typed.
   All interactive controls brighten slightly on hover. Persistent controls pop
   up to 1.1 times their size on a press and settle back; Set Up and Clear Data
   change screens immediately without a click animation.

The fourteen questions cover color, animal, pet's name, three favorite numbers,
food, dance, song, drink, activity, adjective, verb, and noun. All three number
fields accept ASCII digits only (0–9), including leading zeros; letters, signs,
decimal points, and spaces are rejected. All three answers supply the digit bank
used for password generation. Earlier twelve-answer saves remain readable and
use their original numeric favorite. To enter the two new numbers on an existing
installation, use Clear Data and complete Set Up again. Whole answers are retained, so generated passwords
can exceed the requested minimum length. Length alone does not determine the
strength of a password made from personal favorites.

There is no word-list screen. **Clear Data** deletes the saved answers, clears
all fourteen inputs and the displayed password, and returns to the welcome screen.
It clears the clipboard if it still contains the last password copied by this
window. It leaves unrelated clipboard content alone. Returning users with a
saved, nonempty bank go directly to the password screen.

Tooltip events are suppressed throughout the application. There is no Word List screen. The pangolin is the Generate control;
the bubble is the Copy control.

## Artwork and sizing

The original PNGs are preserved unchanged in `src/pangolin/assets/originals/`.
The new main-screen drawing is `page3-v2.png`; the earlier drawing is retained
as `page3.png` for reference. The updated question artwork is `page2-v2.png`;
its three different bubble silhouettes repeat in order by question index modulo 3.
The original question artwork remains available as `page2.png`.
The app uses extracted image assets for the drawings, bubble, Set Up button,
question shapes, answer fields, check states, and scroll thumb. The new main drawing’s instructional text is shown initially. After generation,
only “Password here” is replaced by live text; the CLICK2COPY caption remains.
There is no generated replacement illustration.

Welcome and password screens scale uniformly and center within differently
shaped windows; they do not stretch the drawings. The question form fits the
window width and scrolls vertically beneath the original fixed header. Live
questions, answers, password, and length value use the system font. Clear Data
uses the supplied lettering.
Embedded image color profiles are converted to sRGB when drawn, preserving the
appearance of the original Generic RGB artwork.

`tools/extract_art.py` reproduces the cropped assets from the originals. It is a
development tool requiring Pillow (`python -m pip install Pillow`), not a runtime
dependency. Update those source PNGs and extraction coordinates for future art.

## Saving

The word bank is encrypted with Fernet and stored at:

```text
~/Library/Application Support/Pangolin/words.enc
```

The exact phrase from the original `init_encryption` function is kept in
`src/pangolin/encryption.py`. At runtime it is hashed with SHA-256 to obtain
32 **bytes** (256 bits), then encoded with URL-safe Base64 for Fernet. The key is
intentionally embedded in the source, not a user-supplied secret. Someone with
the source can derive it; this is not a master-password-protected vault.

Writes use a private temporary file and atomic replacement. Existing
`words.json` from the earlier version is migrated to encrypted storage and
removed after the successful save. Clear Data removes both file formats.
Generated passwords are not written to disk.

## Develop and check

```bash
uv run python -m unittest discover -s tests -v
uv build
```

Tests cover the three-screen flow, required answers, scrolling, generation and
clipboard copying, the two-turn animation, copy-only green confirmation,
rapid repeat presses, digit-only input and the three-number bank, hover and press
feedback, reset, returning users, proportional resizing, tooltip
suppression, encrypted round trips, legacy migration, corrupt files, and failed
writes. The tests use isolated temporary folders rather than the real app data.

When PyQt6 is unavailable but a system PyQt5 installation is present, an optional
compatibility runner checks the same painter code and widgets:

```bash
PYTHONPATH=src python3 tests/qt5_check.py
```

This fallback runner does not certify native macOS or Qt6 behavior. The app's
normal runtime and dependency remain PyQt6. `examples/original_prototype.py`
retains the original root script unchanged for reference; it is not an app entry
point and still contains the original unfinished encryption code.

Reference: [Fernet key format](https://cryptography.io/en/latest/fernet/).

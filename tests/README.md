# The Forge · tests

These scripts open the built `the_forge.html` in headless Chromium (Playwright) and exercise the
library, the Studio, the storage card, the backup and the packaging exactly as a person would:
through the real file chooser, the real buttons and the real preview frame. They are the
"testing framework for the library system" asked for in 9s62: every check is a measurement.

## Running

    npm install playwright@1.56   # once, or use a global install; Chromium must be installed
    sh tests/run.sh               # serves the file on 127.0.0.1:8765 and runs every test

Each test takes the apps it works on from environment variables (defaults in `tests/env.sh`):

    FORGE_HTML      the file to test (default: ./the_forge.html)
    INGENIUM_HTML   a full ingenium.html, INKWELL_HTML an Inkwell.html, CARPE_HTML a Carpe Diem index.html

Tests that need an app file skip, and say so, when the file is absent.

## What is covered

| test | what it proves |
| --- | --- |
| `boot.test.js` | the file boots with no page error; the door, the Editor and the Studio are there |
| `studio.test.js` | an app opens through step 1, every page is found, a part is changed live and kept as a new version, the earlier copy stays |
| `library.test.js` | the in-app store self-test passes on this browser; copies read back at their recorded size |
| `storage_backup.test.js` | the Storage card measures, a limit warns, Clean the library frees the earlier copies, the zip backup exports and reads back whole into a fresh profile |
| `compare.test.js` | two kept versions compare in words and by line; the same file twice says so |
| `a11y.test.js` | axe-core finds no serious or critical violation in the open rooms (needs `tests/axe.min.js`) |

A failure prints the step that failed and leaves screenshots in `tests/out/`.

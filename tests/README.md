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
    FORGE_BASE_61   (review test only) the 9s61 the_forge.html, whose old applier is planted in a test version

Tests that need an app file skip, and say so, when the file is absent.

## What is covered

| test | what it proves |
| --- | --- |
| `boot.test.js` | the file boots with no page error; the door, the Editor and the Studio are there |
| `studio.test.js` | an app opens through step 1, every page is found, a part is changed live and kept as a new version, the earlier copy stays |
| `library.test.js` | the in-app store self-test passes on this browser; copies read back at their recorded size |
| `storage_backup.test.js` | the Storage card measures, a limit warns, Clean the library frees the earlier copies, the zip backup exports and reads back whole into a fresh profile |
| `compare.test.js` | two kept versions compare in words and by line; the same file twice says so |
| `a11y.test.js` | axe-core finds no serious or critical violation in the open rooms, measured on the settled page with the entrance fades switched off (needs `tests/axe.min.js`) |
| `review.test.js` | the defects the 9s62 review found, each shown fixed: a second Keep keeps the first edits; blocks and copies on one part stay put over many passes and moves; a version kept under 9s61 runs one Studio on the stage; Clean never hangs; Merge keeps this device's copies; the library tells its listeners; the Editing panel fits a short window; a full device is said in Files; the comparison is fast and speaks French; the Studio's second copy of the edits travels in the zip; Remove takes the row pressed |

A failure prints the step that failed and leaves screenshots in `tests/out/`.

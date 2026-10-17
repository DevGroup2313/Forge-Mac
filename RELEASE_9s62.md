# The Forge · build 9s62 (pass 630, 17 October 2026)

`the_forge.html` at the top of this repository is the whole app, built from the 9s61 package build by the
patches in `tools/9s62/` (see `tools/9s62/README.txt`). The device packages and the standalone file are in
`dist/` (made by the Forge itself, from its own Download-the-app step, in headless Chromium).

## What changed, and how each was verified

Every item below was run in a real browser (headless Chromium, Playwright) against your real app files:
Ingenium 3.2 (`ingenium.html`, 13.3 MB), Inkwell 7.42, Carpe Diem 1051 (the committee demo, 16 MB) and the
Forge itself. The scripts are in `tests/` and run with `sh tests/run.sh`.

### The Editor edits the whole app (your main ask)
- The Studio in the Editor (step 2) finds every page, tab, window and menu of the app on the stage, goes to
  any of them, lets you point at any part and change its words, looks, place or visibility, and the preview
  follows at once. Measured: Ingenium 14 places, Inkwell 13, Carpe Diem 9, the Forge 17; a part changed
  live in each; the kept version carries the change; the earlier copy stays one step back.
- Fixed: a version of **Carpe Diem** kept with Studio edits lost them, because Carpe Diem 1051 carries a
  Studio of its own that ran first and swallowed the baked edits. The baked applier now stands in the head
  and merges with the app's own; verified by keeping a change in Carpe Diem and reopening it.
- A version kept from the Studio now reads "your version of 17 October" in the library, not "the file you
  chose".
- New in the Studio: **Copy this part** and **Paste the copied part after it** carry any part of one app
  into another (a card from Carpe Diem into Ingenium, as data: scripts and handlers are taken out);
  **A block of my own** puts your own HTML after a part; new apps can be **removed by name**; a plain line
  says when the stage is not answering. Verified end to end.
- The Editor's steps now read 1 the file, 2 the whole app, 3 named surfaces (the quick way), 4 change it,
  5 download; the help card and the walkthrough say the same.

### The Editing panel (the dropdown)
- One row per app, each under the seal its own code draws (Carpe Diem 1051, Inkwell 7.42, Ingenium 3.2,
  with a day face and a night face each; the Forge's drawn live), the name beside it, and a line saying
  which copy this device keeps. The panel scrolls instead of running past a short screen; measured at
  1600, 1100 and 760 px wide and at a 640 px tall window, day and night.

### Storage, backup, migration
- Settings, Backup: a **Storage** card with a meter, the Forge's own count (app copies, Files, new apps,
  settings), a **limit of your own** with warnings at 80 and 95 per cent, **tidying by itself** when you
  ask for it (the earlier copies first, oldest first, never a newest copy, a file or a new app), and
  **Clean the library**. Verified: a 62 MB library with a 50 MB limit tidied itself down to 32 MB.
- **Export everything as one zip**: the JSON backup, the files of Files, every kept copy of every app
  (with its SHA-256), the Studio's new apps, a READ ME. **Read a zip back** whole or merged; every entry
  is checked against its checksum and the apps against their fingerprint; a broken one is named and
  skipped; a full device is said plainly. Verified by exporting from one profile and reading back into a
  fresh one. A **Move to another device** card gives the steps per device.
- Plain words when the store refuses (full, closed in a private window, or a fault) in Files, the new
  file and the text editor; a device with no IndexedDB at all is told so, and nothing throws (tested with
  IndexedDB removed).

### Compare two versions
- Editor, Troubleshoot: **Compare two versions**: the stage, any kept copy, a new app or a file; said in
  words first (lines added and removed, places, where the first is), then shown place by place, before in
  red and after in green; the report can go on the stage or into the Library. A 19,000-line file compares
  in about 10 ms.

### Testing framework
- Troubleshoot: **Test the store**: a scratch IndexedDB written, read back whole, counted with a cursor,
  made to abort, cleaned up; the browser's own reading of its storage, persist, the zip streams, SHA-256
  both ways, and the library's own records read back at their recorded sizes.
- `tests/`: a Playwright suite (boot, studio with all four apps, library, storage and backup, compare,
  axe-core accessibility, and the review's fixes) with a runner and a README.

### Accessibility
- axe-core 4.10 over every room: 25 findings in 9s61 (tab roles, the resize handle's value, heading
  order, unnamed fields), all fixed; every room is now clean, day and night.
- Troubleshoot: **Check this room for screen readers**: names, alt words, heading order, tab roles,
  labels, contrast (translucent faces blended as the eye sees them), with a line per fault.
- Guidebook: **Testing with a screen reader**: VoiceOver on the Mac, iPhone and iPad, VoiceView on the
  Fire tablet, Narrator and NVDA on Windows, with what to listen for in each room. A machine finds the
  missing name; only you, with the reader your device carries, find what confuses. That part is yours.

### How much help
- First day, Finding my way, At ease: chosen on any help card or in Settings and kept on the device. The
  help cards, the walkthrough's "why" lines and a line of context as each step of the Editor opens follow
  the choice.

### The curriculum, rewritten
- All thirty-six modules, seventy-two lessons and one hundred and forty-four questions rewritten for you:
  every lesson has the same five parts in the same order (Look, Do, Name, Why it matters to you, Done
  when) and a way to stop; the doing comes before the naming; every lesson points at Carpe Diem, Inkwell,
  Ingenium or the Forge; year 1 runs on the right, years 2 and 3 predict then check and send you to the
  Terminal on your Mac; the ids are unchanged, so what you had read stays read.

### The review, and what it changed
After the first build, every patch was read again adversarially (each claim traced in the built file and in
Chromium) and the real defects were mended; the list is in `tools/9s62/README.txt`. The ones you would have met:
- A second **Keep** in the Studio used to drop the edits already in the version's code. Now they stay, and the
  new ones join them. Verified by keeping twice in Ingenium.
- Two pasted blocks (or a block and a copy) on one part multiplied on every redraw; a part moved beside another's
  block did the same. Fixed in the applier; verified over five passes.
- A version kept under 9s61 ran two Studios on the stage, which fought over the colours. One runs now.
- **Merge** in the zip restore could overwrite your own version of an app with the zip's older copy. Merge now
  keeps what is here. The Studio's second copy of the edits travels in the zip too.
- **Clean the library** pressed during the first measure could freeze the page; a refused tidy could flood the
  diary. Both gone.
- A full device aborted a Files write silently; the refusal is now said in plain words (verified with a 200 KB
  quota).
- **Compare two versions** of the Forge itself took fifteen seconds; now about sixty milliseconds.
- Removing a new app by name could remove the wrong one when two shared a name; Remove now takes the row pressed.
- The Editing panel's height follows its key, so its foot never leaves a short window.
- The walkthrough's **why** lines were missing on steps 4 and 5 and on a second start; the context line spoke at boot
  for a step you never opened and brought back the tutor line you had hidden. Both fixed.
- The Guidebook chapter **Testing with a screen reader** was never listed (it was added after the Guidebook had
  indexed its chapters). It is now under Good to know, and search finds it. The checker also finds an unlabelled
  field and a nameless control on a closed page, and no longer scrolls you away.
- **Check my prediction** showed the answer for a second and a half, then a repaint hid it again (and wiped an answer
  given meanwhile in the questions room). The answer now stays, and the counts follow in place.
- Five C++ programs in year 3 lacked their `#include` lines; added, and every whole program in year 3 compiles
  except the four whose lessons are about the compiler's refusal.

## Installing

Each zip in `dist/` opens with READ ME FIRST.txt. The standalone file `the_forge.html` opens in any
browser with no installer. Every package's app file is byte for byte the repository's `the_forge.html`.

## The APK

The Fire package carries the Android project and its GitHub workflow. The APK your tablet will accept as
an update must be signed with the permanent key your repository holds (`signing/`), which this session
does not have; an APK built here would be signed with a throwaway key and the tablet would refuse to
install it over the one you have. So: upload the contents of `Fire tablet project` to your Fire
repository as before, and GitHub builds and signs the APK (Releases, `the-forge.apk`). The project was
compiled here to prove it builds; see the notes at the end of this file.

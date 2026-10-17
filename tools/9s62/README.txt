THE FORGE 9s62 · HOW THIS BUILD IS MADE

the_forge.html at the top of the repository is built from the 9s61 package build (the_forge.html inside the
9s61 device zips, byte for byte, kept beside this folder as the base) by applying the patches in this folder,
in order, with build.py:

    FORGE_PATCHES=p_studio,p_appseals,p_steps,p_libapi,p_storage,p_backup,p_errors,p_diff,p_studio2,p_selftest,p_a11y,p_guidance,p_curriculum,p_stamp \
    python3 tools/9s62/build.py <output path>

build.py expects the base at ../base_9s61.html relative to this folder, or at the path in the FORGE_BASE
environment variable (FORGE_BASE=/path/to/base_9s61.html).
Each patch names its anchor in the 9s61 file exactly once; if an anchor is not found exactly once, the build
stops and says which. Every patch carries a comment that says what it changes and why, as the Forge's own
passes do.

The patches, in order:
  p_studio      the Studio's applier (applier_v2.js) planted in the head and merging with an app's own Studio;
                a version kept from the Studio is "your version" in the library
  p_appseals    the Editing panel: one row per app, each under its own seal (seals/seals.json), the panel scrolls
  p_steps       the Editor's steps in the order she meets them (1 file, 2 whole app, 3 surfaces, 4 change, 5 download)
  p_libapi      the app library and the zip writer lend their functions by name
  p_storage     Settings · Storage: meter, limit, warnings, tidying, Clean the library
  p_backup      everything in one zip, read back whole or merged; Move to another device
  p_errors      plain words when the store refuses; a device with no store is told so
  p_diff        Compare two versions
  p_studio2     the Studio's pocket (copy and paste a part between apps), a block of her own, new apps removed by name
  p_selftest    Troubleshoot · Test the store
  p_a11y        axe-core's findings fixed; Check this room for screen readers; the Guidebook chapter on screen readers
  p_guidance    how much help: First day, Finding my way, At ease; the walkthrough's why; context as a step opens
  p_curriculum  the three years rewritten for her (curriculum/y1.js, y2.js, y3.js), ids unchanged
  p_stamp       the build's date, pass and stamp

seals/seals.json holds the seals of Carpe Diem 1051, Inkwell 7.42 and Ingenium 3.2, drawn by each app's
own seal code on 17 October 2026 (a day face and a night face each, 128 px PNGs with a clear ground).

THE REVIEW, AND WHAT IT CHANGED (17 October 2026)
After the first 9s62 build, every patch was read again adversarially, each claim traced in the built file and in
Chromium, and the real defects mended in the patches (the built file was then rebuilt from the base and the whole
suite run again). In the order of the patches:
  p_studio      a second Keep (or Download the edited app) used to bake the new edits alone and drop the ones already
                in the version's code: bakeEdits now reads them out of the version and keeps them. The baked tag
                stands after the app's charset, never before it. The stage's copy of a version kept earlier had its
                own older applier at the foot of the body fighting the new one over the same style sheet: that
                applier is taken out and the new one stands in the head with the version's edits.
  applier_v2    two copies or blocks on one part made each other again on every pass; a part moved between another
                part and its block made that block again on every pass. A copy or block is now found anywhere
                beside its part, and a part moves with its run of copies and blocks.
  p_appseals    seals.json is read beside the module; the panel's status line reads the library's cached list
                (a fresh read emptied the cache for a moment and the switch mounted the wrong file); the panel's
                height is taken from where its key stands, below or above it, so its foot never leaves the window.
  p_steps       the French Workshop refusal and the Guidebook's shipping article name the right steps; the Editor's
                help lists 2, 3, 4 in that order in both languages.
  p_libapi      the library says 'forge:lib' on the window whenever a copy is kept, opened or dropped (the paint
                hook alone was never called by the library itself); keepRaw refuses an unknown app or slot;
                sizes() no longer hides a device with no store; metaCached reads without emptying the cache.
  p_storage     one measure at a time, each source answered for after twelve seconds (a hung store could hold the
                card for the whole session); Clean during a measure no longer re-queues itself without end (the page
                froze); tidying that the device refuses rests for ten minutes instead of flooding the diary; the
                tidy report is not painted over at once; a device with no store is named in the card.
  p_backup      Merge keeps what is here: the zip's newest copy comes in only when newer, its earlier copy only when
                the device keeps none (the old order wrote the zip's earlier copy over her own version); the
                Studio's second copy of the edits (forge-studio/edits) travels in the zip and comes back, whole or
                merged by date; a device with no store is told plainly; French counts; one cached read in the
                export; the Mac hand-over falls back to a download if reading the zip back fails.
  p_errors      a full device aborts the Files transaction without an error event: the abort is heard and the
                refusal said; a refusal among several files stays in view while the others are counted; a store
                closed by SecurityError is named as closed; the no-store line is not painted over.
  p_diff        the pairing is linear (a concat per anchor made the Forge against itself take fifteen seconds; now
                about sixty milliseconds); the first pair offered is one app's two copies; the fold speaks French;
                a new app on the stage is what 'the stage' means; the plain-text report keeps < and >; a chosen
                file keeps its name in the list; 'copied' is said only when the clipboard took it.
  p_studio2     Remove takes the row pressed, by id (two new apps may share a name); removing the app on the stage
                with no file in step 1 clears the stage; the box for a block of her own stands outside the part's
                card so pointing elsewhere does not empty it; the pasted part's label no longer hides the part it
                was placed after; the 'What you just did' box explains a paste; a copy that could not be kept, or
                was cut at 200 000 characters, is said; the hand's neighbour for a move skips the part's own run.
  p_selftest    the real error name is read from the request; the megabyte pattern is not all zeros at the sampled
                points; the fold speaks French; 'copied' is said only when the clipboard took it.
  curriculum    five C++ programs in year 3 lacked their #include lines (c04, c08, c11); every whole program in
                year 3 now compiles except the four whose lessons are about the compiler's refusal (c01, c08 private,
                c09 three files, c11), and every Python snippet in year 2 runs.
tests/review.test.js shows each of these fixed in Chromium.


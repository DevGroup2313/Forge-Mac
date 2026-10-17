THE FORGE 9s62 · HOW THIS BUILD IS MADE

the_forge.html at the top of the repository is built from the 9s61 package build (the_forge.html inside the
9s61 device zips, byte for byte, kept beside this folder as the base) by applying the patches in this folder,
in order, with build.py:

    FORGE_PATCHES=p_studio,p_appseals,p_steps,p_libapi,p_storage,p_backup,p_errors,p_diff,p_studio2,p_selftest,p_a11y,p_guidance,p_curriculum,p_stamp \
    python3 tools/9s62/build.py <output path>

build.py expects the base at ../base_9s61.html relative to this folder (set BASE in build.py otherwise).
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

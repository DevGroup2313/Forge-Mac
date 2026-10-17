THE FORGE 9s62 · HOW THIS BUILD IS MADE

the_forge.html at the top of the repository is built from the 9s61 package build (the_forge.html inside the
9s61 device zips, byte for byte) by applying the patches in this folder, in order, with build.py:

    python3 tools/9s62/build.py  <output path>

Each patch names its anchor in the 9s61 file exactly once; if an anchor is not found exactly once, the
build stops and says which. The base file is expected at tools/9s62/../../base_9s61.html or as BASE in
build.py. Every patch carries a comment that says what it changes and why, as the Forge's own passes do.

seals/seals.json holds the seals of Carpe Diem 1051, Inkwell 7.42 and Ingenium 3.2, drawn by each app's
own seal code on 17 October 2026 (a day face and a night face each, 128 px PNGs with a clear ground).

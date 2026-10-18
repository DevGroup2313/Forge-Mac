THE FORGE  |  Copyright (c) 2026 Yannie D. Forest. All rights reserved.
NO LICENCE IS GRANTED. No copying, adaptation, redistribution, reverse
engineering or commercial use without the author's written permission.
See LICENCE.txt. Every distributed copy carries a build marker.
--------------------------------------------------------------------------

THE FORGE ON A MAC
==================

Build 637 (9s69), 2026-10-18. Made by The Forge, 18 October 2026.

New in 637. The help level keys ("First day", "Finding my way",
"At ease") are raised and move like every other key in the Forge: they
lift under the pointer, sink when pressed, and the chosen level is the
filled key, which settles into place. They follow day, night and the
Forge's Minimal motion setting.

Since 636 it carries Inkwell 7.45, Carpe Diem 1055 (whose Tabula holds a
thesis of 100,000 words and whose mini Forge edits Carpe Diem alone) and
Ingenium 5.4, and a copy of itself. The Mac app in every kit the Forge
makes builds on GitHub: its first start as Intel, under Rosetta, may
take up to 40 seconds before the build counts it as failed (it was 12).
Its own Tabula has held a thesis of 100,000 words since 635.

This repository builds the app by itself: the workflow in .github finds
this folder, builds The Forge.app for Intel and Apple silicon Macs, opens
it on GitHub's Mac to check it, and puts The-Forge-Mac.zip on the
Releases page (tag the-forge-mac).

This package holds everything needed to put The Forge on a Mac as a
real app, and to rebuild it yourself later on GitHub, with no help and
nothing to install on your Mac.

WHAT IS IN THIS PACKAGE
  READ ME FIRST.txt               This guide.
  Mac project/                    Everything GitHub needs to build the app.
                                  It also holds the_forge.html, the whole app.
  GITHUB_WORKFLOW_paste_this.txt  The build recipe, as a visible file you can
                                  copy from (Part 1, Step 3).
  LICENCE.txt


THREE WAYS TO HAVE THE FORGE ON THE MAC
---------------------------------------
  WAY A. JUST OPEN IT. In "Mac project", double-click the_forge.html.
         It opens in Safari and runs offline. Nothing to build.
  WAY B. THE READY-MADE APP, BUILT BY GITHUB (recommended).
         Parts 1 and 2 below. One app for Intel and Apple silicon Macs.
  WAY C. BUILD THE APP ON THIS MAC. Part 4 below. Needs Python 3.


PART 1. HAVE GITHUB BUILD THE APP
---------------------------------

Step 1. Make a repository.
  Sign in at github.com. Click the "+" at the top right, then
  "New repository". Name it, for example the-forge-mac. Choose
  Private. Do NOT tick "Add a README file". Click "Create repository".
  (You may use a repository you already have for this app instead.)

Step 2. Upload the project.
  On the new repository's page click "uploading an existing file".
  Open the folder "Mac project" from this package, select EVERYTHING
  INSIDE IT, and drag it onto the page. You should see the_forge.spec,
  the_forge_app.py and the_forge.html in the list. Wait until every file
  has finished uploading, then click "Commit changes".

Step 3. Add the build recipe. THIS STEP MATTERS.
  The recipe lives in a folder called .github. A Mac hides every name
  that begins with a full stop, so this folder is almost always left
  behind when you drag files. Without it GitHub never builds anything.
    a. On the repository page click "Add file", then "Create new file".
    b. In the name box type exactly:
           .github/workflows/build-mac-app.yml
       (GitHub turns each "/" into a folder as you type.)
    c. Open GITHUB_WORKFLOW_paste_this.txt from this package, select all
       of it, copy it, and paste it into the large box on GitHub.
    d. Click "Commit changes", then "Commit changes" again.
  If GitHub says the file already exists, it uploaded in Step 2. Fine.

Step 4. Wait for the build.
  Click the "Actions" tab. "Build The Forge for Mac" runs for about three
  to six minutes. A yellow dot means it is working; a green tick means it
  worked. Before publishing, it opens the finished app on GitHub's Mac
  twice (as Apple silicon and as Intel) and keeps photographs of it under
  "Artifacts" (mac-screenshots), so you can see that it opened.
  If nothing has started after a minute: click "Build The Forge for Mac"
  on the left, then "Run workflow", then the green "Run workflow".

Step 5. Get the app.
  On the repository's main page, on the right, click "Releases", then
  "The Forge for Mac", then The-Forge-Mac.zip. It is also on the run's
  page under "Artifacts".

COST: for a private repository GitHub counts each minute on its Mac
computers as ten minutes of your monthly allowance (as far as I know).
One Mac build takes a few minutes. Please check GitHub's current figures
on its billing pages.


PART 2. INSTALL THE APP
-----------------------

1. Double-click The-Forge-Mac.zip. It becomes The Forge.app.
2. If you already use The Forge on this Mac, export a backup from it
   first and keep the file. The new app uses the same storage as before,
   so your work should simply be there; the backup is your safety net.
3. Drag The Forge.app into Applications. If an older one is there,
   choose Replace.
4. The first open. The app is not notarised by Apple, so macOS blocks
   the first open. Use ONE of these:

   A. Terminal (one line, most reliable). Open Terminal (Command+Space,
      type Terminal, Return), paste this line, and press Return:

          xattr -dr com.apple.quarantine "/Applications/The Forge.app"

      Then double-click The Forge in Applications.

   B. System Settings. Double-click the app and let macOS refuse it.
      Open System Settings, then Privacy & Security, scroll down to the
      message about The Forge, click "Open Anyway", and confirm with
      your password.

   On macOS Sequoia and later, right-click then Open no longer works
   for this.
   That is an Apple change, not a fault in the app.

After the first open it opens normally from then on.


PART 3. UPDATING THE APP LATER
------------------------------

  1. On GitHub, open your repository. Click "Add file", then "Upload
     files", drop in EVERYTHING inside the new package's "Mac project"
     folder (the app, its icons, BUILD_INFO.txt and the rest; the files
     replace the old ones), and commit. The app's version (shown by
     Finder's Get Info) is read from BUILD_INFO.txt.
  2. Replace the recipe too, since Finder leaves the .github folder
     behind: open .github/workflows/build-mac-app.yml on GitHub, click
     the pencil, select all, paste GITHUB_WORKFLOW_paste_this.txt over
     it, and click "Commit changes".
  3. GitHub builds again by itself (Part 1, Steps 4 and 5).
  4. Download the new The-Forge-Mac.zip and install it over the old app
     (Part 2). Your work stays.


PART 4. BUILDING ON THIS MAC INSTEAD (optional)
-----------------------------------------------

"Build Mac App.command", inside "Mac project", builds the same app on
this Mac. It needs Python 3 from python.org and the internet once, to
fetch its build tools. Double-click it; if macOS refuses to run it, see
MACOS_IF_BLOCKED.txt in the same folder. The app appears in the "dist"
folder (or on the Desktop, when the folder sits on a USB stick). The app
it makes runs on Macs like this one; the GitHub build runs on every Mac.


IF THE BUILD FAILS
------------------

A red cross within a few seconds, with no steps listed:
  GitHub refused to start the build. This is about the GitHub account,
  not the app. Open the failed run and read the notice near the top.
  The usual reasons are that the account has used its monthly free
  minutes, or a spending limit or payment problem in the billing
  settings (github.com/settings/billing). Fix what the notice names,
  then click "Re-run all jobs".

A red cross after some minutes, with steps listed:
  Click the step with the red cross. "If the build failed, show why"
  prints the last 80 lines of the build log; they name the cause.

"the_forge.spec not found":
  The project was not uploaded, or only partly. Upload the CONTENTS of
  "Mac project" again (Part 1, Step 2).


ABOUT THE APP
-------------
  - It runs entirely from the copy of the_forge.html inside it and works with
    no connection. Your work is kept by macOS for this app, on this Mac. It
    stays when you quit, and when you replace the app with a newer build.
    To carry it to another Mac, export a backup in the app and read it back
    in the app on the other Mac.
  - The first time something in it asks for the microphone, macOS asks
    whether The Forge may use it: choose Allow. If it was refused:
    System Settings, Privacy & Security, Microphone, switch it on.
  - Its Mac identity is com.yannieforest.theforge and its version is 630.

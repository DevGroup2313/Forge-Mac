THE FORGE · BUILD 9s62 (pass 630, 17 October 2026) · THE PACKAGES

Every package was made by the Forge itself, from its own Download-the-app step (the Forge opened as the
app on its own stage, in headless Chromium). The app file inside each one is byte for byte the
the_forge.html at the top of this repository. Each zip opens with READ ME FIRST.txt.

  the_forge_mac_9s62.zip        MacBook Pro: the Mac project with its GitHub recipe, and "Build Mac App.command"
  the_forge_mac_mini_9s62.zip   Mac mini (Apple silicon): the same universal app, with a guide written for the Mac mini
  the_forge_windows_9s62.zip    Windows: the project, its GitHub recipe, and the installer recipe (Inno Setup)
  the_forge_ios_9s62.zip        iPhone and iPad: the Xcode project with its GitHub recipe, and the Home Screen app
  the_forge_fire_9s62.zip       Fire tablet: the app file for Silk, and the Android project with its GitHub recipe
  the_forge_web_9s62.zip        the web: index.html, the manifest, the service worker and the icons

  the_forge.html (at the top of the repository)   the standalone app, no installer: open it in any browser

THE APK
  the_forge_fire_9s62_debug-signed_fresh-install-only.apk
  Built here from the Fire project above (compileSdk 34, versionName 630), as proof that the project
  builds. It is signed with a throwaway key, because the permanent key lives in your own GitHub
  repository's "signing" folder and never leaves it. Android installs a new APK over an old one only when
  both carry the same signature, so THIS FILE WILL NOT INSTALL OVER THE FORGE YOU ALREADY HAVE; it installs
  only as a fresh app (uninstalling the old one first would delete what it saved). For the update your
  tablet will accept, upload the contents of "Fire tablet project" from the_forge_fire_9s62.zip to your
  Fire repository as before: GitHub builds and signs the-forge.apk with the permanent key and puts it on
  the Releases page.

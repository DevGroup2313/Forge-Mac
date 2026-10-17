"""9s62 · the build's own name: date, pass and stamp, wherever the page says them."""
MARK = '<!-- CD-BUILD-MARKER: 9s62 | 2026-10-17 | the Studio reaches every app whole and its kept edits survive Carpe Diem; each app under its own seal in the Editing panel; the steps in order; Storage with a limit, warnings, tidying and Clean the library; everything in one zip, read back on any device; Compare two versions; Test the store; the screen-reader check and axe clean in every room; how much help; the Studio\'s pocket (a part carried between apps, a block of her own); the curriculum rewritten for her, three years; on top of 9s61: '
def apply(P):
    P.replace_once('<!-- CD-BUILD-MARKER: 9s61 | 2026-10-12 | ', MARK, 'marker')
    P.replace_once('window.CD_BUILD={date:"2026-10-12",pass:"629",stamp:"9s61"};', 'window.CD_BUILD={date:"2026-10-17",pass:"630",stamp:"9s62"};', 'CD_BUILD')
    P.replace_all('<span class="build">Build 2026-10-12 · 629 · 9s61</span>', '<span class="build">Build 2026-10-17 · 630 · 9s62</span>', 'build spans', expect=2)
    P.replace_once('id="aboutSealDate">die XXIII Augusti MMXXVI', 'id="aboutSealDate">die XVII Octobris MMXXVI', 'about seal date')
    # the Guidebook's glossary names the build too (the 9s61 pass updated it; this one did not, found by the review)
    P.replace_once('this Forge is build 629.', 'this Forge is build 630.', 'glossary build en')
    P.replace_once('cette Forge est le build 629.', 'cette Forge est le build 630.', 'glossary build fr')

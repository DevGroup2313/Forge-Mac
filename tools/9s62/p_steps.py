"""9s62 · the Editor's steps in the order she meets them: 1 the file, 2 the whole app (the Studio), 3 named surfaces, 4 change it, 5 download."""
def apply(P):
    P.replace_once('<summary><span class="n">2</span><span class="t">🧭 Pick a surface</span>', '<summary><span class="n">3</span><span class="t">🧭 Pick a named surface (the quick way)</span>', 'fold surface 3')
    P.replace_once('<summary><span class="n">3</span><span class="t">🎛️ Change it</span>', '<summary><span class="n">4</span><span class="t">🎛️ Change it</span>', 'fold controls 4')
    P.replace_once('<summary><span class="n">4</span><span class="t">📦 Download the app</span>', '<summary><span class="n">5</span><span class="t">📦 Download the app</span>', 'fold ship 5')
    P.replace_once("""d.innerHTML='<summary><span class="n">✦</span><span class="t">✍️ '+T('The whole app: go anywhere, point at a part, change it','L’app entière : allez partout, montrez une partie, changez-la')+'</span>""",
                   """d.innerHTML='<summary><span class="n">2</span><span class="t">✍️ '+T('The whole app: go anywhere, point at a part, change it','L’app entière : allez partout, montrez une partie, changez-la')+'</span>""", 'studio fold 2')
    P.replace_once('<p>A surface is one named part of the page. Pick one; its controls open in step 3.</p>',
                   '<p>A surface is one named part of the page that the app itself registered (its rail, its door, its top bar). Pick one; its controls open in step 4. For anything else on any page, use step 2.</p>', 'surface lede')
    P.replace_once('Each app keeps its own edits, its own surfaces in step 2, and its own way out in step 4. Another app offers',
                   'Each app keeps its own edits, its own surfaces in step 3, and its own way out in step 5. Another app offers', 'tip steps')
    for old, new in (('In 2, Pick a surface: choose the part of the app you want to change.', 'In 3, Pick a named surface: the quick way to show, hide, rename, reorder or colour a part the app registered (its rail, its door, its top bar).'),
                     ('In 3, Change it: change the words, the colour or the picture. The preview on the right follows at once.', 'In 4, Change it: the words, the order, the colour. The preview on the right follows at once.'),
                     ('In 4, Download the app: save the edited app as one HTML file, or make its i', 'In 5, Download the app: save the edited app as one HTML file, or make its i'),
                     ('En 2, Choisir une surface : choisissez la partie de l’app à changer.', 'En 3, Choisir une surface nommée : le chemin rapide pour montrer, cacher, renommer, réordonner ou colorer une partie que l’app a nommée (son rail, sa porte, sa barre du haut).'),
                     ('En 3, La changer : changez les mots, la couleur ou l’image. L’aperçu à droite suit aussitôt.', 'En 4, La changer : les mots, l’ordre, la couleur. L’aperçu à droite suit aussitôt.'),
                     ('En 4, Télécharger l’app : enregistrez l’app modifiée en un seul fich', 'En 5, Télécharger l’app : enregistrez l’app modifiée en un seul fich'),
                     ('For the whole app, every page: open \\"✍️ The whole app\\", choose a page, press \\"✋ Point at a part\\" and click the part on the right.', 'In 2, The whole app: choose any page of the app, press \\"✋ Point at a part\\" and click the part on the right.'),
                     ('Step 5. Still in 4: ', 'Step 5. Still in 5: '), ('Étape 5. Toujours en 4 : ', 'Étape 5. Toujours en 5 : ')):
        n = P.t.count(old)
        if n == 0: raise SystemExit('steps: missing ' + old[:50])
        P.replace_all(old, new, 'help: ' + old[:30])
    for old, new in (('its own surfaces in step 2, its own checks in Troubleshoot and its own way out in step 4', 'its own surfaces in step 3, its own checks in Troubleshoot and its own way out in step 5'),
                     ('ses propres surfaces à l’étape 2, ses propres vérifications dans Troubleshoot et sa propre sortie à l’étape 4', 'ses propres surfaces à l’étape 3, ses propres vérifications dans Troubleshoot et sa propre sortie à l’étape 5'),
                     ('step 4 gives you Inkwell.html', 'step 5 gives you Inkwell.html'), ('step 4 gives you ingenium.html', 'step 5 gives you ingenium.html'),
                     ('l’étape 4 vous donne Inkwell.html', 'l’étape 5 vous donne Inkwell.html'), ('l’étape 4 vous donne ingenium.html', 'l’étape 5 vous donne ingenium.html'),
                     ('Troubleshoot and step 4 read the live preview', 'Troubleshoot and step 5 read the live preview'), ('Troubleshoot et l’étape 4 lisent', 'Troubleshoot et l’étape 5 lisent'),
                     ('step 4 says so if you choose it', 'step 5 says so if you choose it'), ('l’étape 4 le dit si vous la choisissez', 'l’étape 5 le dit si vous la choisissez'),
                     ('In step 2 the surfaces are listed', 'In step 3 the surfaces are listed'), ('press Export (JSON) in step 4', 'press Export (JSON) in step 5'),
                     ('Les surfaces de l’étape 2 sont celles', 'Les surfaces de l’étape 3 sont celles'), ('et l’étape 4 rend ', 'et l’étape 5 rend '),
                     ('The surfaces in step 2 are ', 'The surfaces in step 3 are '), (', and step 4 hands ', ', and step 5 hands '),
                     ('Its surfaces (step 2) and free CSS work instead.', 'Its surfaces (step 3) and free CSS work instead.')):
        P.replace_all(old, new, 'steps: ' + old[:30])
    # the walkthrough's cards name the folds by number
    for old, new in (('In <b>2, Pick a surface</b>', 'In <b>3, Pick a named surface</b>'), ('In <b>3, Change it</b>', 'In <b>4, Change it</b>'), ('In <b>4, Download the app</b>', 'In <b>5, Download the app</b>'),
                     ('En <b>2, Choisir une surface</b>', 'En <b>3, Choisir une surface nommée</b>'), ('En <b>3, La changer</b>', 'En <b>4, La changer</b>'), ('En <b>4, Télécharger l’app</b>', 'En <b>5, Télécharger l’app</b>')):
        if P.t.count(old): P.replace_all(old, new, 'walk: ' + old[:30])
        else: P.log.append('walk: not present: ' + old[:40])

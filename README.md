Données et code pour l'analyse du [Test électoral 2024 RTBF](https://www.rtbf.be/test-electoral)

Pour calculer les scores des partis pour une liste de 35 réponses aux questions:

`python test_electoral.py 'adddadadaddaadaaaddddaaddadaadaddaa'`

Avec
a: agree (D'accord)
A: Agree (D'accord) avec Boost
d: disagree (Pas d'accord)
D: Disagree (Pas d'accord) avec Boost
u: undecided (Indécis)
U: Undecided (Indécis) avec Boost

Pour voir comment utiliser le code de calcul des scores dans un script ou dans le REPL:

`python -m doctest -v test_electoral.py`

Pour regénérer les tables des données (prend quelques secondes):

`python create_data_tables.py`

Le code pour générer les figures se trouve dans `analyse.qmd`

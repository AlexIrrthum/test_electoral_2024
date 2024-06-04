Données et code pour l'analyse du [Test électoral 2024 RTBF](https://www.rtbf.be/test-electoral)

Pour calculer les scores des partis pour une liste de 35 réponses aux questions:

`python test_electoral.py 'adddadadaddaadaaaddddaaddadaadaddaa'`

Avec
* a: agree (D'accord)
* A: Agree (D'accord) avec Boost
* d: disagree (Pas d'accord)
* D: Disagree (Pas d'accord) avec Boost
* u: undecided (Indécis)
* U: Undecided (Indécis) avec Boost

Pour voir comment utiliser le code dans un script ou le REPL, voir docstring dans `test_electoral.py`

Pour vérifier que le code de calcul donne les résultats attendus:

`python -m doctest -v test_electoral.py`

Pour regénérer les tables des données (prend quelques secondes):

`python create_data_tables.py`

Pour regénérer la table des fréquences des mots-clés dans les pages des programmes:

`python keyword_counter.py > data/keyword_counts.csv`

Le code quarto/R pour générer les figures des posts X/Twitter se trouve dans `analyse.qmd`

Le code quarto/R pour générer la [page web de l'analyse critique du Test Electoral](https://alexirrthum.quarto.pub/une-critique-du-test-electoral-rtbf-2024/) est dans `test_electoral_2024_blogpost.qmd`

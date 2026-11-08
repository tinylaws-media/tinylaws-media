"""Official Naruto databook battle stats (8 parameters, each out of 5, total out of 40).

Format: DATABOOK[char_id] = [(book_number, total, [nin, tai, gen, int, str, spd, sta, seals]), ...]
book 1 = Hiden Rin no Sho (2002), 2 = Hiden To no Sho (2005), 3 = Hiden Sha no Sho (2008).
The 4th databook (Hiden Jin no Sho, 2014) prints no stat tables: no page read showed a
"Fourth" row, and pages citing it (e.g. Shisui, Torune) give no stats.
The total is the one printed on the page, even where it differs from the sum (flagged below).

Sources (read with WebFetch, 2026-11-08):
  English Narutopedia, https://naruto.fandom.com/wiki/<Page>, used for kakashi, sasuke,
    zabuza, haku, sakura, gai (Might_Guy), neji, shikamaru, asuma, kurenai, kankuro, kabuto,
    orochimaru, tsunade, hiruzen, sasori, hidan, kakuzu, obito, sai, kimimaro, jirobo,
    sakon (Sakon_and_Ukon), tayuya, zaku, hiashi.
  French Narutopedia, https://naruto.fandom.com/fr/wiki/<Page>, used where the English page
    would not load: naruto, itachi (Itachi_Uchiwa), rock_lee, gaara, temari, kiba, shino,
    chiyo, deidara, yamato, dosu, shizune, anko, hayate, kidomaru.
  Portuguese Narutopedia, https://naruto.fandom.com/pt-br/wiki/Jiraiya, used for jiraiya.

Oddities:
  - gaara book 3: page total 29, but the stats sum to 29.5.
  - temari book 1: page total 19, but the stats sum to 18.5.
  - sakon: the page has two unlabeled book-2 tables. The first (25) is probably Sakon
    and the second (24.5) probably Ukon, judging by the description.
  - obito: rated only in book 2, as a child (Kakashi Gaiden), not as the adult.
  - hiruzen: rated in books 1 and 2 (dead before book 2). Sasori, Chiyo, Kakuzu, Hidan,
    Deidara and Jiraiya are rated in book 3 at the time of their fights/deaths.
  - itachi, orochimaru, tsunade, jiraiya: the pages read show only a book-3 row.
  - tenten: German Narutopedia (de) shows a "Parameter" table naming no databook
    (3, 3.5, 1.5, 3.5, 1.5, 3.5, 2, 2 = 20.5). It is not used here.

Checked, no stats table on the page: minato, nagato, konan, danzo, suigetsu, karin, jugo,
  kin, misumi, killer_b, konohamaru, yugito, rasa, gozu, hashirama, tobirama, hanzo, kushina,
  kurama, yahiko, kakko, onoki, darui, ao, chojuro, mifune, mu, toneri, izuna, shisui,
  torune, kazekage3, izumo, kotetsu.
Could not be read (fetch errors on every language version tried): hinata, tenten, ino,
  choji, kisame, madara, baki, mizuki, yoroi, fu_root, meizu, a4, mei, kaguya, kinkaku,
  gengetsu, kurotsuchi.
Not fetched; they first appeared after the 3rd databook, so no stats are expected:
  hagoromo, hamura, indra, asura, butsuma, tajima, ginkaku, raikage3, taiseki, kumo_chef.
Skipped: the GENERIC group entries, and the Boruto-era characters (no Boruto book uses the
  8-stat tables).
"""

DATABOOK = {
    "naruto": [
        (1, 14.5, [2, 1.5, 1, 1, 2, 2, 4, 1]),
        (2, 18.5, [3, 2, 1, 1.5, 3, 3, 4, 1]),
        (3, 26, [4, 3.5, 2, 3, 3.5, 3.5, 5, 1.5]),
    ],
    "sasuke": [
        (1, 18.5, [2.5, 2.5, 1.5, 2, 2, 3, 2, 3]),
        (2, 22.5, [3.5, 2.5, 1.5, 2.5, 3, 3.5, 3, 3]),
        (3, 31.5, [5, 3.5, 4, 3.5, 3.5, 4.5, 3.5, 4]),
    ],
    "sakura": [
        (1, 15.5, [1.5, 1, 3, 3.5, 0.5, 1, 1, 4]),
        (2, 18, [2, 1, 3.5, 4, 1, 1, 1.5, 4]),
        (3, 26, [3, 3, 3.5, 4, 3, 3, 2.5, 4]),
    ],
    "kakashi": [
        (1, 33, [5, 4, 4, 4.5, 3.5, 4, 3, 5]),
        (2, 34.5, [5, 4.5, 4, 5, 3.5, 4.5, 3, 5]),
        (3, 34.5, [5, 4.5, 4, 5, 3.5, 4.5, 3, 5]),
    ],
    "rock_lee": [
        (1, 17, [0.5, 3.5, 0.5, 1.5, 3, 4, 3, 1]),
        (2, 18, [0.5, 4, 0.5, 1.5, 3.5, 4, 3, 1]),
        (3, 22, [0.5, 5, 1, 2, 4.5, 4.5, 3.5, 1]),
    ],
    "gai": [
        (1, 31.5, [3, 5, 3, 3, 5, 5, 5, 2.5]),
        (2, 31.5, [3, 5, 3, 3, 5, 5, 5, 2.5]),
        (3, 31.5, [3, 5, 3, 3, 5, 5, 5, 2.5]),
    ],
    "neji": [
        (1, 21, [2.5, 3.5, 2, 2.5, 2.5, 3, 2, 3]),
        (2, 25, [3.5, 4.5, 2, 3, 2.5, 4, 2.5, 3]),
        (3, 27, [4, 4.5, 2, 3, 2.5, 4.5, 3.5, 3]),
    ],
    "shikamaru": [
        (1, 19, [2.5, 1.5, 2.5, 5, 1.5, 2, 1.5, 2.5]),
        (2, 21.5, [3, 1.5, 3, 5, 2, 2.5, 2, 2.5]),
        (3, 24, [3.5, 2, 3, 5, 2, 2.5, 3, 3]),
    ],
    "kiba": [
        (1, 14.5, [1.5, 2.5, 0.5, 1, 2.5, 3.5, 1.5, 1.5]),
        (2, 17.5, [2.5, 2.5, 0.5, 1.5, 3, 4, 2, 1.5]),
        (3, 22, [3.5, 3, 2, 2, 3, 4.5, 2.5, 1.5]),
    ],
    "shino": [
        (1, 17, [3.5, 1.5, 2, 3, 1.5, 1.5, 2, 2]),
        (2, 18.5, [3.5, 1.5, 2, 3.5, 1.5, 2, 2.5, 2]),
        (3, 21, [4, 1.5, 2, 4, 1.5, 3, 3, 2]),
    ],
    "asuma": [
        (1, 31.5, [4.5, 4, 3.5, 4, 4, 4.5, 3.5, 3.5]),
        (2, 32.5, [4.5, 4.5, 3.5, 4.5, 4, 4.5, 3.5, 3.5]),
        (3, 32.5, [4.5, 4.5, 3.5, 4.5, 4, 4.5, 3.5, 3.5]),
    ],
    "kurenai": [
        (1, 29, [3.5, 4, 5, 4, 2, 4, 2, 4.5]),
        (2, 29.5, [4, 4, 5, 4, 2, 4, 2, 4.5]),
        (3, 29.5, [4, 4, 5, 4, 2, 4, 2, 4.5]),
    ],
    "gaara": [
        (1, 20, [3.5, 1, 2.5, 2.5, 1, 2, 4, 3.5]),
        (2, 26.5, [4.5, 2, 2.5, 3.5, 2, 3, 5, 4]),
        (3, 29, [5, 2, 3.5, 4, 3, 3, 5, 4]),  # page total 29; stats sum to 29.5
    ],
    "kankuro": [
        (1, 19, [3.5, 1.5, 1.5, 2, 2.5, 2, 2.5, 3.5]),
        (2, 24.5, [4, 2.5, 2, 3.5, 3, 2, 3.5, 4]),
        (3, 26.5, [4, 3, 2, 3.5, 3.5, 2.5, 4, 4]),
    ],
    "temari": [
        (1, 19, [3, 2.5, 1.5, 2.5, 3, 2, 2, 2]),  # page total 19; stats sum to 18.5
        (2, 23, [4, 2.5, 1.5, 3.5, 3.5, 2.5, 2.5, 3]),
        (3, 24.5, [4, 2.5, 1.5, 4, 3.5, 3, 3, 3]),
    ],
    "kabuto": [
        (1, 30, [4, 2.5, 4.5, 5, 3, 3.5, 3, 4.5]),
        (2, 32, [4.5, 3.5, 4.5, 5, 3, 3.5, 3, 5]),
        (3, 32, [4.5, 3.5, 4.5, 5, 3, 3.5, 3, 5]),
    ],
    "hiruzen": [
        (1, 34, [5, 5, 5, 5, 3, 3, 3, 5]),
        (2, 34, [5, 5, 5, 5, 3, 3, 3, 5]),
    ],
    "hiashi": [
        (1, 29.5, [3.5, 4.5, 2, 3, 3.5, 4, 4, 5]),
        (2, 30, [3.5, 5, 2, 3, 3.5, 4, 4, 5]),
    ],
    "zabuza": [(1, 30.5, [4.5, 4.5, 2.5, 3, 4, 4, 4, 4])],
    "haku": [(1, 21, [3.5, 1, 1, 4, 1.5, 4, 2, 4])],
    "zaku": [(1, 14, [3.5, 2, 2, 1, 1, 2.5, 1, 1])],
    "dosu": [(1, 16, [2.5, 2, 1.5, 2.5, 1.5, 3, 2, 1])],
    "anko": [(1, 25, [3.5, 2.5, 4, 2, 3, 3, 4, 3])],
    "hayate": [(1, 24.5, [4, 3, 3.5, 3.5, 2, 3, 2, 3.5])],
    "obito": [(2, 18, [3, 2, 1.5, 1, 2, 3, 2.5, 3])],  # child Obito (Kakashi Gaiden)
    "kimimaro": [(2, 30.5, [4, 5, 3, 3.5, 3, 4.5, 4.5, 3])],
    "jirobo": [(2, 23.5, [3, 4, 1, 2.5, 5, 2, 4, 2])],
    "kidomaru": [(2, 25, [4, 2.5, 1.5, 4, 2, 3, 4, 4])],
    "tayuya": [(2, 24.5, [3, 2, 5, 3.5, 1, 3, 3, 4])],
    # Two book-2 tables, not labeled on the page: probably Sakon first, Ukon second.
    "sakon": [
        (2, 25, [4, 3, 1, 2.5, 3.5, 3, 4, 4]),
        (2, 24.5, [5, 3, 1, 3.5, 3, 3, 2, 4]),
    ],
    "shizune": [(2, 29.5, [4.5, 2, 4, 4.5, 2.5, 4, 3, 5])],
    "itachi": [(3, 35.5, [5, 4.5, 5, 5, 3.5, 5, 2.5, 5])],
    "orochimaru": [(3, 35, [5, 3.5, 5, 5, 3.5, 4.5, 3.5, 5])],
    "tsunade": [(3, 35, [5, 5, 3.5, 5, 5, 3.5, 4, 4])],
    "jiraiya": [(3, 35.5, [5, 4.5, 3, 4.5, 4.5, 4.5, 5, 4.5])],
    "sasori": [(3, 34.5, [5, 4, 4, 5, 3, 4.5, 5, 4])],
    "chiyo": [(3, 32, [5, 4.5, 3.5, 5, 3.5, 4, 2, 4.5])],
    "deidara": [(3, 32, [5, 3.5, 3.5, 4.5, 3.5, 4.5, 4, 3.5])],
    "kakuzu": [(3, 32.5, [5, 4, 3, 4.5, 4, 4, 4.5, 3.5])],
    "hidan": [(3, 31.5, [5, 4.5, 3, 3, 4, 3.5, 5, 3.5])],
    "yamato": [(3, 31, [4.5, 4, 3.5, 4.5, 3.5, 4, 3.5, 3.5])],
    "sai": [(3, 27.5, [4, 3.5, 3, 3.5, 3, 3.5, 3, 4])],
}

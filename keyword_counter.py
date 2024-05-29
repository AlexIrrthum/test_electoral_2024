# Script to tabulate the frequencies of keywords in the party programs (PDFs)
# The party programs are in the electoral_programs/ directory
# Note that the program from Défi comes in 5 parts that have been fused
# Note also that we've left PTB out as they don't provide a program PDF
import re
import pymupdf

programs = {
        'PS': 'electoral_programs/Programme_PS.pdf',
        'Ecolo': 'electoral_programs/Programme_Ecolo.pdf',
        'Defi': 'electoral_programs/Programme_Defi.pdf',
        'Engages': 'electoral_programs/Programme_Engages.pdf',
        'MR': 'electoral_programs/Programme_MR.pdf'
}

keyword_file = "data/police_justice_keywords.txt"

keywords = set()
counts_by_page = {
        'PS': [],
        'Ecolo': [],
        'Defi': [],
        'Engages': [],
        'MR': []
}

if __name__ == "__main__":
    with open(keyword_file, 'r') as f:
        for line in f:
            # ignore comment lines
            if line.startswith("#"):
                continue
            line = line.strip()
            keywords.add(line)
    for (party, program_file) in programs.items():
        doc = pymupdf.open(program_file)
        for page in doc:
            keyword_count = 0
            word_count = 0
            text = page.get_text()
            for w in re.findall(r"\w+", text):
                word_count += 1
                w = w.lower()
                if w in keywords:
                    keyword_count += 1
            counts_by_page[party].append((keyword_count, word_count))
        doc.close()
    print("party,page,kw_count,word_count")
    for (party, counts) in counts_by_page.items():
        for i, count in enumerate(counts):
            print(party + ',' + str(i+1) + ',' + str(count[0]) + ',' + str(count[1]))


from classes.word_token import WordToken
from classes.word_occurrence import WordOccurrence
from classes.book import Book

from services.database import DatabaseService
from services.junk import JunkService
db = DatabaseService.get_instance()
db.set_db_path("../../data/db_prod.sqlite")
js = JunkService.get_instance()

if __name__ == '__main__':
    with open("../../data/tsv/000.tsv", "r", encoding="utf8") as f:
        data = f.read()
        data = data.split("\n")
        data = [l.strip().split("\t") for l in data if data != ""]

    book_file = data[0][0]
    book = [book for book in Book.from_db_fetch_all() if book.file == book_file][0]

    to_learn = []
    for entry in data:
        word_token = WordToken(entry[3], stem=entry[4])
        if len(entry) == 6:      # To learn
            word_token.definitions = entry[5]
            word_token.persist()

            word_occurrence = WordOccurrence(
                token_id=word_token.id,
                book_id=book.id,
                line_id=int(entry[1])
            )
            word_occurrence.__book_line=entry[2]
            to_learn.append(word_occurrence)
        elif len(entry) == 5:    # Junk
            js.append(word_token)

    # Write to to_learn
    tsv_content = "\n".join([
        "\t".join([occ.__book_line, occ.token.token, occ.token.definitions])
        for occ in to_learn
    ])
    with open("../../data/tsv/to_learn.tsv", "w", encoding="utf8") as f:
        f.write(tsv_content)

    print("to_learn.tsv written")
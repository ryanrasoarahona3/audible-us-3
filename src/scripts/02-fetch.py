
from classes.book import Book
from classes.extract import Extract
from services.database import DatabaseService

db = DatabaseService.get_instance()
db.set_db_path("../../data/db_prod.sqlite")


def review_1():
    powersat_book = Book.from_db_fetch_all()
    powersat_book = [b for b in powersat_book if "powersat" in b.file][0]
    powersat_book.load_content() # load content
    book_lines = powersat_book.content.split("\n")

    # Empty word_token
    db.get_cursor().execute("DELETE FROM word_token")
    # Empty extract
    db.get_cursor().execute("DELETE FROM extract")
    extract = Extract(
        book_id=powersat_book.id,
        line_from=914,
        line_to=919
    )
    extract.persist()

    occurrences = extract.word_occurrences
    # For each occurence,
    tsv_lines = []
    for occurrence in occurrences:
        occurrence.token
        tsv_lines.append([
            powersat_book.file,
            str(occurrence.line_id),
            book_lines[occurrence.line_id],
            occurrence.token.token,
            occurrence.token.stem
        ])
    tsv_content = "\n".join(["\t".join(l) for l in tsv_lines])
    with open("../../data/tsv/000.tsv", "w", encoding="utf8") as f:
        f.write(tsv_content)
    print("TSV Written, please fill it inside ms excel")


if __name__ == '__main__':
    review_1()
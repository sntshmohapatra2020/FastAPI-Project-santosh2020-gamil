from fastapi import FastAPI, Body

app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]

@app.get("/books")
async def get_all_books():
    return BOOKS 

@app.post("/books/create_book")
async def create_book(new_book=Body()):
    BOOKS.append(new_book)
    
@app.put("/books/update_book")
async def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == updated_book["title"].casefold():
            BOOKS[i] = updated_book
    return updated_book

@app.delete("/books/delete_book/{title}")
async def delete_book(title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("title").casefold() == title.casefold():
            BOOKS.pop(i)
            break
@app.get("/books/byauthor/{author}")
async def get_book_by_author(author):
    returned_books = []
    for book in BOOKS:
        if author.casefold() == book.get("author").casefold():
            returned_books.append(book)
    return returned_books
        
@app.get("/books/{title}")
async def get_book_by_title(title):
    for book in BOOKS:
        if title.casefold() == book.get("title").casefold():
            return book

@app.get("/books/")
async def get_book_by_category(category: str):
    books_to_be_returned = []
    for book in BOOKS:
        if category.casefold() == book.get("category").casefold():
            books_to_be_returned.append(book)
    return books_to_be_returned

@app.get("/books/{author}/")
async def get_book_by_category(author: str, category: str):
    books_to_be_returned = []
    for book in BOOKS:
        if category.casefold() == book.get("category").casefold()\
            and author.casefold() == book.get("author").casefold():
            books_to_be_returned.append(book)
    return books_to_be_returned


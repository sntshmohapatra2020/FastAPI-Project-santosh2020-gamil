from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

app = FastAPI()

class Book:
    id : Optional[int] = None
    title : str
    author : str
    category  : str
    rating : int
    published_year : int
    
    def __init__(self,id, title, author, category, rating, published_year):
        self.id = id
        self.title = title
        self.author = author
        self.category = category
        self.rating = rating
        self.published_year = published_year
        
class BookRequest(BaseModel):
    id : Optional[int] = Field(description="Id is not needed", default=None)
    title : str = Field(min_length=1)
    author : str = Field(min_length=3)
    category  : str = Field(min_length=1)
    rating : int = Field(gt=-1, lt=6)
    published_year : int
'''
    model_config = {
        "json_schema_extra":{
            "example":{
                "title": "Play with Python",
                "author": "Santosh Mohapatra",
                "category": "Computer Science",
                "rating": 5,
                "published_year": 2026
            }
        }
    }'''

book_list = [
    Book(1, 'Title 1', 'Author 1', 'Book Description', 5, 2030),
    Book(2, 'Title 2', 'Author 2', 'Book Description', 5, 2030),
    Book(3, 'Title 3', 'Author 3', 'Book Description', 5, 2029),
    Book(4, 'Title 4', 'Author 4', 'Book Description', 2, 2028),
    Book(5, 'Title 5', 'Author 5', 'Book Description', 3, 2027),
    Book(6, 'Title 6', 'Author 6', 'Book Description', 1, 2026)
]

@app.get('/books', status_code=status.HTTP_200_OK)
async def get_all_books():
    return book_list

@app.post('/books/create-book',  status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookRequest):
    book = Book(**new_book.model_dump())
    book_list.append(find_id(book))

def find_id(book: Book):
    book.id = 1 if len(book_list)==0 else book_list[-1].id + 1
    return book

@app.get("/book/filter-by-rating/", status_code=status.HTTP_200_OK)
async def get_book_by_id(rating: int):
    rating_book_list = []
    for book in book_list:
        if rating == book.rating:
            rating_book_list.append(book)
    return rating_book_list

@app.get("/book/filter-by-published-year/", status_code=status.HTTP_200_OK)
async def get_book_by_published_year(published_year: int = Query(lt=2040)):
    published_year_list = []
    for book in book_list:
        if published_year == book.published_year:
            published_year_list.append(book)
    return published_year_list

@app.put("/book/update-book", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(book_list)):
        if book_list[i].id == book.id:
            book_list[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail=f"The book with {book.id} ia not found")
@app.delete("/book/delete-book/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_by_id(book_id: int = Path(gt=0)):
    book_found = False
    for i, book in enumerate(book_list):
        if book_id == book.id:
            book_found = True
            book_list.pop(i)
            break
    if not book_found:
        raise HTTPException(status_code=404, detail=f"The book with {book_id} is not found")
@app.get("/book/{book_id}", status_code=status.HTTP_200_OK)
async def get_book_by_id(book_id: int = Path(gt=0)):
    for book in book_list:
        if book_id == book.id:
            return book
    return HTTPException(status_code=404, detail=f"book with {book_id} is not found")
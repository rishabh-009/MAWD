'''
1. b) sqlite3
2. b) conn.commit()
3. b) 2
4. c) None
5. c) 5
6. b) uvicorn main:app --reload
7. c) /doc
8. b) POST
9. d) 422
10.c) 303

'''


import sqlite3

con = sqlite3.Connection("HEHE.db")

cur = con.cursor()

from fastapi import FastAPI

app = FastAPI()

# Question B1
def marksscoredabove_80():
        cursor = con.execute("SELECT name, marks FROM students WHERE marks > ? ORDER BY marks DESC", (80,))
        results = cursor.fetchall()
        for row in results:
            print(f"Name -> {row[0]}, Marks -> {row[1]}")

# Question B2

def add_student(name, course, city, marks):
    con.execute("INSERT INTO students (name, course, city, marks) VALUES (?, ?, ?, ?)", (name, course, city, marks))
    con.commit()

add_student("Vikram", "BCA", "Udaipur", 67)
marksscoredabove_80()
# Vikram will get the id 6


# Question B3
'''
CRUD is the shortform for Create, Read, Update and Delete. It is the operations that can be performed by APIs in the backend or database. The SQL command and HTTPS methods for each is as follows: 
C - Create, SQL: INSERT, HTTP: POST
R - Read, SQL: SELECT, HTTPS: GET
U - Update, SQL: UPDATE, HTTPS: PUT
D - Delete, SQL DELETE and DROP, HTTP: DELETE

'''


#Question B4
@app.get("/hello/{name}")
def greet(name:str):
     return{"message":f"hello {name}"}

#Question B5
@app.get("/students/{student_id}")
def get_student(student_id:int):
    con = get_connection()
    row = con.execute("SELECT * FROM students WHERE id = ?", (student_id,)).fetchone()
    con.close()
    if row is None:
         return {"error": "student not found"}
    return dict(zip(("id", "name", "course", "city", "marks"), row))


# Question C1

import sqlite3


con = sqlite3.Connection("library.db")
cur = con.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT NOT NULL,author TEXT,price REAL)""")

books = [("Python basics", "Rao", 250),("SQL guide", "Mehta", 180),("Web Dev", "Khan", 400)]

cur.executemany("INSERT INTO books (title, author, price) VALUES (?, ?, ?)",books)
con.commit()



cur.execute("UPDATE books SET price = price * 1.10")
print(f"Rows updated: {cur.rowcount}")
con.commit()



cur.execute("DELETE FROM books WHERE price < 200")
con.commit()

cur.execute("SELECT id, title, author, ROUND(price, 2) FROM books ORDER BY id")

remaining_books = cur.fetchall()

print("Remaining books:")
for book in remaining_books:

    print(book)

con.close()

# Question C2


import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

con = sqlite3.Connection("shop.db")
cur = con.cursor()


class Book(BaseModel):
    title: str
    author: str
    price: float


cur.execute("""CREATE TABLE IF NOT EXISTS books (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    price REAL NOT NULL
)""")
con.commit()


def find_book(book_id):
    cur.execute("SELECT * FROM books WHERE id = ?", (book_id,))
    book = cur.fetchone()
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return dict(zip(("id", "title", "author", "price"), book))


@app.post("/books", status_code=201)
def add_book(book: Book):
    cur.execute(
        "INSERT INTO books (title, author, price) VALUES (?, ?, ?)",
        (book.title, book.author, book.price)
    )
    con.commit()
    return find_book(cur.lastrowid)


@app.get("/books")
def get_books():
    cur.execute("SELECT * FROM books ORDER BY id")
    rows = cur.fetchall()
    return [dict(zip(("id", "title", "author", "price"), row)) for row in rows]


@app.get("/books/{book_id}")
def get_book(book_id: int):
    return find_book(book_id)


@app.put("/books/{book_id}")
def update_book(book_id: int, book: Book):
    cur.execute(
        "UPDATE books SET title = ?, author = ?, price = ? WHERE id = ?",
        (book.title, book.author, book.price, book_id)
    )
    con.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")
    return find_book(book_id)


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    cur.execute("DELETE FROM books WHERE id = ?", (book_id,))
    con.commit()
    if cur.rowcount == 0:
        raise HTTPException(status_code=404, detail="Book not found")

    return {"message": "Book deleted successfully"}

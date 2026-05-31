'''
Build a library management system

Add book -> title, author, isbn and number of copies
Borrow book -> member_id, isbn
return_book -> member id, isbn
get book info


implement a reservation system (member_id, isbn)

if book does not exist, false
if copies are available, reservation should fail and just execute borrow directly
member cannot reserve the same book twice
a member cant reserve a book they have already borrowed
reservations should be in a first in first out format
'''
from collections import defaultdict, deque

class Book:
    def __init__(self, title: str, author: str, isbn: int, num_copies: int):
        self._title = title
        self._author = author
        self._isbn = isbn
        self._num_copies = num_copies

    @property
    def title(self) -> str:
        return self._title

    @property
    def author(self) -> str:
        return self._author

    @property
    def isbn(self) -> int:
        return self._isbn

    @property
    def num_copies(self) -> int:
        return self._num_copies

    @num_copies.setter
    def num_copies(self, value: int):
        if value < 0:
            raise ValueError("Number of copies cannot be below 0")
        self._num_copies = value

    def __repr__(self) -> str:
        return (f"Title: {self._title}, Author: {self._author}, "
                f"ISBN: {self._isbn}, Copies: {self._num_copies}")


class LibraryManagement:
    def __init__(self):
        self._books: dict[int, Book] = {}
        self._borrowed: dict[int, set[int]] = defaultdict(set)
        self._reservations: dict[int, deque[int]] = {}       # isbn → queue of member_ids
        self._member_reservations: dict[int, set[int]] = {} # member_id → set of reserved isbns

    def add_book(self, title: str, author: str, isbn: int, copies: int) -> bool:
        if isbn in self._books:
            return False
        self._books[isbn] = Book(title, author, isbn, copies)
        return True

    def borrow_book(self, member_id: int, isbn: int) -> bool:
        if isbn not in self._books:
            return False
        if isbn in self._borrowed[member_id]:
            return False
        book = self._books[isbn]
        if book.num_copies == 0:
            return False
        self._borrowed[member_id].add(isbn)
        book.num_copies -= 1
        return True

    def return_book(self, member_id: int, isbn: int) -> bool:
        if member_id not in self._borrowed or isbn not in self._borrowed[member_id]:
            return False
        self._borrowed[member_id].remove(isbn)
        self._books[isbn].num_copies += 1
        self._implement_reservation(isbn)
        return True

    def get_book_info(self, isbn: int) -> str:
        if isbn not in self._books:
            return "Book not found"
        return repr(self._books[isbn])
    
    def reserve_book(self, member_id: int, isbn: int) -> bool:
        if isbn not in self._books:
            return False
        if self._books[isbn].num_copies > 0:
            return self.borrow_book(member_id, isbn)
        if isbn in self._borrowed[member_id]:
            return False
        if isbn in self._member_reservations.get(member_id, set()):
            return False
        self._reservations.setdefault(isbn, deque()).append(member_id)
        self._member_reservations.setdefault(member_id, set()).add(isbn)
        return True

    def _implement_reservation(self, isbn: int) -> None:
        if isbn not in self._reservations or not self._reservations[isbn]:
            return
        member_id = self._reservations[isbn].popleft()
        self._member_reservations[member_id].discard(isbn)
        self.borrow_book(member_id, isbn)
    

lib = LibraryManagement()
print(lib.add_book('OS','abc',1,2))
print(lib.get_book_info(1))
print(lib.borrow_book(1,1))
print(lib.borrow_book(2,1))
print(lib.borrow_book(3,1))
print(lib.borrow_book(1,1))
print(lib.get_book_info(1))
print(lib.return_book(1,1))
print(lib.get_book_info(1))


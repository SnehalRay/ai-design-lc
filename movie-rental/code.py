'''
You have a movie renting company consisting of n shops. You want to implement a renting system that supports searching for, booking, and returning movies. The system should also support generating a report of the currently rented movies.

Each movie is given as a 2D integer array entries where entries[i] = [shopi, moviei, pricei] indicates that there is a copy of movie moviei at shop shopi with a rental price of pricei. Each shop carries at most one copy of a movie moviei.

The system should support the following functions:

Search: Finds the cheapest 5 shops that have an unrented copy of a given movie. The shops should be sorted by price in ascending order, and in case of a tie, the one with the smaller shopi should appear first. If there are less than 5 matching shops, then all of them should be returned. If no shop has an unrented copy, then an empty list should be returned.
Rent: Rents an unrented copy of a given movie from a given shop.
Drop: Drops off a previously rented copy of a given movie at a given shop.
Report: Returns the cheapest 5 rented movies (possibly of the same movie ID) as a 2D list res where res[j] = [shopj, moviej] describes that the jth cheapest rented movie moviej was rented from the shop shopj. The movies in res should be sorted by price in ascending order, and in case of a tie, the one with the smaller shopj should appear first, and if there is still tie, the one with the smaller moviej should appear first. If there are fewer than 5 rented movies, then all of them should be returned. If no movies are currently being rented, then an empty list should be returned.
Implement the MovieRentingSystem class:

MovieRentingSystem(int n, int[][] entries) Initializes the MovieRentingSystem object with n shops and the movies in entries.
List<Integer> search(int movie) Returns a list of shops that have an unrented copy of the given movie as described above.
void rent(int shop, int movie) Rents the given movie from the given shop.
void drop(int shop, int movie) Drops off a previously rented movie at the given shop.
List<List<Integer>> report() Returns a list of cheapest rented movies as described above.




company -> n shops
search, book, return, get how many rented
movie: shop idx, movie index and prices idx

{movie i: {shop i: pricei}}
'''
from sortedcontainers import SortedList

class MovieRentingCompany:

    def __init__(self, entries: list):
        self.store_record = {}          # {movie: {shop: price}}
        self.available = {}             # {movie: SortedList[(price, shop)]}
        self.rented = SortedList()      # [(price, shop, movie)]

        for shop, movie, price in entries:
            if movie not in self.store_record:
                self.store_record[movie] = {}
                self.available[movie] = SortedList()
            self.store_record[movie][shop] = price
            self.available[movie].add((price, shop))

    def search(self, movie: int) -> list:
        if movie not in self.available:
            return []
        return [shop for price, shop in self.available[movie][:5]]

    def rent(self, shop: int, movie: int) -> None:
        if movie not in self.store_record or shop not in self.store_record[movie]:
            return
        price = self.store_record[movie][shop]
        self.available[movie].remove((price, shop))
        self.rented.add((price, shop, movie))

    def drop(self, shop: int, movie: int) -> None:
        if movie not in self.store_record or shop not in self.store_record[movie]:
            return
        price = self.store_record[movie][shop]
        self.rented.remove((price, shop, movie))
        self.available[movie].add((price, shop))

    def report(self) -> list:
        return [[shop, movie] for price, shop, movie in self.rented[:5]]


if __name__ == "__main__":
    entries = [
        [0, 1, 5],
        [0, 2, 8],
        [1, 1, 3],
        [1, 2, 6],
        [2, 1, 10],
        [2, 2, 4],
    ]
    system = MovieRentingCompany(entries)

    print("search(1):", system.search(1))   # shops with movie 1, sorted by price: [1(3), 0(5), 2(10)]
    print("search(2):", system.search(2))   # shops with movie 2, sorted by price: [2(4), 1(6), 0(8)]

    system.rent(1, 1)
    system.rent(2, 2)
    print("\nafter renting (shop=1, movie=1) and (shop=2, movie=2):")
    print("search(1):", system.search(1))   # shop 1 rented out, expect [0, 2]
    print("report():", system.report())     # cheapest rented: (3,1,1) and (4,2,2)

    system.rent(0, 1)
    print("\nafter renting (shop=0, movie=1):")
    print("report():", system.report())     # 3 rented movies now

    system.drop(1, 1)
    print("\nafter dropping (shop=1, movie=1):")
    print("search(1):", system.search(1))   
    print("report():", system.report()) 

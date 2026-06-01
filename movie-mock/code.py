'''
Movie renting company
implementing a renting system
=> searching movies, booking movies and returning movies and generate movies
=> add movies
=> add stores

Movie object needs name of the movie and the price and the store it is linked to?
'''


class Movie:
    def __init__(self, name: str, price: float, store_id: int, qty:int):
        self._name = name
        self._price = 0.0
        self._store_id = 0
        self.__qty = 0
        self.price = price
        self.store_id = store_id
        self.qty = qty

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            raise ValueError("Price cannot be negative")
        self._price = float(value)

    @property
    def qty(self) -> int:
        return self.__qty

    @qty.setter
    def qty(self, value: int):
        if value < 0:
            raise ValueError("Quantity cannot be negative")
        self.__qty = int(value)

    @property
    def store_id(self) -> int:
        return self._store_id

    @store_id.setter
    def store_id(self, value: int):
        self._store_id = int(value)

class MovieRentalSystem:
    def __init__(self):
        self._stores: set[int] = set()
        self._movies: dict[str, dict[int, Movie]] = {}
        self._user_rented: dict[int, dict[str, Movie]] = {}

    def add_movie(self, movie: str, store_id: int, price: float, quantity: int) -> bool:
        if store_id not in self._stores:
            return False
        if movie in self._movies and store_id in self._movies[movie]:
            self._movies[movie][store_id].qty += quantity
        else:
            self._movies.setdefault(movie, {})[store_id] = Movie(movie, price, store_id, quantity)
        return True

    def add_stores(self, store_id: int) -> bool:
        if store_id in self._stores:
            return False
        self._stores.add(store_id)
        return True

    def search_movies(self, movie: str) -> list:
        '''
        returns top 5 store id with the cheapest layer of movies
        '''
        if movie not in self._movies:
            return []
        results = sorted(self._movies[movie].values(), key=lambda m: m.price)
        return results[:5]

    def rent_movie(self, movie: str, store_id: int, userId: int) -> None:
        user_movies = self._user_rented.setdefault(userId, {})
        if movie in user_movies:
            return
        if movie not in self._movies or store_id not in self._movies[movie]:
            return
        m = self._movies[movie][store_id]
        if m.qty == 0:
            return
        m.qty -= 1
        user_movies[movie] = m

    def return_movie(self, movie: str, store_id: int, userId: int) -> None:
        user_movies = self._user_rented.get(userId, {})
        if movie not in user_movies:
            return
        m = user_movies.pop(movie)
        m.qty += 1

    def report(self) -> str:
        '''
        return the top 5 cheapest rented movies with their store names
        '''
        all_movies = [m for store_map in self._movies.values() for m in store_map.values()]
        top5 = sorted(all_movies, key=lambda m: m.price)[:5]
        lines = ["Top 5 Cheapest Movies:"]
        for i, m in enumerate(top5, 1):
            lines.append(f"{i}. {m.name} @ Store {m.store_id} - ${m.price:.2f}")
        return "\n".join(lines)



if __name__ == "__main__":
    rs = MovieRentalSystem()
    rs.add_stores(1)
    rs.add_stores(2)
    rs.add_movie("Inception", 1, 2.99, 3)
    rs.add_movie("Inception", 2, 4.50, 1)
    rs.add_movie("Dunkirk", 1, 3.49, 2)
    rs.add_movie("Interstellar", 2, 1.99, 5)

    print("search 'Inception':", [(m.store_id, m.price) for m in rs.search_movies("Inception")]) #1 and 2

    rs.rent_movie("Inception", 1,1)
    rs.rent_movie("Inception", 1,2)  # no-op: already renting
    print("qty after rent:", rs._movies["Inception"][1].qty)  # 2

    print(rs.report())

    rs.return_movie("Inception", 1, 1)
    print("qty after return:", rs._movies["Inception"][1].qty)  # 3


    

'''
An underground railway system is keeping track of customer travel times between different stations. They are using this data to calculate the average time it takes to travel from one station to another.

Implement the UndergroundSystem class:

void checkIn(int id, string stationName, int t)
A customer with a card ID equal to id, checks in at the station stationName at time t.
A customer can only be checked into one place at a time.
void checkOut(int id, string stationName, int t)
A customer with a card ID equal to id, checks out from the station stationName at time t.
double getAverageTime(string startStation, string endStation)
Returns the average time it takes to travel from startStation to endStation.
The average time is computed from all the previous traveling times from startStation to endStation that happened directly, meaning a check in at startStation followed by a check out from endStation.
The time it takes to travel from startStation to endStation may be different from the time it takes to travel from endStation to startStation.
There will be at least one customer that has traveled from startStation to endStation before getAverageTime is called.
You may assume all calls to the checkIn and checkOut methods are consistent. If a customer checks in at time t1 then checks out at time t2, then t1 < t2. All events happen in chronological order.
'''

class UndergroundSystem:

    def __init__(self):
        self.entered = {} #id: (station,start Time)
        self.total_time = {} #(start station, end station) : (totalTime, length)

    def checkIn(self,id: int, stationName: str, t: int) -> None:
        self.entered[id] = (stationName, t)

    def checkOut(self,id: int, stationName: str, t: int) -> None:

        if id not in self.entered:
            raise KeyError('User never checked in')
        
        startStation, startTime = self.entered[id]
        duration = t - startTime
        route = (startStation, stationName)
        if route in self.total_time:
            totalTime, count = self.total_time[route]
            self.total_time[route] = (totalTime + duration, count + 1)
        else:
            self.total_time[route] = (duration, 1)

        

    def averageTime(self,startStation, endStation) -> float:
        #if the pair is not seen, output can be INF? or None with an error?
        if (startStation, endStation) not in self.total_time:
            return float('inf')
        total_time, total_people = self.total_time[(startStation,endStation)]
        return total_time / total_people


if __name__ == "__main__":
    system = UndergroundSystem()

    system.checkIn(1, "Leyton", 3)
    system.checkIn(2, "Waterloo", 8)
    system.checkIn(3, "Leyton", 10)

    system.checkOut(1, "Waterloo", 15)   # Leyton -> Waterloo: 12
    system.checkOut(2, "Leyton", 20)     # Waterloo -> Leyton: 12
    system.checkOut(3, "Waterloo", 22)   # Leyton -> Waterloo: 12

    print(system.averageTime("Leyton", "Waterloo"))   # (12 + 12) / 2 = 12.0

    system.checkIn(5, "Leyton", 23)
    system.checkOut(5, "Waterloo", 38)   # Leyton -> Waterloo: 15

    print(system.averageTime("Leyton", "Waterloo"))   # (12 + 12 + 15) / 3 = 13.0
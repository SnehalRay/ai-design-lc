'''
You are implementing a program to use as your calendar. We can add a new event if adding the event will not cause a double booking.

A double booking happens when two events have some non-empty intersection (i.e., some moment is common to both events.).

The event can be represented as a pair of integers startTime and endTime that represents a booking on the half-open interval [startTime, endTime), the range of real numbers x such that startTime <= x < endTime.

Implement the MyCalendar class:

MyCalendar() Initializes the calendar object.
boolean book(int startTime, int endTime) Returns true if the event can be added to the calendar successfully without causing a double booking. Otherwise, return false and do not add the event to the calendar.


#no double booking

s1,e1 and s2,e2

overlaps: false => s1<e2 and s2 < e1
s1 -- s2 --- e1 -- e2
P
true : no overlap
e1 <= s2 or e2 <= s1

s1 --- e1 --- s2 ---- e2
s2 --- e2 --- s1 ---- e1
'''

class MyCalendar:

    def __init__(self):
        self.events = []

    def book(self,startTime: int, endTime: int)->bool:
        for s, e in self.events:
            if startTime < e and s < endTime:   # overlap condition
                return False
        self.events.append((startTime, endTime))
        return True


calendar = MyCalendar()
print(calendar.book(0,2)) # true
print(calendar.book(3,5)) # true
print(calendar.book(1,2)) #false
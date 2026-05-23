'''
1472. Design Browser History


You have a browser of one tab where you start on the homepage and you can visit another url, get back in the history number of steps or move forward in the history number of steps.

Implement the BrowserHistory class:

BrowserHistory(string homepage) Initializes the object with the homepage of the browser.
void visit(string url) Visits url from the current page. It clears up all the forward history.
string back(int steps) Move steps back in history. If you can only return x steps in the history and steps > x, you will return only x steps. Return the current url after moving back in history at most steps.
string forward(int steps) Move steps forward in history. If you can only forward x steps in the history and steps > x, you will forward only x steps. Return the current url after forwarding in history at most steps.



start: homepage -> visit url
can move around

back-> no back, stay where you are
front-> no front, stay where you are at
'''

class Node:
    def __init__(self,url):
        self.next = None
        self.prev = None
        self.url = url


class BrowserHistory:

    def __init__(self):
        self.homepage = Node("home")
        self.current = self.homepage

    def visit(self,url:str) -> None:
        new_site = Node(url)
        self.current.next = new_site
        new_site.prev = self.current
        self.current = self.current.next


    def back(self, steps: int) -> str:
        while steps > 0 and self.current.prev:
            self.current = self.current.prev
            steps -= 1
        return self.current.url

    def forward(self, steps: int) -> str:
        while steps > 0 and self.current.next:
            self.current = self.current.next
            steps -= 1
        return self.current.url


if __name__ == "__main__":
    bh = BrowserHistory()

    print(f"[init]       → current: {bh.current.url}")

    for url in ["google.com", "youtube.com", "facebook.com"]:
        bh.visit(url)
        print(f"[visit]      → current: {bh.current.url}")

    print(f"[back 1]     → current: {bh.back(1)}") 
    print(f"[back 5]     → current: {bh.back(5)}")   # clamped to homepage
    print(f"[forward 1]  → current: {bh.forward(1)}")

    print(f"[back 1]     → current: {bh.current.url}")
    bh.visit("reddit.com")
    print(f"[visit]      → current: {bh.current.url}  (forward history cleared)")

    print(f"[forward 1]  → current: {bh.forward(1)}")  # no forward, stays
    print(f"[back 1]  → current: {bh.back(1)}") 

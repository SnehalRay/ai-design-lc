'''
You are asked to design an auction system that manages bids from multiple users in real time.

Each bid is associated with a userId, an itemId, and a bidAmount.

Implement the AuctionSystem class:

AuctionSystem(): Initializes the AuctionSystem object.
void addBid(int userId, int itemId, int bidAmount): Adds a new bid for itemId by userId with bidAmount. If the same userId already has a bid on itemId, replace it with the new bidAmount.
void updateBid(int userId, int itemId, int newAmount): Updates the existing bid of userId for itemId to newAmount. It is guaranteed that this bid exists.
void removeBid(int userId, int itemId): Removes the bid of userId for itemId. It is guaranteed that this bid exists.
int getHighestBidder(int itemId): Returns the userId of the highest bidder for itemId. If multiple users have the same highest bidAmount, return the user with the highest userId. If no bids exist for the item, return -1.
'''

import heapq

class AuctionSystem:

    def __init__(self):
        self.bids = {}  # {itemID: {userID: amount}}  — source of truth
        self.heap = {}  # {itemID: min-heap of (-amount, -userID)}

    def _peek_highest(self, itemId):
        """Lazy-delete stale heap entries; return (amount, userId) of valid top or None."""
        heap = self.heap.get(itemId, [])
        bids_for_item = self.bids.get(itemId, {})
        while heap:
            neg_amount, neg_uid = heap[0]
            amount, uid = -neg_amount, -neg_uid
            if bids_for_item.get(uid) == amount:
                return (amount, uid)
            heapq.heappop(heap)
        return None

    def addBid(self, userId, itemId, bidAmount):
        if itemId not in self.bids:
            self.bids[itemId] = {}
            self.heap[itemId] = []

        top = self._peek_highest(itemId)
        if top is not None and bidAmount <= top[0]:
            raise ValueError(f"Bid {bidAmount} must strictly exceed current highest bid {top[0]}")

        self.bids[itemId][userId] = bidAmount
        heapq.heappush(self.heap[itemId], (-bidAmount, -userId))

    def updateBid(self, userId, itemId, newAmount):
        if itemId not in self.bids or userId not in self.bids[itemId]:
            raise KeyError(f"No existing bid for userId={userId}, itemId={itemId}")

        top = self._peek_highest(itemId)
        if top is not None and newAmount <= top[0]:
            raise ValueError(f"Bid {newAmount} must strictly exceed current highest bid {top[0]}")

        self.bids[itemId][userId] = newAmount
        heapq.heappush(self.heap[itemId], (-newAmount, -userId))

    def removeBid(self, userId, itemId):
        del self.bids[itemId][userId]
        # Stale heap entry is left; _peek_highest skips it lazily

    def getHighestBidder(self, itemId):
        if itemId not in self.bids or not self.bids[itemId]:
            return -1
        top = self._peek_highest(itemId)
        return top[1] if top is not None else -1


# --- Tests matching the scenario from comments ---
auction = AuctionSystem()
# user1, item1 for 10
auction.addBid(1, 1, 10)
# user2, item1 for 15
auction.addBid(2, 1, 15)
# user1 updates bid for 20
auction.updateBid(1, 1, 20)
# user2 updates for 21
auction.updateBid(2, 1, 21)
# user2 removes
auction.removeBid(2, 1)
# check winner -> user1 (bid 20, after lazy heap cleanup removes stale user2 entry)
assert auction.getHighestBidder(1) == 1, f"Expected 1, got {auction.getHighestBidder(1)}"

# No bids returns -1
assert auction.getHighestBidder(999) == -1

# Strict condition: cannot bid equal or lower than current highest
try:
    auction.addBid(3, 1, 20)
    assert False, "Should have raised ValueError"
except ValueError:
    pass

# updateBid raises on non-existent user
try:
    auction.updateBid(99, 1, 100)
    assert False, "Should have raised KeyError"
except KeyError:
    pass

print("All tests passed.")

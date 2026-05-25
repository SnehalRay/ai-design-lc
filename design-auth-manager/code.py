'''
There is an authentication system that works with authentication tokens. For each session, the user will receive a new authentication token that will expire timeToLive seconds after the currentTime. If the token is renewed, the expiry time will be extended to expire timeToLive seconds after the (potentially different) currentTime.

Implement the AuthenticationManager class:

AuthenticationManager(int timeToLive) constructs the AuthenticationManager and sets the timeToLive.
generate(string tokenId, int currentTime) generates a new token with the given tokenId at the given currentTime in seconds.
renew(string tokenId, int currentTime) renews the unexpired token with the given tokenId at the given currentTime in seconds. If there are no unexpired tokens with the given tokenId, the request is ignored, and nothing happens.
countUnexpiredTokens(int currentTime) returns the number of unexpired tokens at the given currentTime.
Note that if a token expires at time t, and another action happens on time t (renew or countUnexpiredTokens), the expiration takes place before the other actions.


Authentication Manager has time to live

generate: generates a tokenId and expiry is current time + time to live
renew: only works if token is valid or exists. renews the token
count the number of unexpired tokens at a given time

'''

class AuthenticationManager:

    def __init__(self, timeToLive: int)-> int:
        self.time_to_live = timeToLive
        self.tokens = {} #tokeniD: Expiry time

    def generate(self,tokenId: str, currentTime: int)->None:
        self.tokens[tokenId] = currentTime + self.time_to_live

    def renew(self,tokenId:str, currentTime: int)->None:
        # tokens must exist and must be unexpired
        # expiry is strictly greater than current time
        # if token[x] == current time it is already expired
        if tokenId not in self.tokens:
            return
        
        if self.tokens[tokenId]<=currentTime:
            return
        
        self.tokens[tokenId] = currentTime + self.time_to_live

    def countUnexpiredTokens(self, currentTime: int)->int:
        # return sum(1 for exp in self.tokens.values() if exp >currentTime)
        res = 0
        copy = self.tokens.copy()
        for id,exp in copy.items():
            if exp<=currentTime:
                del self.tokens[id]
            else:
                res+=1
        return res



if __name__ == "__main__":
    auth = AuthenticationManager(timeToLive=5)

    # Generate two tokens at t=1
    auth.generate("aaa", 1)   # expires at 6
    auth.generate("bbb", 1)   # expires at 6
    print(f"t=1  | after generating 'aaa' and 'bbb' | tokens: {auth.tokens}")

    # Renew 'aaa' at t=3 (unexpired: 6 > 3) → new expiry = 8
    auth.renew("aaa", 3)
    print(f"t=3  | after renewing 'aaa'              | tokens: {auth.tokens}")

    # Count at t=5: 'aaa' expires 8, 'bbb' expires 6 — both unexpired
    count = auth.countUnexpiredTokens(5)
    print(f"t=5  | unexpired count = {count} (expected 2)")

    # Count at t=6: 'bbb' expires exactly at 6 → expired; 'aaa' at 8 → alive
    count = auth.countUnexpiredTokens(6)
    print(f"t=6  | unexpired count = {count} (expected 1, 'bbb' expired)")

    # Try to renew 'bbb' at t=6 (expired at 6, not strictly greater) → no-op
    auth.renew("bbb", 6)
    print(f"t=6  | after renewing expired 'bbb'      | tokens: {auth.tokens}")

    # Try to renew 'ccc' which was never generated → no-op
    auth.renew("ccc", 6)
    print(f"t=6  | after renewing non-existent 'ccc' | tokens: {auth.tokens}")

    # Count at t=9: 'aaa' expires 8, now expired; 'bbb' still expired
    count = auth.countUnexpiredTokens(9)
    print(f"t=9  | unexpired count = {count} (expected 0, all expired)")

    # Re-generate an existing expired token
    auth.generate("bbb", 9)   # expires at 14
    count = auth.countUnexpiredTokens(9)
    print(f"t=9  | after re-generating 'bbb'         | unexpired count = {count} (expected 1)")

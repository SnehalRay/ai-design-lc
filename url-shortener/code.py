import random
import string

'''
long url: anything
short url: 6 digit unique id

Shortening a long URL
Expanding a short code back to the original URL
Handling duplicate long URLs
Handling invalid short codes


add URL () -> this method adds the url and generates a short url -> returns short url
generate short url () #helper method => collision handle through while loop
long_url exists ()
short_url_exists ()
url_exists() -> runs both long and short url exist method
get_long_url(shorturl)

handle uniqueness

www.shopify.com
'''

class URLShortener:

    def __init__(self):
        self.long_to_short = {}
        self.short_to_long = {}
        self.tiny_prefix = 'https://www.tinyURL/'

    def add_URL(self, longUrl: str) -> str:
        if self.long_url_exists(longUrl):
            return self.long_to_short[longUrl]
        short_url = self._generate_short_url()
        self.long_to_short[longUrl] = short_url
        self.short_to_long[short_url] = longUrl
        return short_url

    def _generate_short_url(self) -> str:
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choices(characters, k=6))
            short_url = self.tiny_prefix + short_code
            if not self.short_url_exists(short_url):
                return short_url
            
    def long_url_exists(self, longUrl: str) -> bool:
        return longUrl in self.long_to_short

    def short_url_exists(self, short_url: str) -> bool:
        return short_url in self.short_to_long
    
    def url_exists(self,url:str)->bool:
        return self.long_url_exists(url) or self.short_url_exists(url)
    
    def get_long_url(self, shorturl: str) -> str | None:
        if shorturl in self.short_to_long:
            return self.short_to_long[shorturl]
        return None

    def get_short_url(self, longUrl: str) -> str | None:
        if longUrl in self.long_to_short:
            return self.long_to_short[longUrl]
        return None
    

if __name__ == "__main__":
    urlShortener = URLShortener()
    short = urlShortener.add_URL("www.shopify.com")
    print(urlShortener.add_URL("www.shopify.com"))
    print(urlShortener.get_long_url('dnkwjend'))


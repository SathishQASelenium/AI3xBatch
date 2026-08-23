class Browser:

    def make_http_request(self, url):
        print("Hi, Lets make the HTTP request without auth", url)

    def make_http_request(self, url, auth=None):
        print("Hi, Lets make the HTTP request with auth", url, auth)


t = Browser()
t.make_http_request("sdet.live") # url = "sdet.live" and auth = None, so it will call the second method with two parameters, and auth will take the default value of None.
t.make_http_request("google.com","admin") # url = "google.com" and auth = "admin", so it will call the second method with two parameters, and auth will take the value of "admin".
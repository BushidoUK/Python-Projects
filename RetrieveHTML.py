import requests

URL = "<ENTER URL>" # Target URL to fetch HTML from
page = requests.get(URL) # Performs HTTP GET Request

print(page.text) # Displays HTML in the Terminal

import requests

URL = "<TARGET URL>" # Target URL to fetch HTML from
page = requests.get(URL) # Performs HTTP GET Request

# Write the page content to a file called "TargetSiteHTML.txt"
with open("TargetSiteHTML.txt", "w") as file:
    file.write(page.text)

print(f"Page content saved to TargetSiteHTML.txt")

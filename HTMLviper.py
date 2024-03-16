import requests
from bs4 import BeautifulSoup

def fetch_and_save_page_content(url, element_id):
    try:
        page = requests.get(url)
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, "html.parser")
            results = soup.find(id=element_id)
            with open("TargetSiteHTML.txt", "w") as file:
                file.write(results.prettify())
            print(f"Page content saved to TargetSiteHTML.txt")
        else:
            print(f"Error fetching the page. Status code: {page.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    user_url = input("Enter the URL: ")
    user_id = input("Enter the element ID: ")
    fetch_and_save_page_content(user_url, user_id)

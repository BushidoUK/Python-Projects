import requests

def fetch_and_save_page_content(url):
    try:
        page = requests.get(url)
        if page.status_code == 200:
            with open("TargetSiteHTML.txt", "w") as file:
                file.write(page.text)
            print(f"Page content saved to TargetSiteHTML.txt")
        else:
            print(f"Error fetching the page. Status code: {page.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    user_url = input("Enter the URL: ")
    fetch_and_save_page_content(user_url)

import dotenv
import requests
import os
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

dotenv.load_dotenv()
# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def user_by_name_url(users):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=" + users
    user_fields = "user.fields=description,created_at"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url

def user_tweets_url(user_id):

    return "https://api.twitter.com/2/users/{}/tweets".format(user_id)

def tweet_params():
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    return {"tweet.fields": "created_at,text"}

def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "tw3AddressLookup"
    return r


def get_request(url, params=None):
    response = requests.request("GET", url, auth=bearer_oauth, params=params)
    # print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def get_user_ids(usernames):
    url = user_by_name_url(usernames)
    json_response = get_request(url)
    # print(json_response)
    return json_response['data'][0]['id']

def get_user_tweets(id):
    url = user_tweets_url(id)
    params = tweet_params()
    json_response = get_request(url, params)
    return json_response['data']

def get_tweet_count(username):

    url = f'https://x.com/{username}'

    options = Options()
    options.headless = True

    driver_path = '/webdriver/geckodriver.exe'
    driver = webdriver.Firefox(executable_path=driver_path, options=options)

    driver.get(url)
    
    try:
        # Wait for the script tag in the head with application/ld+json type
        script_tag = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "head script[type='application/ld+json']"))
        )
        # print("Script tag loaded in the head")

        # Now you can proceed with further actions, e.g., scraping data or interacting with elements
        # Example: Get the text content of the script tag
        script_content = script_tag.get_attribute("innerText")
        # Parse the JSON data
        data = json.loads(script_content)

        # Access the userInteractionCount for "WriteAction"
        for interaction in data["author"]["interactionStatistic"]:
            if interaction["interactionType"] == "https://schema.org/WriteAction" or interaction["name"] == "Tweets":
                tweet_count = interaction["userInteractionCount"]
                # print (f"tweet count {tweet_count}")
                return tweet_count

    except Exception as e:
        print("Error occurred while waiting for the script tag:", e)

    finally:
        # Close the WebDriver
        driver.quit()

__all__ = [
    'get_user_ids',
    'get_user_tweets'
]
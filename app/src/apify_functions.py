from apify_client import ApifyClient
import pandas as pd
import datetime

def authenticate_apify(token):
    """
    Authenticate with Apify and returns an Apify client
    :param token: Apify token
    :return: Apify client
    """
    client = ApifyClient(token)
    return client


def query_instagram_info(client, run_input):
    actor = client.actor("zuzka/instagram-profile-scraper")
    run = actor.call(run_input=run_input)
    print("--- Run succeeded ---")
    unpackaged = actor.last_run(status='SUCCEEDED')
    unpackaged_json = unpackaged.dataset().list_items().items
    print("--- Results retrieved ---")
    parsed = []

    for item in unpackaged_json:
        values = []
        values.append(item["username"])
        values.append(item["followersCount"])
        values.append(item["followsCount"])
        values.append(item["postsCount"])
        parsed.append(values)

    df = pd.DataFrame(parsed,
        columns=["Username", "Followers", "Following", "postsCount"])
    print("--- Results parsed ---")

    return df


def query_last_trimester_of_tweets(client, run_input):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    today = datetime.datetime.strptime(today, "%Y-%m-%d")
    last_trimester = today - datetime.timedelta(days=90)

    today = datetime.datetime.today().strftime('%Y-%m-%d')
    last_trimester = datetime.datetime.strftime(last_trimester, "%Y-%m-%d")

    actor = client.actor("apify/twitter-history-scraper")
    run = actor.call(run_input=run_input)
    print("--- Run succeeded ---")
    unpackaged = actor.last_run(status='SUCCEEDED')
    unpackaged_json = unpackaged.dataset().list_items().items
    print("--- Results retrieved ---")

    parsed = []

    for item in unpackaged_json:
        values = []
        values.append(item["full_text"])
        values.append(item["hashtags"])
        values.append(item["created_at"])
        parsed.append(values)

    df = pd.DataFrame(parsed, columns=["Text", "Hashtags", "datetime"])
    df["Account"] = str(run_input["userNames"])
    print("--- Results parsed ---")

    return df


def query_most_recent_tweets_with_keyword(client, run_input):
    actor = client.actor("apify/twitter-latest-scraper")
    run = actor.call(run_input=run_input)
    print("--- Run succeeded ---")
    unpackaged = actor.last_run(status='SUCCEEDED')
    unpackaged_json = unpackaged.dataset().list_items().items
    print("--- Results retrieved ---")

    parsed = []

    for item in unpackaged_json:
        values = []
        values.append(item["user"]["name"])
        values.append(item["user"]["location"])
        values.append(item["full_text"])
        values.append(item["created_at"])
        values.append(item["hashtags"])
        parsed.append(values)

    df = pd.DataFrame(parsed, columns=["AccName", "Location", "Text", "Datetime", "Hashtags"])
    print("--- Results parsed ---")

    return df


def query_airbnbs(client, run_input):
    actor = client.actor("dtrungtin/airbnb-scraper")
    run = actor.call(run_input=run_input)
    print("--- Run succeeded ---")
    unpackaged = actor.last_run(status='SUCCEEDED')
    unpackaged_json = unpackaged.dataset().list_items().items
    print("--- Results retrieved ---")

    parsed = []

    for item in unpackaged_json:
        values = []

        values.append(item["url"])
        values.append(item["name"])

        try:
            values.append(item["stars"])
        except KeyError:
            values.append("no_stars")

        values.append(item["numberOfGuests"])
        values.append(item["address"])
        values.append(item["roomType"])
        values.append(item["location"])
        values.append(item["pricing"])
        values.append(len(item["reviews"]))

        parsed.append(values)


    df = pd.DataFrame(parsed, columns=["url", "name", "stars", "n_guests", "address", "roomType", "location", "pricing", "reviews"])
    print("--- Results parsed ---")

    return df


def query_trip_advisor_locations(client, run_input):
    
    actor = client.actor("maxcopell/free-tripadvisor")
    run = actor.call(run_input=run_input)
    print("--- Run succeeded ---")
    unpackaged = actor.last_run(status='SUCCEEDED')
    unpackaged_json = unpackaged.dataset().list_items().items
    print("--- Results retrieved ---")

    parsed = []

    for item in unpackaged_json:
        values = []

        values.append(item["name"])
        values.append(item["rankingPosition"])
        values.append(item["category"])
        values.append(item["priceLevel"])
        values.append(item["priceRange"])
        values.append(item["rating"])
        values.append(item["address"])
        values.append(item["reviews"])

        parsed.append(values)


    df = pd.DataFrame(parsed, columns=["name", "ranking", "category", "priceLevel", "priceRange", "ratingStars", "address", "reviews"])
    print("--- Results parsed ---")
    
    return df

def query_google_results(client, run_input):
    actor = client.actor("apify/google-search-scraper")
    run = actor.call(run_input=run_input)
    print("--- Run succeeded ---")
    unpackaged = actor.last_run(status='SUCCEEDED')
    unpackaged_json = unpackaged.dataset().list_items().items
    print("--- Results retrieved ---")

    parsed = []

    for item in unpackaged_json[0]["organicResults"]:
        values = []

        values.append(item["title"])
        values.append(item["url"])
        values.append(item["description"])
        values.append(item["emphasizedKeywords"])

        parsed.append(values)


    df = pd.DataFrame(parsed, columns=["title", "url", "description", "emphasizedKeywords"])
    print("--- Results parsed ---")
    
    return df

def query_google_trends(client, run_input):
    actor = client.actor("emastra/google-trends-scraper")
    run = actor.call(run_input=run_input)
    print("--- Run succeeded ---")
    unpackaged = actor.last_run(status='SUCCEEDED')
    unpackaged_json = unpackaged.dataset().list_items().items
    print("--- Results retrieved ---")

    return unpackaged_json

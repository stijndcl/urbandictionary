import requests
import sys

args = sys.argv
if len(args) < 2:
    print("Check your arguments.")
    exit(1)


def define(words):
    definition = lookup(" ".join(words))


def lookup(words):
    """
    :param words: The word(s) you want to define
    :return: A dictionary containing the best definition
    """
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

    queryString = {"word": words}

    headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        "x-rapidapi-key": getApiKey()
    }

    # Get a list of all the definitions of this query
    response = requests.request("GET", url, headers=headers, params=queryString).json()["list"]
    # Sort the response to get the definition with the highest rating
    response.sort(key=lambda x: ratio(x), reverse=True)

    # Nothing found
    if len(response) == 0:
        print("No definitions found for \"{}\"".format(words))
        exit(1)

    # A word was found, return a dictionary with all the required info.
    return {"word": response[0]["word"], "definition": response[0]["definition"],
            "example": response[0]["example"], "thumbs_up": response[0]["thumbs_up"],
            "thumbs_down": response[0]["thumbs_down"], "link": response[0]["permalink"],
            "author": response[0]["author"]}


# Calculates the upvote/downvote ratio | Don't divide by 0 if there are no (down)votes yet
def ratio(definition):
    """
    :param definition: The dictionary representing the definition of this word
    :return: the upvote/downvote ratio of this word
    """
    return (100 * int(definition["thumbs_up"])) / (int(definition["thumbs_up"]) + int(definition["thumbs_down"])) \
        if int(definition["thumbs_down"]) != 0 else 100.0


def getApiKey():
    """
    :return: Returns your api key
    """
    try:
        with open("apikey.txt", "r") as file:
            return file.readline().strip()
    except FileNotFoundError:
        print("You have not yet generated an Api key.\n"
              "Visit {} and paste your key into a file named \"apikey.txt\".".format(
               "https://english.api.rakuten.net/community/api/urban-dictionary?endpoint=53aa4f68e4b07e1f4ebeb2b0"
                ))

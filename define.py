import requests
import sys

args = sys.argv
if len(args) < 2:
    print("Check your arguments.")
    exit(1)


# Store all definitions so the user can go to prev/next without having to send another request
definitions = {}
currentDefinition = 0


def define(words):
    """
    :param words: The words to define
    """
    definition = lookup(" ".join(words))
    formatResponse(definition)


def lookup(words):
    """
    :param words: The word(s) you want to define
    :return: A dictionary containing the best definition for this word
    """
    global definitions
    url = "https://mashape-community-urban-dictionary.p.rapidapi.com/define"

    queryString = {"term": words}

    headers = {
        'x-rapidapi-host': "mashape-community-urban-dictionary.p.rapidapi.com",
        "x-rapidapi-key": getApiKey()
    }

    # Get a list of all the definitions of this query
    response = requests.request("GET", url, headers=headers, params=queryString).json()["list"]
    if "error" in response:
        print("Something went wrong. Try again later.")

    # Nothing found
    if len(response) == 0:
        print("No definitions found for \"{}\"".format(words))
        exit(3)

    definitions = [formatDict(dic) for dic in response]

    # A word was found, return a dictionary with all the required info.
    return formatDict(response[0])


def formatDict(dic):
    """
    :param dic: The dictionary to format
    :return: Returns a formatted version of an input dictionary, assigning values to their appropriate keys
    """
    return {"word": dic["word"], "definition": dic["definition"],
            "example": dic["example"], "thumbs_up": dic["thumbs_up"],
            "thumbs_down": dic["thumbs_down"], "link": dic["permalink"],
            "author": dic["author"]}


def ratio(definition):
    """
    :param definition: The dictionary representing the definition of this word
    :return: the upvote/downvote ratio of this word
    """
    return (100 * int(definition["thumbs_up"])) / (int(definition["thumbs_up"]) + int(definition["thumbs_down"])) \
        if int(definition["thumbs_down"]) != 0 else 100.0  # Don't divide by 0 if there are no downvotes yet


def getApiKey():
    """
    :return: Returns your api key
    """
    with open("{}/filepath.txt".format(sys.path[0]), "r") as file:
        path = file.readline().strip()
        if not path:
            print("You have not yet passed the path to your Api Key file.\nRun python3 config.py path_to_your_key.")
            exit(1)
    try:
        with open("{}/apikey.txt".format(sys.path[0]), "r") as file:
            return str(file.readline().strip())
    except FileNotFoundError:
        print("Could not find {}. You have not yet generated an Api key.\n"
              "Make sure you passed the correct path to your file.".format(path))
        exit(2)


def markdown(text, col):
    """
    :param text: The text to colour
    :param col: A string (or list of strings) of colours to apply
    :return: The input text with all colours applied
    """
    colours = {"blue": "\033[94m", "green": "\033[92m", "red": "\033[91m", "bold": "\033[1m"}

    # If multiple options were passed, return all of them in order
    if isinstance(col, list):
        if len(col) > 1:
            return markdown(colours[col[0]] + str(text) + "\033[0m", col[1:])

        # If a list of 1 element was passed, just take that element (avoids indexerrors)
        col = col[0]
    return colours[col] + str(text) + "\033[0m"


def formatDefinition(definition):
    """
    :param definition: The definition to format
    :return: The definition with all existing markdown removed
    """
    definition = definition.replace("[", "")
    definition = definition.replace("]", "")
    definition = definition.replace("\"", "")
    definition = definition.replace("\n\n", "\n")
    return definition


def formatResponse(definition):
    """
    :param definition: The chosen definition to format
    :return: A formatted response of the input definition
    """
    global definitions
    global currentDefinition
    print(
        "{} #{} of {}\n".format(markdown("Definition", "bold"),
                                markdown(currentDefinition + 1, "bold"), markdown(len(definitions), "bold")) +
        "{}: {}\n\n".format(markdown("Word", ["blue", "bold"]), definition["word"]) +
        "{}: {}\n\n".format(markdown("Definition", ["blue", "bold"]), formatDefinition(definition["definition"])) +
        "{}: {}\n\n".format(markdown("Example", ["blue", "bold"]), formatDefinition(definition["example"])) +
        "{}: {} | {}: {} | {}: {}%\n\n".format(markdown("Upvotes", ["green", "bold"]), definition["thumbs_up"],
                                               markdown("Downvotes", ["red", "bold"]), definition["thumbs_down"],
                                               markdown("Rating", ["blue", "bold"]), str(round(ratio(definition), 2))) +
        "{}: {}\n\n".format(markdown("Author", ["blue", "bold"]), definition["author"]) +
        "{}: {}\n".format(markdown("Link", ["blue", "bold"]), definition["link"])
    )

    np = input("Previous Definition/Next Definition (P/N): ")

    if not np:
        exit(4)

    # Next/Previous
    elif np.lower().startswith("p"):
        currentDefinition = currentDefinition - 1 if currentDefinition != 0 else currentDefinition
    elif np.lower().startswith("n"):
        currentDefinition = currentDefinition + 1 if currentDefinition != len(definitions) - 1 else currentDefinition
    else:
        print("Invalid parameter \"{}\".".format(np))
        exit(5)

    print("\n\n")
    formatResponse(definitions[currentDefinition])


define(args[1:])

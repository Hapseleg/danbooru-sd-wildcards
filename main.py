import requests
import time
import sys


def get_data(base_url, tag):
    """Fetches JSON data from the specified API URL with pagination.

    Args:
        api_url (str): The base URL with optional username and API key parameters.
        page (int): The page number for pagination (if applicable).

    Returns:
        list: A list of dictionaries containing extracted tags.
    """
    processed_data = []
    url = base_url + tag

    print(url)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()  # Assuming the response is valid JSON
        
        # Extract and split tag_string_general from each object
        for item in data:
            if "tag_string_general" in item:  # Check if "tag_string_general" exists
                processed_data += item["tag_string_general"].split()  # Split tags using whitespace
    else:
        print(f"Status code: {response.status_code}")
    
    return processed_data


def process_data(tags, toptagscount, basetag, commontags, filtertags):
    """

    """
    # add the basetag and commontags to the string
    processed_data = basetag + ', '
    for commontag in commontags:
        processed_data += commontag + ', '

    # remove them from the list
    new_tags_list = tags
    new_tags_list = [i for i in new_tags_list if i != basetag]
    for common in commontags:
        new_tags_list = [i for i in new_tags_list if i != common]
    for filter in filtertags:
        new_tags_list = [i for i in new_tags_list if i != filter]

    # create a dict
    unique_tags = set(new_tags_list)
    tags_count = {}

    # add the tags to a list of tuples with (word, count)
    for tag in unique_tags:
        lowered_tag = str(tag).lower()
        tags_count[lowered_tag] = new_tags_list.count(tag)

    # sort by count
    sorted_tags = sorted(tags_count.items(), key=lambda x:x[1], reverse=True)

    # add top toptagscount to the string
    for i in range(toptagscount):
        processed_data += sorted_tags[i][0] + ', '

    processed_data += "\n"

    return processed_data

def to_lower_case(s):
    if s:
        return str(s).lower()
    return s


def main():
    """Parses command-line arguments and runs the script."""
    import argparse
    parser = argparse.ArgumentParser(description="Extract certain tags from Danbooru, for Stable diffusion wildcard files")
    parser.add_argument("--tags", help="The tags, for example, 'cat,bird,dog' - csv", required=True)
    parser.add_argument("--commontags", help="If you want specific common tags, such as 'no_humans,simple_background' or '1girl' etc (optional) - csv", required=False)
    parser.add_argument("--filtertags", help="If you want filter tags, such as 'solo' (optional) - csv", required=False)
    parser.add_argument("--toptagscount", help="Specify the amount of tags you want added, defaults to 5 (optional) - number", required=False)
    parser.add_argument("--filename", help="If you want it to save it as a txt file in current dir (optional) - string", required=False)
    parser.add_argument("--username", help="The username to use with the API(optional) - string", required=False)
    parser.add_argument("--apikey", help="The API key for authentication (optional) - string", required=False)
    parser.add_argument("--limit", help="Amount of posts, defaults to 200 (optional) - int", required=False)
    #parser.add_argument("--minfavcount", help="Minimum amount of fav count (optional) - int", required=False)
    args = parser.parse_args()


    #construct the url----------------------
    base_url = "https://danbooru.donmai.us/posts.json?"  # Base URL, limit 200 and tag order:favcount
    lowered_tags = to_lower_case(args.tags)
    tags = lowered_tags.split(",")
    commontags = []
    filtertags = []
    toptagscount = 5

    if args.toptagscount:
        toptagscount = int(args.toptagscount)

    if args.commontags:
        commontags = to_lower_case(commontags)
        commontags = args.commontags.split(",") 

    if args.filtertags:
        filtertags = to_lower_case(filtertags)
        filtertags = args.filtertags.split(",")

    if args.limit:
        base_url += f"limit={args.limit}"
    else:
        base_url += "limit=200"


    # Construct API URL including username and API key if provided
    if args.apikey:
        base_url += f"&login={args.username}"
        base_url += f"&api_key={args.apikey}"
    else:
        if (len(commontags) + len(filtertags) + 1) > 2:
            sys.exit("Free users can max search for 2 tags at a time.")
    

    #add tags
    base_url += "&tags=order:favcount"
    # add common tags
    for commontag in commontags:
        base_url += "+" + commontag

    for filter in filtertags:
        base_url += "+" + filter

    base_url += "+"
    #construct the url----------------------
    



    wildcard_string_list = []

    for tag in tags:
        data = get_data(base_url, tag)
        if len(data) > 0:
            wildcard_string = process_data(data, toptagscount,tag, commontags, filtertags)
            wildcard_string_list.append(wildcard_string)
            print(wildcard_string)
        else:
            print(f"NO DATA FOUND FOR {tag} PLEASE CHECK YOUR TAG")
        time.sleep(1)

    if args.filename:
        f = open(f"{args.filename}.txt", "a")
        for s in wildcard_string_list:
            f.write(s)
        f.close()
        


if __name__ == "__main__":
    main()
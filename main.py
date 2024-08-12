import requests
import json
import time

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


def process_data(tags, toptagscount):
    """

    """
    processed_data = ""
    unique_tags = set(tags)
    tags_count = {}

    for tag in unique_tags:

        tags_count[tag] = tags.count(tag)
        #unique_tags.update({tag:tags.count(tag)})




    print(tags_count)


    return processed_data









def main():
    """Parses command-line arguments and runs the script."""
    #Example:
    # https://danbooru.donmai.us/posts.json?login=USERNAME&api_key=APIKEY&tags=fav:USERNAME&limit=2&page=1
    # https://danbooru.donmai.us/posts.json?tags=fav:albert&limit=2&page=1
    
    import argparse
    parser = argparse.ArgumentParser(description="Extract certain tags from Danbooru, for Stable diffusion wildcard files")
    parser.add_argument("--tags", help="The tags, for example, 'cat,bird,dog' - csv", required=True)
    parser.add_argument("--commontags", help="If you want specific common tags, such as 'no_humans,simple_background' or '1girl' etc (optional) - csv", required=False)
    parser.add_argument("--toptagscount", help="Specify the amount of tags you want added, defaults to 5 (optional) - number", required=False)
    parser.add_argument("--filename", help="If you want it to save it as a txt file in current dir (optional) - string", required=False)
    parser.add_argument("--username", help="The username to use with the API(optional) - string", required=False)
    parser.add_argument("--apikey", help="The API key for authentication (optional) - string", required=False)
    parser.add_argument("--limit", help="Amount of posts, defaults to 200 (optional) - int", required=False)
    #parser.add_argument("--minfavcount", help="Minimum amount of fav count (optional) - int", required=False)
    args = parser.parse_args()

    if args.toptagscount:
        toptagscount = args.toptagscount


    #construct the url----------------------
    base_url = "https://danbooru.donmai.us/posts.json?"  # Base URL, limit 200 and tag order:favcount
    tags = args.tags.split(",")
    commontags = []
    toptagscount = 5

    if args.commontags:
        commontags = args.commontags.split(",") 

    if args.limit:
        base_url += f"limit={args.limit}"
    else:
        base_url += "limit=200"


    # Construct API URL including username and API key if provided
    if args.apikey:
        base_url += f"&login={args.username}"
        base_url += f"&api_key={args.apikey}"

    

    #add tags
    base_url += "&tags=order:favcount"
    # add common tags
    for commontag in commontags:
        base_url += "+" + commontag
        #base_url = base_url[:-1]


    # if len(commontags) == 0:
    base_url += "+"
    #construct the url----------------------
    



    all_data = []

    for tag in tags:
        data = get_data(base_url, tag)
        process_data(data, toptagscount)
        


    # for page in range(1, args.pages + 1):
    #     page_data = get_data(api_url, page, args.limit)

    #     # Break if nothing is returned because that means... theres nothing left?
    #     if page_data.count == 0:
    #         break

    #     all_data.extend(page_data)

    #     #you can do more calls than this if youre gold or platinum but eh... No rush for me, check here for info: https://danbooru.donmai.us/wiki_pages/help%3Ausers
    #     time.sleep(1)

    # # for item in all_data:
    # #     tags = item["tags"]
    # #     for tag in tags:
    # #         total_fav_tags[tag] = total_fav_tags.get(tag, 0) + 1
    # #         if just_the_tags.__contains__(tag) == False:
    # #             just_the_tags.append(tag)

    # # Sort by the tag with the highest value!
    # sorted_tags = sorted(total_fav_tags.items(), key=itemgetter(1), reverse=True)

    # save_to_json(sorted_tags, "./files/", "total_fav_tags", ".json", False)
    # print("Total fav tags saved to total_fav_tags.json")

if __name__ == "__main__":
    main()
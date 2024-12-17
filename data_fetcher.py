import requests
import json
import time
import warnings
import urllib3

# Disable only the unverified HTTPS request warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# List of match links
match_links = [
    "https://www.mackolik.com/mac/aston-villa-vs-manchester-city/bqcfixkutrz2cqakxgc538c2c",
    "https://www.mackolik.com/mac/brentford-vs-nottingham-forest/bqqukjxfkt2l1pg3s37o3zklw",
    "https://www.mackolik.com/mac/ipswich-town-vs-newcastle-utd/bscwbokacno17wumgq52jm3h0",
    "https://www.mackolik.com/mac/west-ham-vs-brighton-hove-albion/bu13u0clkituy9j0ibwv3efpw",
    "https://www.mackolik.com/mac/crystal-palace-vs-arsenal/br5dy7fu89celv6lqm2rt7vv8",
    "https://www.mackolik.com/mac/everton-vs-chelsea-fc/brjpvrtt6xp1hgec63hmides4",
    "https://www.mackolik.com/mac/fulham-vs-southampton/bry42iitu51mkcuujnk2eugpg",
    "https://www.mackolik.com/mac/leicester-city-vs-wolverhampton/bsrb72ntjgzl4u7aymo410tg4",
    "https://www.mackolik.com/mac/manchester-united-vs-afc-bournemouth/bt5z6e9ui8y8u8yrkz9ejg7pw",
    "https://www.mackolik.com/mac/tottenham-vs-liverpool/btmq794wygveimscov4kyx4b8",
]

def extract_match_uuid(link):
    return link.split("/")[-1]

def fetch_match_details(match_uuid):
    api_url = f"https://claros.mackolik.com/match-service/soccer/match?match_uuid={match_uuid}&language=tr&country=tr"
    try:
        response = requests.get(api_url, verify=False)  # Still using verify=False but warnings are suppressed
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data for {match_uuid}. Status code: {response.status_code}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data for {match_uuid}: {e}")
        return None

# Store match details
match_details = {}

for link in match_links:
    match_uuid = extract_match_uuid(link)
    print(f"Fetching data for match_uuid: {match_uuid}...")
    match_data = fetch_match_details(match_uuid)
    if match_data:
        match_details[match_uuid] = match_data
    time.sleep(1)  # Added small delay between requests to be more polite to the server

# Save the data to a JSON file
with open("match_details.json", "w", encoding="utf-8") as file:
    json.dump(match_details, file, ensure_ascii=False, indent=4)

print("Match details have been saved to match_details.json")
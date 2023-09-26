import requests
from base64 import urlsafe_b64encode as b64enc
from json import loads

URL = "https://www.virustotal.com/api/v3/urls"
API_KEY = "c1a224f9daa04ebc3d7cafa6939ab0605301d48a81133fb527b8aab6c15b0c66"
THRESHOLD = 0 # how many malicious indications to ignore

"""
This method determines if a given url is harmful
@type target_url: str
@param target_url: the url to check
"""
def is_harmful(target_url):
    post_data = {"url" : target_url}
    headers = {
    "accept": "application/json",
    "x-apikey": API_KEY,
    "content-type": "application/x-www-form-urlencoded"
    }

    # scan the URL on VT so it will appear in the IDs list, and also retrieve the ID
    res =  requests.post(URL, data=post_data, headers=headers)

    res_json = loads(res.text)
    
    if not res_json.get("data") and not res_json["data"].get("id"):
        return "[!!!] Error - Invalid URL"

    url_id = res_json["data"]["id"].split("-")[1]
    res = requests.get(f"{URL}/{url_id}", headers=headers)
    
    is_harmful = check_for_harmful_indications(res.text)
    return is_harmful

"""
Check if URL Identifier returend from VT contains any harmful indicator
@type indicators: str
@param indicators: json with URL indications
"""
def check_for_harmful_indications(indicators):
    indicators_json = loads(indicators)
    if indicators_json.get("data") and indicators_json["data"].get("attributes") \
        and indicators_json["data"]["attributes"].get("last_analysis_stats"):   
        stat_list = indicators_json["data"]["attributes"]["last_analysis_stats"]

        return "malicious" if stat_list["malicious"] > THRESHOLD else "harmless"
    else:
        return "[!!!] Error - Invalid Indicators JSON Format"
    

def main():
    demo_url = "https://tsboi.com/israelpostil"
    status = is_harmful(demo_url)
    print(status)


if __name__ == "__main__":
    main()

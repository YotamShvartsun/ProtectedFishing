import json
import requests
from app import URLStatusCode
from base64 import urlsafe_b64encode as b64enc

URL = "https://www.virustotal.com/api/v3/urls"
API_KEY = "c1a224f9daa04ebc3d7cafa6939ab0605301d48a81133fb527b8aab6c15b0c66"
THRESHOLD = 0 # how many malicious indications to ignore

HEADERS = {
    "accept": "application/json",
    "x-apikey": API_KEY,
    "content-type": "application/x-www-form-urlencoded"
    }

"""
This method determines if a given url is harmful
@type target_url: str
@param target_url: the url to check
@rtype: URLStatusCode
@return: a URLStatusCode of "malicious" or "harmless" depending on the script's analysis
"""
def is_harmful(target_url: str) -> URLStatusCode:
    post_data = {"url" : target_url}
    

    # scan the URL on VT so it will appear in the IDs list, and also retrieve the ID
    result =  requests.post(URL, data=post_data, headers=HEADERS)

    result_json = json.loads(result.text)
    
    if not result_json.get("data") and not result_json["data"].get("id"):
        raise ValueError("Error - Invalid URL")

    url_id = result_json["data"]["id"].split("-")[1]
    result = requests.get(f"{URL}/{url_id}", headers=HEADERS)
    
    is_harmful = check_for_harmful_indications(result.text)
    return is_harmful

"""
Check if URL Identifier returend from VT contains any harmful indicator
@type indicators: str
@param indicators: json with URL indications
@rtype: URLStatusCode
@return: an enum whether the URL identifier object contains malicious indications 
"""
def check_for_harmful_indications(indicators: str) -> URLStatusCode:
    indicators_json = json.loads(indicators)
    if indicators_json.get("data") and indicators_json["data"].get("attributes") \
        and indicators_json["data"]["attributes"].get("last_analysis_stats"):   
        stat_list = indicators_json["data"]["attributes"]["last_analysis_stats"]

        return URLStatusCode.Fishing if stat_list["malicious"] > THRESHOLD else URLStatusCode.SafeURL
    else:
        raise ValueError("Error - Invalid Indicators JSON Format")
    

def main():
    demo_url = "https://tsboi.com/israelpostil"
    status = is_harmful(demo_url)
    print(status)


if __name__ == "__main__":
    main()

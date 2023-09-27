import math
import json
import requests
from datetime import datetime
from base_db_api import BaseDBAPI
from base64 import urlsafe_b64encode as b64enc


class VtApi(BaseDBAPI):
    def __init__(self, threshold=0.8):
        self._vt_url: str = "https://www.virustotal.com/api/v3/urls"
        self._api_key: str = "c1a224f9daa04ebc3d7cafa6939ab0605301d48a81133fb527b8aab6c15b0c66"
        self._threshold: int = threshold
        self._headers: dict = { "accept": "application/json", "x-apikey": self._api_key, "content-type": "application/x-www-form-urlencoded" }

    """
    Check using heuristics if the site is harmful (derived from the last scanned time and number of engines who flagged it as malicious)
    @type stat_list: str
    @param stat_list: json with URL indications
    @type last_scanned: int
    @param last_scanned: unix timestamp of when the url was last scanned
    """
    def _is_harmful_from_indications(self, stat_list: dict, last_scanned: int):
        is_harmful = False # stat_list["malicious"] > self._threshold
        daytime_diff = datetime.today() - datetime.fromtimestamp(last_scanned)
        return ((math.log(daytime_diff.days + 2, 10) ** -1) * stat_list["malicious"] * 0.2) >= self._threshold

    
    """
    Check if URL Identifier returend from VT contains any harmful indicator
    @type indicators: str
    @param indicators: json with URL indications
    @rtype: bool
    @return: an boolean whether the URL identifier object contains malicious indications 
    """
    def _check_for_harmful_indications(self, indicators: str) -> bool:
        indicators_json = json.loads(indicators)
        if indicators_json.get("data") and indicators_json["data"].get("attributes") \
            and indicators_json["data"]["attributes"].get("last_analysis_stats"):   
            stat_list = indicators_json["data"]["attributes"]["last_analysis_stats"]

            return self._is_harmful_from_indications(stat_list, indicators_json["data"]["attributes"]["last_submission_date"])
        else:
            raise ValueError("Error - Invalid Indicators JSON Format")


    """
    This method determines if a given url is harmful
    @type domain: str
    @param domain: the url to check
    @rtype: bool
    @return: a boolean of True(=malicious) or False(=safe) depending on the script's analysis
    """
    def is_site_safe(self, domain: str) -> bool:
        post_data = {"url" : domain}

        # scan the URL on VT so it will appear in the IDs list, and also retrieve the ID
        result =  requests.post(self._vt_url, data=post_data, headers=self._headers)

        result_json = json.loads(result.text)
        if result_json.get("error"):
            raise Exception(result_json["error"]["message"])
        elif not result_json.get("data") and not result_json["data"].get("id"):
            raise ValueError("Error - Invalid URL")

        url_id = result_json["data"]["id"].split("-")[1]
        result = requests.get(f"{self._vt_url}/{url_id}", headers=self._headers)
        
        is_harmful = self._check_for_harmful_indications(result.text)
        return not is_harmful


def main():
    demo_url = "https://tsboi.com/israelpostil"
    vt_checker = VtApi()
    status = vt_checker.is_site_safe(demo_url)
    print(status)


if __name__ == "__main__":
    main()

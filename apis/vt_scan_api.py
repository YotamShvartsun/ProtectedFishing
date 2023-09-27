import json
import aiohttp
import requests
from apis.base_db_api import BaseDBAPI
from base64 import urlsafe_b64encode as b64enc
from apis.db_type import DBType

class VtApi(BaseDBAPI):
    def __init__(self, dbType: DBType, threshold=0):
        super().__init__(dbType)
        self._vt_url: str = "https://www.virustotal.com/api/v3/urls"
        self._api_key: str = "bc8fc8d06edad568290af4e5677278d3a1f2d641bd746c1e9266c514900be295"
        self._threshold: int = threshold
        self._headers: dict = { "accept": "application/json", "x-apikey": self._api_key, "content-type": "application/x-www-form-urlencoded" }
    
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

            return stat_list["malicious"] > self._threshold
        else:
            raise ValueError("Error - Invalid Indicators JSON Format")
    

    """
    This method determines if a given url is harmful
    @type domain: str
    @param domain: the url to check
    @rtype: bool
    @return: a boolean of True(=malicious) or False(=safe) depending on the script's analysis
    """
    async def is_in_db(self, domain: str) -> bool:
        post_data = {"url" : domain}

        async with aiohttp.ClientSession() as session:
            # scan the URL on VT so it will appear in the IDs list, and also retrieve the ID
            result =  await session.post(self._vt_url, data=post_data, headers=self._headers)
            result.raise_for_status()
            result_json = await result.json()

        if not result_json.get("data") and not result_json["data"].get("id"):
            raise ValueError("Error - Invalid URL")

        url_id = result_json["data"]["id"].split("-")[1]
        async with aiohttp.ClientSession() as indications_session:
            result = await indications_session.get(f"{self._vt_url}/{url_id}", headers=self._headers)
            if not result.ok:
                return False
            indications_text = await result.text()
        
        is_harmful = self._check_for_harmful_indications(indications_text)
        return is_harmful


def main():
    demo_url = "https://tsboi.com/israelpostil"
    vt_checker = VtApi()
    status = vt_checker.is_site_safe(demo_url)
    print(status)


if __name__ == "__main__":
    main()

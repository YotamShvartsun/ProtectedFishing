from typing import Union
from dataclasses import dataclass
import requests
import ipaddress


@dataclass
class JsonReponse:
    status: str
    country: str
    countryCode: str
    region: str
    regionName: str
    city: str
    zip: str
    lat: int
    lon: int
    timezone: str
    isp: str
    org: str
    asn: str
    query: str


LOCATION_API = 'http://ip-api.com/json/{}'


class LocationApiFailedToFetchIpError(Exception):
    pass


def get_location_info(ip: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]) -> JsonReponse:
    response = requests.get(LOCATION_API.format(str(ip)))
    response.raise_for_status()
    json_response = response.json()
    if json_response['status'] != 'success':
        raise LocationApiFailedToFetchIpError(
            f'For ip: {str(ip)}, the api: {LOCATION_API} failed to fetch geoinfo'
        )
    as_result = json_response.pop('as')
    json_response['asn'] = as_result
    return JsonReponse(**json_response)

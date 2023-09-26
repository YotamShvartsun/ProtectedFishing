from typing import Union
from dataclasses import dataclass
import ipaddress
import logging
import requests
import socket

from apis.base_db_api import BaseDBAPI

_LOGGER = logging.getLogger('app.apis.iplocation')

@dataclass
class GeolocationResponse:
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


class FailedToResolveDomain(Exception):
    pass


class IPLocationDBAPI(BaseDBAPI):
    UNSAFE_COUNTRY_CODES = ['ir', 'sy', 'lb']
    def get_location_info(self, ip: Union[ipaddress.IPv4Address, ipaddress.IPv6Address]) -> GeolocationResponse:
        response = requests.get(LOCATION_API.format(str(ip)))
        response.raise_for_status()
        json_response = response.json()
        if json_response['status'] != 'success':
            raise LocationApiFailedToFetchIpError(
                f'For ip: {str(ip)}, the api: {LOCATION_API} failed to fetch geoinfo'
            )
        as_result = json_response.pop('as')
        json_response['asn'] = as_result
        return GeolocationResponse(**json_response)

    def get_ip_from_domain(self, domain: str) -> ipaddress.IPv4Address:
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            _LOGGER.error(f'Failed to resolve domain name {domain}')
            raise FailedToResolveDomain()
    
    def is_in_safe_country(self, country_code: str) -> bool:
        return country_code not in self.UNSAFE_COUNTRY_CODES

    def is_site_safe(self, domain: str) -> bool:
        try:
            ip_addr = self.get_ip_from_domain(domain)
            location_data = self.get_location_info(ip_addr)
            _LOGGER.info(f'domain {domain} has location {location_data}')
            _LOGGER.debug(f'Unsafe country codes are {self.UNSAFE_COUNTRY_CODES}, and the current country code is {location_data.countryCode}')
            return self.is_in_safe_country(location_data.countryCode.lower())
        except FailedToResolveDomain:
            return True


# if __name__ == '__main__':
#     x = IPLocationDBAPI()
#     print(x.is_site_safe('egov.sy'))

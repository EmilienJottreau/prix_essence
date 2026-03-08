from abc import abstractmethod

from models.fuelPrice import FuelPrice


class Provider:
    headers = {
        "accept": "application/json",
        "accept-language": "fr-FR,fr;q=0.5",
        "priority": "u=1, i",
        "sec-ch-ua": '"Not:A-Brand";v="99", "Brave";v="145", "Chromium";v="145"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36",
    }

    @abstractmethod
    def get_price(self) -> FuelPrice:
        raise NotImplementedError("get_price must be implemented")

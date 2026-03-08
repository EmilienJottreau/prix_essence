from datetime import datetime

import requests


from models.fuelPrice import FuelPrice
from sources.provider import Provider


class TotalProvider(Provider):

    special_header = {
        "origin": "https://services.totalenergies.fr",
        "referer": "https://services.totalenergies.fr/",
        "api-key": "SC.8Q~32p3cNR6oVRWyHPppS8JdWGV5-LxnHUaEU",
    }

    params = {
        "type": "FUELING",
    }

    def get_price(self, station_code) -> FuelPrice:
        self.headers.update(self.special_header)
        self.params.update({"location_id": station_code})

        response = requests.get(
            "https://apis.poifinder.alzp.tgscloud.net/poi-finder-store-locator-back/api/v1/point-of-interest",
            params=self.params,
            headers=self.headers,
        )

        # print(response.status_code)
        if response.status_code != 200:
            print("Status code not 200, might be api key")
            return

        # find
        json_reps = response.json()
        try:
            products_and_services = json_reps["products_and_services"]
            station_name = json_reps["contractual_name"]
        except KeyError:
            print("No products and services found")
            return None

        try:
            diesel_product = list(
                filter(lambda x: x["product_code"] == "GO", products_and_services)
            )
            essence_product = list(
                filter(lambda x: x["product_code"] == "E10", products_and_services)
            )

            diesel_product_name = ""
            diesel_product_price = 0
            diesel_product_updated_at = 0

            if len(diesel_product) == 0:
                print("No diesel product found")
            else:
                diesel_product_name = diesel_product[0]["product_name"]
                diesel_product_price = diesel_product[0]["price"]
                diesel_product_updated_at = datetime.strptime(
                    diesel_product[0]["price_update_date_time"], "%Y-%m-%dT%H:%M:%SZ"
                )

            essence_product_name = ""
            essence_product_price = 0
            essence_product_updated_at = 0
            if len(essence_product) == 0:
                print("No essence product found")
            else:
                essence_product_name = essence_product[0]["product_name"]
                essence_product_price = essence_product[0]["price"]
                essence_product_updated_at = datetime.strptime(
                    essence_product[0]["price_update_date_time"], "%Y-%m-%dT%H:%M:%SZ"
                )

            result = FuelPrice(
                station_name=station_name,
                sp95_name=essence_product_name,
                sp95_price=essence_product_price,
                sp95_updated_at=essence_product_updated_at,
                diesel_name=diesel_product_name,
                diesel_price=diesel_product_price,
                diesel_updated_at=diesel_product_updated_at,
            )
            return result
        except KeyError:
            print("JSON has changed, must re-develop")
            return None

    def get_all_stations(self) -> list:
        return [
            "NF059545",  # porte du vignoble
            "NF042579",  # porte du reze
            "NF079860",  # porte du retz
        ]

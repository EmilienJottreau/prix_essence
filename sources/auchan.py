from datetime import datetime

from bs4 import BeautifulSoup
import requests


from models.fuelPrice import FuelPrice
from sources.provider import Provider


class AuchanProvider(Provider):
    special_header = {
        "referer": "https://www.auchan.fr/nos-magasins",
    }

    def get_price(self, station_code) -> FuelPrice:
        self.headers.update(self.special_header)

        response = requests.get(
            f"https://www.auchan.fr/magasins/hypermarche/{station_code}",
            headers=self.headers,
        )

        if response.status_code != 200:
            print("Status code not 200")
            return

        soup = BeautifulSoup(response.text, "html.parser")

        all_visual_price = soup.select(".fuel-element-content > div")

        essence_price = 0
        essence_updated_at = 0
        diesel_price = 0
        diesel_updated_at = 0


        for visual_price in all_visual_price:
            if visual_price.find("div", class_="name").text == "GASOIL":
                diesel_price = visual_price.find("div", class_="price").text.replace(",", ".").replace("€", "")
                diesel_updated_at = datetime.strptime(visual_price.find("span", class_="value").text, "%d/%m/%Y")
            elif visual_price.find("div", class_="name").text == "SP95 E10":
                essence_price = visual_price.find("div", class_="price").text.replace(",", ".").replace("€", "")
                essence_updated_at = datetime.strptime(visual_price.find("span", class_="value").text, "%d/%m/%Y")
        
        diesel_name = "GASOIL"
        essence_name = "SP95 E10"
        station_name = station_code.split("/")[0]

        result = FuelPrice(
            station_name=station_name,
            sp95_name=essence_name,
            sp95_price=float(essence_price),
            sp95_updated_at=essence_updated_at,
            diesel_name=diesel_name,
            diesel_price=float(diesel_price),
            diesel_updated_at=diesel_updated_at,
        )

        return result
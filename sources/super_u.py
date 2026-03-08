from datetime import datetime

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, Playwright
import requests

from models.fuelPrice import FuelPrice
from sources.provider import Provider


class SuperUProvider(Provider):

    def get_price(self, station_code) -> FuelPrice:
        with sync_playwright() as playwright:
            chromium = playwright.chromium # or "firefox" or "webkit".
            browser = chromium.launch(headless=False)
            print("launch browser")
            page = browser.new_page()
            print("navigate")
            page.goto(f"https://www.magasins-u.com/station/{station_code}")
            print("navigate ok, searching element")
            # other actions...
            table = page.locator("table", has_text="SP95").first.inner_html()
            browser.close()

            soup = BeautifulSoup(table, "html.parser")
            
            # <tr class="u-station__line-fuel">
            #     <td class="name">SP95-E10</td>
            #     <td class="price">1,729 €/l</td>
            # </tr>
            essence_name = "SP95-E10"
            if soup.find("td", text=essence_name) is None:
                essence_name = "SP95"
            essence_price = soup.find("td", text=essence_name).parent.find("td", class_="price").text.split(" ")[0]
            essence_updated_at = datetime.now()

            diesel_name = "Gazole"
            diesel_price = soup.find("td", text=diesel_name).parent.find("td", class_="price").text.split(" ")[0]
            diesel_updated_at = datetime.now()

            station_name = station_code.split("_")[0].split("-")[1]

            result = FuelPrice(
                station_name=station_name,
                sp95_name=essence_name,
                sp95_price=float(essence_price.replace(",", ".")),
                sp95_updated_at=essence_updated_at,
                diesel_name=diesel_name,
                diesel_price=float(diesel_price.replace(",", ".")),
                diesel_updated_at=diesel_updated_at,
            )

            return result

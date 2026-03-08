from sources.auchan import AuchanProvider
from sources.super_u import SuperUProvider
from sources.total import TotalProvider

from database import get_db

with get_db() as db:

    total = TotalProvider()
    for station in total.get_all_stations():
        prix = total.get_price(station) 
        db.add(prix)
        db.commit()

    super_u = SuperUProvider()
    prix = super_u.get_price("hyperu-vallet_81980") # perif
    db.add(prix)
    db.commit()
    prix = super_u.get_price("hyperu-vallet_81979") # magasin
    db.add(prix)
    db.commit()


    auchan = AuchanProvider()
    prix = auchan.get_price("auchan-hypermarche-nantes-st-sebastien/s-53")
    db.add(prix)
    db.commit()

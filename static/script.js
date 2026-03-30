const COORDS = {
        "REL.BOUGUENAIS": [47.16498, -1.5703],
        "RELAIS LA DIVATTE": [47.22201, -1.47318],
        "RELAIS REZE": [47.16051, -1.5513],
        "auchan-hypermarche-nantes-st-sebastien": [47.19267, -1.49176],
        "vallet_magasin": [47.16930, -1.26676],
        "vallet_perif": [47.15824, -1.27475],
      };

      const map = L.map("map", { zoomControl: false }).setView([47.17, -1.47], 11);

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png").addTo(map);

      async function loadData() {
        try {
          const response = await fetch("/prices/latest");
          let data = await response.json();

          // Nettoyage des doublons éventuels par nom de station
          const uniqueData = Array.from(new Map(data.map(item => [item.station_name, item])).values())
					.sort((a, b) => a.sp95_price - b.sp95_price);
          
          const list = document.getElementById("station-list");

          uniqueData.forEach((s) => {
            const pos = COORDS[s.station_name] || [47.2, -1.5];

            // Marqueur Carte
            const marker = L.marker(pos).addTo(map);
            marker.bindPopup(`
                <b>${s.station_name.replace(/[-_]/g, " ")}</b><br>
                ${s.sp95_name}: ${s.sp95_price.toFixed(3)}€<br>
                ${s.diesel_name}: ${s.diesel_price.toFixed(3)}€
            `);

            // Création Card
            const card = document.createElement("div");
            card.className = "card";
            card.onclick = () => {
              map.setView(pos, 15);
              marker.openPopup();
              window.scrollTo({ top: 0, behavior: "smooth" });
            };

            const dateEssence = s.sp95_updated_at.split(" ")[0];
            
            card.innerHTML = `
                <div class="station-name">${s.station_name.replace(/[-_]/g, " ")}</div>
                <div class="price-row">
                    <span class="fuel-type">${s.sp95_name}</span>
                    <span class="price-tag sp95">${s.sp95_price.toFixed(3)}€</span>
                </div>
                <div class="price-row">
                    <span class="fuel-type">${s.diesel_name}</span>
                    <span class="price-tag diesel">${s.diesel_price.toFixed(3)}€</span>
                </div>
                <div class="date">Mise à jour : ${dateEssence}</div>
            `;
            list.appendChild(card);
          });
        } catch (e) {
          console.error("Erreur de chargement :", e);
        }
      }

      loadData();

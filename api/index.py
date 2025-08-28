from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup
import csv
from fastapi.responses import Response

app = FastAPI()

URL = "https://www.transfermarkt.com/transfers/transferrekorde/statistik/top/plus/0/galerie/0?saison_id=2025&land_id=&ausrichtung=&spielerposition_id=&altersklasse=&jahrgang=0&leihe=&w_s="

@app.get("/top15.csv")
def get_top15_csv():
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(URL, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    rows = []
    for tr in soup.select("table.tm-table tbody tr")[:15]:
        tds = tr.find_all("td")
        if len(tds) < 6:
            continue
        name = tds[1].get_text(strip=True)
        dest = tds[4].get_text(strip=True)
        fee = tds[5].get_text(strip=True)
        rows.append([name, dest, fee])

    output = []
    writer = csv.writer(output := [])
    writer.writerow(["Player", "To Club", "Fee"])
    for row in rows:
        writer.writerow(row)

    return Response("\n".join(output), media_type="text/csv")

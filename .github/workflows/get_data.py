from datetime import datetime
import os

from bs4 import BeautifulSoup
from deta import Deta


def main(db, file_path):
    date_now = datetime.now().strftime("%Y%m%d%H%M%S%f")
    with open(file_path, "r") as f:
        soup = BeautifulSoup(f, features="html.parser")

    table = soup.body.find("table", {"id":"items-table"})
    last_key = table.attrs["data-last"]
    items = db.fetch(limit=1000, last=last_key)

    if items.count > 0:
        tbody = table.tbody
        for item in items.items:
            tr = soup.new_tag("tr")
            td_cat = soup.new_tag("td")
            td_url = soup.new_tag("td")
            td_desc = soup.new_tag("td")
            td_user = soup.new_tag("td")
            td_cat.string = ", ".join(item["categories"])
            td_url.string = item["url"]
            td_desc.string = item["desc"]
            td_user.string = item["user"]
            tr.append(td_cat)
            tr.append(td_url)
            tr.append(td_desc)
            tr.append(td_user)    
            tbody.append(tr)

        last_key = items.items[-1]["key"]
    else:
        last_key = date_now
    
    table.attrs["data-last"] = last_key

    with open(file_path, "w") as f:
        f.write(soup.prettify())

if __name__ == "__main__":
    deta = Deta(os.getenv("DETA_PROJECT_KEY"))
    db = deta.Base("links")
    file_path = "index.html"
    main(db, file_path)
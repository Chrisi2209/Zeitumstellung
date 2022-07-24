import requests
import bs4
import datetime as dt

url = "https://www.feiertage-oesterreich.at/termine/zeitumstellung/"


def main():
    resp = requests.get(url)
    document = bs4.BeautifulSoup(resp.text, "html.parser")

    results = {}
    years = document.find_all("div", style="padding: 20px 0 10px 0;")
    for year in years:
        results[year.strong.string] = {}
        table = year.next_sibling.next_sibling
        table_rows = table.children
        for table_row in table_rows:
            time = table_row.find("td")
            if time != -1:
                results[year.strong.string][time.string] = {}
                data = time
                for data_name in ("date", "direction", "time_displacement"):
                    data = data.next_sibling.next_sibling
                    if data_name == "date":
                        data_day = int(data.string[5:7])
                        data_year = int(data.string[-4:])
                        if data.string[-6] == "z":
                            data_month = 3
                        else:
                            data_month = 10
                        date_data = dt.date(data_year, data_month, data_day)
                        results[year.strong.string][time.string][data_name] = date_data
                    else:
                        results[year.strong.string][time.string][data_name] = data.string
        
    # change the formatting of the time_displacement
    for i, key in enumerate(results):
        for value in results[key]:
            results[key][value]["time_displacement"] = results[key][value]["time_displacement"].split(" ⇢")

    return results

    


if __name__ == "__main__":
    print(main())

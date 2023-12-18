import json
import datetime
from dateutil.parser import parse


with open('ieee_data.json') as data_file:
    data = json.load(data_file)

dico_journal = {}
all_journals = []
# date_set = set()

for v in data:
    try:
        date1 = v["Day"]+' ' + v["MonthName"]+' ' + v["Year"]
    except:
        date1 = ""
    Access = ""

    LocationsPro = []
    Universities = []
    Countries = []
    university_set = set()
    Country_set = set()
    Author_set = set()

    for author in v["Authors"]:

        Author_set.add(author)
        Author_s = ';'.join(author for author in Author_set)

    for location in v["Locations"]:
        location = location.split('\n', 1)[0]
        location = location.replace('View Profile', '')
        university_set.update(location.split(',')[0:2])
        University = ';'.join(university for university in university_set)

        Country = Country_set.add((location.split(',')[-1]))
        Country = ';'.join(Country for Country in Country_set)

        if (Country == University):
            Country = ""
        LocationsPro.append(location)

    dico_journal = {"Title": v["Title"], "Abstract": v["Abstract"], "Type": v["Type"], "Access": Access, "Date": date1, "Year": v["Year"], "Month": v["Month"], "MonthName": v["MonthName"],
                    "Day": v["Day"], "DOI": v["DOI"], "Publisher": v["Publisher"], "Authors": Author_s, "Locations": v["Locations"], "Locations": LocationsPro, "Universities": University, "Countries": Country}

    all_journals.append(dico_journal)

with open("ieee_data_final.json", "w") as write_file:
    json.dump(all_journals, write_file, indent=4)

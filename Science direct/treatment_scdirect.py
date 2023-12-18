import json
import datetime
from dateutil.parser import parse


with open('scdirect_data.json') as data_file:
    data = json.load(data_file)

dico_journal = {}
all_journals = []


for v in data:
    if v["Date"] != "":
        date = v["Date"]

        try:
            date1 = (date.split(',')[-2])
        except:
            date1 = ""

        try:
            MonthName = (date1.split(' ')[-2])
        except:
            MonthName = ""

        try:
            Year = (date1.split(' ')[-1])
        except:
            Year = ""

        if (MonthName == "January"):
            Month = "1"
        if (MonthName == "February"):
            Month = "2"
        if (MonthName == "March"):
            Month = "3"
        if (MonthName == "April"):
            Month = "4"
        if (MonthName == "May"):
            Month = "5"
        if (MonthName == "June"):
            Month = "6"
        if (MonthName == "July"):
            Month = "7"
        if (MonthName == "August"):
            Month = "8"
        if (MonthName == "September"):
            Month = "9"
        if (MonthName == "October"):
            Month = "10"
        if (MonthName == "November"):
            Month = "11"
        if (MonthName == "December"):
            Month = "12"

        try:
            Day = (date1.split(' ')[-3])
        except:
            Day = ""
    else:
        date1 = ""
        Month = ""
        Year = ""
        MonthName = ""
        Day = ""

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

    dico_journal = {"Title": v["Title"], "Abstract": v["Abstract"], "Type": v["Type"], "Access": v["Access"], "Date": date1, "Year": Year, "Month": Month, "MonthName": MonthName,
                    "Day": Day, "DOI": v["DOI"], "Publisher": v["Publisher"], "Authors": Author_s, "Locations": v["Locations"], "Locations": LocationsPro, "Universities": University, "Countries": Country}

    all_journals.append(dico_journal)

with open("scdirect_data_final.json", "w") as write_file:
    json.dump(all_journals, write_file, indent=4)

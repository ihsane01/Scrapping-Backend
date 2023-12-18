import json
import datetime
from dateutil.parser import parse


with open('acm_data.json') as data_file:
    data = json.load(data_file)

dico_journal = {}
all_journals = []


for v in data:
    if v["Date"] != "":
        date = parse(v["Date"])
        Year = date.year
        Year = str(Year)
        Month = date.month
        Month = str(Month)
        if (Month == "1"):
            MonthName = "January"
        if (Month == "2"):
            MonthName = "February"
        if (Month == "3"):
            MonthName = "March"
        if (Month == "4"):
            MonthName = "April"
        if (Month == "5"):
            MonthName = "May"
        if (Month == "6"):
            MonthName = "June"
        if (Month == "7"):
            MonthName = "July"
        if (Month == "8"):
            MonthName = "August"
        if (Month == "9"):
            MonthName = "September"
        if (Month == "10"):
            MonthName = "October"
        if (Month == "11"):
            MonthName = "November"
        if (Month == "12"):
            MonthName = "December"
        Day = date.day
        Day = str(Day)
    else:
        Year = ""
        Month = ""
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

    dico_journal = {"Title": v["Title"], "Abstract": v["Abstract"], "Type": v["Type"], "Access": v["Access"], "Date": v["Date"], "Year": Year, "Month": Month, "MonthName": MonthName,
                    "Day": Day, "DOI": v["DOI"], "Publisher": v["Publisher"], "Authors": Author_s, "Locations": LocationsPro, "Universities": University, "Countries": Country}

    all_journals.append(dico_journal)

with open("acm_data_final.json", "w") as write_file:
    json.dump(all_journals, write_file, indent=4)

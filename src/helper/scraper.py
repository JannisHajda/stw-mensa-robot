from urllib.request import urlopen
import xml.etree.ElementTree as ET
import datetime
import math


def get_date():
    today = datetime.datetime.today()
    return today.strftime("%d.%m.%Y")


def get_menus(url):
    with urlopen(url) as response:
        tree = ET.parse(response)
        return tree.getroot()


def get_menu(menus, date):
    menu = menus.find("datum[@index='{}']".format(date))
    return menu


def get_sample_menu():
    tree = ET.parse("src/helper/sample.xml")
    return tree.getroot()


def kj_to_kcal(kj):
    return math.floor(kj * 0.239005736)


def get_offers(menu):
    if menu.findall("angebotnr") is not None:
        offers = []

        for offer in menu.findall("angebotnr"):
            kcal = protein = carbs = fat = None
            vegan = vegetarian = chicken = garlic = pork = cow = fish = regional = alcohol = False

            title = offer.find("titel").text
            desc = offer.find("beschreibung").text

            student_price = offer.find("preis_s").text if offer.find(
                "preis_s") is not None else None
            guest_price = offer.find("preis_g").text if offer.find(
                "preis_g") is not None else None

            nutrients = offer.find("nutrients").findall("nutrient") if offer.find(
                "nutrients") is not None else None

            if nutrients is not None:
                for nutrient in nutrients:
                    if nutrient.find("name").text == "Energie (Kilojoule)":
                        kj = int(nutrient.find("wert").text)
                        kcal = kj_to_kcal(kj)
                    elif nutrient.find("name").text == "Eiweiß (Protein)":
                        protein = float(nutrient.find("wert").text)
                    elif nutrient.find("name").text == "Kohlenhydrate, resorbierbar":
                        carbs = float(nutrient.find("wert").text)
                    elif nutrient.find("name").text == "Fett":
                        fat = float(nutrient.find("wert").text)

            labels = offer.find("labels").findall("label") if offer.find(
                "labels") is not None else None

            if labels is not None:
                for label in labels:
                    if label.attrib["name"] == "vegan":
                        vegan = True
                    elif label.attrib["name"] == "Geflügel":
                        chicken = True
                    elif label.attrib["name"] == "Knoblauch":
                        garlic = True
                    elif label.attrib["name"] == "vegetarisch":
                        vegetarian = True
                    elif label.text == "Alkohol":
                        alcohol = True
                    elif label.text == "Fisch":
                        fish = True
                    elif label.text == "regional":
                        regional = True
                    elif label.text == "Schwein":
                        pork = True
                    elif label.text == "Rind":
                        cow = True

            offers.append(
                {
                    "title": title,
                    "desc": desc,
                    "student_price": student_price,
                    "guest_price": guest_price,
                    "nutrients": {
                        "kcal": kcal if kcal is not None else None,
                        "protein": protein if protein is not None else None,
                        "carbs": carbs if carbs is not None else None,
                        "fat": fat if fat is not None else None
                    },
                    "labels": {
                        "vegan": vegan,
                        "vegetarian": vegetarian,
                        "regional": regional,
                        "alcohol": alcohol,
                        "garlic": garlic,
                        "chicken": chicken,
                        "pork": pork,
                        "cow": cow,
                        "fish": fish,
                    }
                }
            )

        return offers

    return None


def scrape(url):
    menus = get_menus(url)
    todays_menu = get_menu(menus, get_date())

    if todays_menu is not None:
        offers = get_offers(todays_menu)
        return offers
    else:
        return None

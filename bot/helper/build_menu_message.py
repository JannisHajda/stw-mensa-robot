from helper.locales import locales


def label_to_emoji(label):
    if label == "vegan":
        return "π±"
    elif label == "vegetarian":
        return "π₯¦"
    elif label == "regional":
        return "π½"
    elif label == "alcohol":
        return "πΊ"
    elif label == "garlic":
        return "π§"
    elif label == "chicken":
        return "π"
    elif label == "pork":
        return "π·"
    elif label == "cow":
        return "π"
    elif label == "fish":
        return "π"


def build_message(canteen_name, menu, detail=False):
    message = "π {} {} π\n\n".format(locales['menu_for'], canteen_name)

    for offer in menu:
        labels = offer["labels"]
        labels = [label for label in labels if labels[label] is True]
        labels = [label_to_emoji(label) for label in labels]

        message += 'π½οΈ {} {}\n'.format(offer["title"], " ".join(labels))
        message += '{}\n'.format(offer["desc"])

        if detail:
            nutrients = offer["nutrients"]
            nutrients = [
                nutrient for nutrient in nutrients if nutrients[nutrient] is not None]

            if len(nutrients) > 0:
                message += '\n'
                message += 'π NΓ€hrwerte:\n'

                if offer["nutrients"]["kcal"] is not None:
                    message += "β‘ {} kcal \n".format(
                        offer["nutrients"]["kcal"])

                if offer["nutrients"]["carbs"] is not None:
                    message += "π {}g Kohlenhydrate \n".format(
                        offer["nutrients"]["carbs"])

                if offer["nutrients"]["protein"] is not None:
                    message += "π {}g Protein \n".format(
                        offer["nutrients"]["protein"])

                if offer["nutrients"]["fat"] is not None:
                    message += "π₯© {}g Fett \n".format(
                        offer["nutrients"]["fat"])

                message += "\n"

        prices = []

        if offer["student_price"] is not None:
            prices.append("{}β¬".format(offer["student_price"]))
        if offer["guest_price"] is not None:
            prices.append("{}β¬".format(offer["guest_price"]))
        if len(prices) > 0:
            message += "π° {}\n".format(" | ".join(prices))

        message += "\n"

    return message

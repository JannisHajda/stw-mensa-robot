from helper.locales import locales


def label_to_emoji(label):
    if label == "vegan":
        return "🌱"
    elif label == "vegetarian":
        return "🥦"
    elif label == "regional":
        return "🌽"
    elif label == "alcohol":
        return "🍺"
    elif label == "garlic":
        return "🧄"
    elif label == "chicken":
        return "🐔"
    elif label == "pork":
        return "🐷"
    elif label == "cow":
        return "🐄"
    elif label == "fish":
        return "🐟"


def build_message(canteen_name, menu, detail=False):
    message = "🌟 {} {} 🌟\n\n".format(locales['menu_for'], canteen_name)

    for offer in menu:
        labels = offer["labels"]
        labels = [label for label in labels if labels[label] is True]
        labels = [label_to_emoji(label) for label in labels]

        message += '🍽️ {} {}\n'.format(offer["title"], " ".join(labels))
        message += '{}\n'.format(offer["desc"])

        if detail:
            nutrients = offer["nutrients"]
            nutrients = [
                nutrient for nutrient in nutrients if nutrients[nutrient] is not None]

            if len(nutrients) > 0:
                message += '\n'
                message += '🔍 Nährwerte:\n'

                if offer["nutrients"]["kcal"] is not None:
                    message += "⚡ {} kcal \n".format(
                        offer["nutrients"]["kcal"])

                if offer["nutrients"]["carbs"] is not None:
                    message += "🍞 {}g Kohlenhydrate \n".format(
                        offer["nutrients"]["carbs"])

                if offer["nutrients"]["protein"] is not None:
                    message += "🍗 {}g Protein \n".format(
                        offer["nutrients"]["protein"])

                if offer["nutrients"]["fat"] is not None:
                    message += "🥩 {}g Fett \n".format(
                        offer["nutrients"]["fat"])

                message += "\n"

        prices = []

        if offer["student_price"] is not None:
            prices.append("{}€".format(offer["student_price"]))
        if offer["guest_price"] is not None:
            prices.append("{}€".format(offer["guest_price"]))
        if len(prices) > 0:
            message += "💰 {}\n".format(" | ".join(prices))

        message += "\n"

    return message

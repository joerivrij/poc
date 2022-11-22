import datetime


def validate_author(author):
    today = datetime.date.today()
    tomorrow = today + datetime.timedelta(days=1)

    dob = datetime.datetime.strptime(author.date_of_birth, "%d-%m-%Y").date()
    if dob > tomorrow:
        return {"valid": False, "reason": "an author cannot be born in the future"}

    return {"valid": True, "reason": "this is a valid author"}

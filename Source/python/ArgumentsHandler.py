import argparse
import datetime

DataChoices : list[str] = [
    "standings",
    # "stats"
]

def validateDate(date_input : str) -> str:
    if date_input == "now":
        return "now"
    try:
        return str(datetime.datetime.strptime(date_input, "%Y-%m-%d").date())
    except ValueError:
        raise argparse.ArgumentTypeError(f"ERROR : Invalid date input (YYYY-MM-DD)")


def run() -> argparse.Namespace:

    Parser : argparse.ArgumentParser = argparse.ArgumentParser()

    Parser.add_argument(
        "data",
        choices = DataChoices,
        help = "NHL data to display"
    )

    Parser.add_argument(
        "-t",
        "--type",
        type = str,
        help = "the specific way to view given data" # Write a better help section
    )

    Parser.add_argument(
        "-d",
        "--date",
        type = validateDate,
        default = "now",
        help = "specify date for certain NHL data (YYYY-MM-DD)"
    )

    Arguments : argparse.Namespace = Parser.parse_args()

    return Arguments
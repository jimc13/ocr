#!/usr/bin/env python3
import json
import time
from helpers import select_unicode_responses
from config import week_json_path, today_responses_path

# To be ran as a daily cron
def main():
    with open(week_json_path) as f:
        day_data = json.load(f)

    day = time.strftime('%a').upper()
    day = "WED"
    text = day_data[day].replace(" {} ".format(day), ' ')
    responses = select_unicode_responses(text)
    print(responses)
    with open(today_responses_path, "w") as f:
        json.dump(responses, f)

if __name__ == "__main__":
    main()

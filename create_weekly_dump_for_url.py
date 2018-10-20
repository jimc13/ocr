#!/usr/bin/env python3
import json
from helpers import create_jpg, get_text_for_jpg, pull_info_out_by_day
from config import url, jpg_path, week_json_path

# To be ran as a weekly cron
def main():
    create_jpg(url, jpg_path)
    text = get_text_for_jpg(jpg_path)
    # Keep a record of what text we got
    day_data = pull_info_out_by_day(text)
    with open(week_json_path, "w") as f:
        json.dump(day_data, f)

if __name__ == "__main__":
    main()

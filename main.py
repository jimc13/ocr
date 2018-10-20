#!/usr/bin/env python3
import numpy as np
import pytesseract
import cv2
import requests
import io
import wand.image
import os
import time
import unicodedata
from config import url

def get_jpg(url):
    """
    Fetches a the content from a URL and converts it to a fairly big jpg on the
    assumption it is a PDF that we need to maintain the quality of
    """
    r = requests.get(url, timeout=30)
    r.raise_for_status()
    f = io.BytesIO(r.content)
    with wand.image.Image(file=f, resolution=500) as img:
        with img.convert('jpg') as converted:
            converted.compression_quality = 99
            converted.save(filename='menu.jpg')


def get_string(img_path, output_path="out"):
    """
    Carries out a number of transformations with the intention in improving the
    readablity of the image.  Each of these are saved as separate files as this
    is here for testing / to be played with rather than ran regularly
    """
    # Read image using opencv
    img = cv2.imread(img_path)

    # Extract the file name without the file extension
    file_name = os.path.basename(img_path).split('.')[0]
    file_name = file_name.split()[0]

    # Create a directory for outputs
    output_path = os.path.join(output_dir, file_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    cv2.imwrite('{}/1-initial.jpg'.format(output_path), img)

    # Rescale the image, if needed.
    img = cv2.resize(img, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
    cv2.imwrite('{}/2-resized.jpg'.format(output_path), img)

    # Convert to gray
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    cv2.imwrite('{}/3-grey.jpg'.format(output_path), img)

    # Apply dilation and erosion to remove some noise
    kernel = np.ones((1, 1), np.uint8)
    img = cv2.dilate(img, kernel, iterations=1)
    cv2.imwrite('{}/4-dilated.jpg'.format(output_path), img)
    img = cv2.erode(img, kernel, iterations=1)
    cv2.imwrite('{}/5-eroded.jpg'.format(output_path), img)

    # Apply blur to smooth out the edges
    img = cv2.GaussianBlur(img, (5, 5), 0)
    cv2.imwrite('{}/6-blurred.jpg'.format(output_path), img)

    # Apply threshold to get image with only b&w (binarization)
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cv2.imwrite('{}/7-bw.jpg'.format(output_path), img)

    # Save the filtered image in the output directory
    save_path = os.path.join(output_path, file_name + ".jpg")
    cv2.imwrite(save_path, img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(img, lang="eng")
    return result

def get_string_for_dir(dir):
    """
    Function to be used in testing to compare the improvements of different
    stages in the image declutter process
    """
    for x, y, files in os.walk(dir):
        for filename in sorted(files):
            assert filename.endswith("jpg")
            with open(os.path.join(dir, filename.replace('jpg', 'txt')), 'w') as f:
                img = cv2.imread(os.path.join(dir, filename))
                f.write(pytesseract.image_to_string(img, lang="eng"))

def pull_info_out_by_day(text):
    """
    Goes through the menu and makes a few assumptions in order to create
    a dictionary, key: day, value: text from menu that day
    """
    # Use placeholder values for the weekend since the restraunt doesn't open
    data = {"SAT": ":pizza:", "SUN": ":spaghetti:"}
    days = ("MON", "TUE", "WED", "THU", "FRI")
    current_day = days[0]
    for line in text.split("\n"):
        for day in days:
            if day in line:
                current_day = day

        data[current_day] = "{}{} ".format(data.get(current_day, ""), line)

    return data

def select_unicode_responses(text):
    """
    Returns the emoji for any words that exactly match the name of an emoji
    supported by python

    This currently allows Slack emoji that are specified using colons, it would
    be nice to allow any words in an up to date list of Slack's emoji and add
    colons to them automagically

    Would be nice to add phrase support
    """
    responses = []
    for word in text.split():
        # not sure if I want to use regex against a unicode data file unicode
        # or bruteforce this within python
        if word.startswith(":") and word.endswith(":") and len(word) > 2:
            responses.append(word)
            continue

        try:
            responses.append(unicodedata.lookup(word))
        except KeyError:
            pass

    return responses

def weekly():
    get_jpg(url)
    # Nice command that needs writing based off of get_string
    get_string_and_write_to_file()

def daily():
    # The file that was written to by the above
    with open(file_that_is_written_to_weekly) as f:
        text = f.read()

    #import pprint
    #pp = pprint.PrettyPrinter(indent=4)
    #pp.pprint(pull_info_out_by_day(text))
    day_data = pull_info_out_by_day(text)
    day = time.strftime('%a').upper()
    text = day_data[day].replace(" {} ".format(day), ' ')
    responses = select_unicode_response(text)
    # We need to store this in the cache file rather than printing it
    print(', '.join(responses))

def main(image_to_get_text_for):
    print(get_string(image_to_get_text_for))
    get_string_for_dir(os.path.join(output_dir, image_to_get_text_for.replace('.jpg', '')))

if __name__ == "__main__":
    output_dir = time.strftime('%X')
    main("menu.jpg")

# This needs a weekly cron to get the latest Menu.pdf.
#
# I think it is simplest to have a daily cron to check the responses and cache
# them
#
# The code to check the cached responses can be part of the dogsbot daemon

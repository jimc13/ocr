#!/usr/bin/env python3
from helpers import *
def main(image_to_get_text_for):
    print(get_string(image_to_get_text_for))
    get_string_for_dir(os.path.join(output_dir, image_to_get_text_for.replace('.jpg', '')))

if __name__ == "__main__":
    output_dir = time.strftime('%X')
    main('Menu.jpg')

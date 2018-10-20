# Set-up
```
sudo apt-get install tesseract-ocr
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

sudo vim /etc/ImageMagick-6/policy.xml
    <!-- <policy domain="coder" rights="none" pattern="MVG" /> -->
    <policy domain="coder" rights="read|write" pattern="PDF" />
    <policy domain="coder" rights="read|write" pattern="LABEL" />
```

# Main Source
https://medium.freecodecamp.org/getting-started-with-tesseract-part-i-2a6a6b1cf75e

might read https://medium.freecodecamp.org/getting-started-with-tesseract-part-ii-f7f9a0899b3f

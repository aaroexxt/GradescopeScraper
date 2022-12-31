# GradescopeScraper

Short Python script that scrapes all Gradescope data for a class

No idea why they don't have a "Download All" button it's really annoying

Inpsired by Python 2.x script written by YimengYang, found [here](https://github.com/YimengYang/gradescope)

## Instructions for Use

Download this directory, and `cd` into it

Then, install dependencies:

`pip3 install mechanize tqdm html2text bs4`

Finally, `cd` to the script directory and run it:

`python3 gradescope.py`

You will then be prompted for your Gradescope username and password in plaintext (these are not used for anything other then authenticating your account)

After answering `y` to confirm you want to download everything, the script will then download all of your files!

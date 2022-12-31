import mechanize
from tqdm import tqdm

try:
    from http.cookiejar import LWPCookieJar
except ImportError:
    from cookielib import LWPCookieJar
import html2text
from bs4 import BeautifulSoup
import os

# Settings (you can either specify these here or leave blank and you will be prompted later)
g_user = ""
g_pwd = ""

# Browser
br = mechanize.Browser()

# Cookie Jar
cj = LWPCookieJar()
br.set_cookiejar(cj)

# Browser options
br.set_handle_equiv(True)
br.set_handle_gzip(True)
br.set_handle_redirect(True)
br.set_handle_referer(True)
br.set_handle_robots(False)
br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)

br.addheaders = [('User-agent', 'Chrome')]

dir_path = os.path.dirname(os.path.realpath(__file__))

print("Gradescope scraper, by Aaron Becker (some credit to YimengYang)")
print("------------------------")
print("This script will create one folder per class, containing all of the files you've submitted for that class.")
print("Your current directory (that all the class folders will be created in) is: {}".format(dir_path))
print("------------------------")
print("Step 1) Logging into Gradescope and getting class list...\nYou will be prompted for your username and password if you haven't entered them already")
# The site we will navigate into, handling it's session
br.open('https://gradescope.com/login')
base_url = "https://gradescope.com"
# View available forms
for f in br.forms():
    # Select the second (index one) form (the first form is a search query box)
    br.select_form(nr=0)

    if not g_user:
        g_user = input("Enter your Gradescope username: ")
    if not g_pwd:
        g_pwd = input("Enter your Gradescope password: ")

    # User credentials
    br.form['session[email]'] = g_user
    br.form['session[password]'] = g_pwd

    # Login
    br.submit()

    soup = BeautifulSoup(br.open('https://gradescope.com/account').read(), "html.parser")
    
    courseBoxes = soup.find_all('a', {'class':'courseBox'})
    links = {}
    for c in courseBoxes:
        n = c.find("h3").text
        n = n.replace("/", " ")
        links[n] = c.get("href")

    print("Classes read from your Gradescope account:")
    for cName in links.keys():
        print(cName)

    if not input("Do you want to continue and download all content? (yY/nN)").lower() == "y":
        exit()
    
    print("Step 2) Downloading all content (this may take a while)...")
    
    for k,v in links.items():
        if not os.path.exists(k):
            os.mkdir(k)
        else:
            print("Dir {} exists, skipping".format(k))
            continue
        course_soup = BeautifulSoup(br.open(base_url+ v).read(), "html.parser")
        os.chdir(k)
        assignment_table = course_soup.find('table', {'class':'table'})
        assignment_links = {}
        for head in assignment_table.find_all("th"):
            a_res = head.find("a")
            if a_res:
                assignment_links[a_res.get("aria-label")] = a_res.get("href")

        print("{}'s assignments:".format(k))
        for aName in assignment_links.keys():
            print(aName.split(' ', 1)[1])
        print("Now downloading all assignments in '{}' (this may take a while)...".format(k))

        for name, l in tqdm(assignment_links.items()):
            assignment_soup = BeautifulSoup(br.open(base_url+l).read(), "html.parser")
            a_res = assignment_soup.find_all("a", {"class": "actionBar--action"})
            download_link = base_url + l + ".pdf"
            for a in a_res:
                tmp = a.get("href")
                if tmp:
                    download_link = base_url + tmp
                    break
            orig_filename = download_link.split("/")[-1]
            extension = orig_filename.split(".")[-1]
            name = name.replace("/", " ") 
            br.retrieve(download_link,'{}.{}'.format(name, extension))[0]
        os.chdir("../")
        print("Finished downloading all assignments for {}".format(k))

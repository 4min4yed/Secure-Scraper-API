import re
from playwright.sync_api import Page, expect
i=input("Enter job title or keyword to search: ")

def test_click_each_link(page: Page, i: str):
    page.goto("https://careers.ey.com/search/?createNewAlert=false&q="+i+"&optionsFacetsDD_customfield1=&optionsFacetsDD_country=&optionsFacetsDD_city=")
    links = page.query_selector_all("a")
    urls = set(link.get_attribute("href") for link in links)
    for url in urls:
        if "/ey/job" in str(url):
            url="https://careers.ey.com"+url
            print("URL:", url,":")
            page.goto(url)
            page.wait_for_load_state("load")
            #print("Apply here: ", page.locator("div.jobTitle a").get_attribute("href"))
            print("jobTitle: ", page.title().removesuffix("Job Details | EY"))
            print("Apply here: ","https://careers.ey.com/" + page.get_by_role("button", name=re.compile(r"apply\s*now", re.I)).first.get_attribute("href"))

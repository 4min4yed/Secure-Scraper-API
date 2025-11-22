import re
from playwright.sync_api import Page, expect, sync_playwright
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI() #ta3ml serveur API, w tdefini des routes api

class ScrapeRequest(BaseModel):
    keyword: str

def test_scrape_jobs(i: ScrapeRequest):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://careers.ey.com/search/?createNewAlert=false&q="+i.keyword+"&optionsFacetsDD_customfield1=&optionsFacetsDD_country=&optionsFacetsDD_city=")
        links = page.query_selector_all("a")
        urls = set(link.get_attribute("href") for link in links)
        s=[]
        for url in urls:
            if "/ey/job" in str(url):
                url="https://careers.ey.com"+url
                # print("URL:", url,":")
                page.goto(url)
                page.wait_for_load_state("load")
                #print("Apply here: ", page.locator("div.jobTitle a").get_attribute("href"))
                s.append({  
                    "JobURL": str(url),
                    "JobTitle": str(page.title().removesuffix("Job Details | EY")),
                    "Apply here" :str("https://careers.ey.com/" + page.get_by_role("button", name=re.compile(r"apply\s*now", re.I)).first.get_attribute("href"))})
        browser.close()
        return s

@app.post("/scrape")  #kif 7ad yposti 7aja 3al /scrape l'fct ta7tha te5dm

def scrape(req: ScrapeRequest):
    result= test_scrape_jobs(req)
    return {"keyword": req.keyword, "results": result}  #in FastAPI, whatever you return from your route function is automatically serialized to JSON and sent as the HTTP response to the client.


import pandas as pd
import requests
from bs4 import BeautifulSoup

def get_html(url, headers):
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    return None

def parse_jobs(html_data):
    soup = BeautifulSoup(html_data, 'html.parser')
    job_listings = soup.find_all('li', class_='list-group-item')
    jobs_data = []

    for job in job_listings:
        title = job.find('h2')
        job_id = job.get("id") if job else None
        company = job.find(class_="d-inline-block mt-1 mb-0 ng-star-inserted")
        types = job.find(class_="mr-1 mb-0 ng-star-inserted")
        lieu = job.find(class_="mr-3 mb-1 cc-font-size-small")
        date = job.find(class_="mb-0")
        jobs_data.append({"Titre": title, "Company": company, "Type": types, "Lieu": lieu, "Publication": date, "ID": job_id})

    return jobs_data

def create_dataframe(jobs_data):
    df_jobs = pd.DataFrame(jobs_data)
    return df_jobs#.iloc[::2]

def main():
    url = "https://www.meteojob.com/jobs/meteo?job=36692~ENTRY_LEVEL~INTERMEDIATE~SENIOR~EXPERT&location=2996944~30"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept-Language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    html_data = get_html(url, headers)
    if html_data:
        jobs_data = parse_jobs(html_data)
        df_jobs = create_dataframe(jobs_data)

import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

visited_urls = set()

def spider_urls(url, keyword):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        st.write(f"Request failed for URL: {url}")
        return

    if response.status_code == 200:
        st.write(f"Scraping URL: {url}")
        soup = BeautifulSoup(response.content, 'html.parser')
        a_tag = soup.find_all('a')
        urls = []
        for tag in a_tag:
            href = tag.get("href")
            if href is not None and href != "":
                urls.append(href)

        for urls2 in urls:
            if urls2 not in visited_urls:
                visited_urls.add(urls2)
                url_join = urljoin(url, urls2)
                if keyword in url_join:
                    st.write(f"Found keyword '{keyword}' at: {url_join}")
                    spider_urls(url_join, keyword)

st.title("Web Scraping App")

# Input for the starting URL
starting_url = st.text_input("Enter the starting URL:")

# Input for the keyword
keyword = st.text_input("Enter the keyword to search for:")

if st.button("Start Scraping"):
    visited_urls.clear()
    spider_urls(starting_url, keyword)

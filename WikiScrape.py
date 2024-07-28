import requests
from bs4 import BeautifulSoup
import validators
import re

def valid_wikipedia_link(url):
    #Validate if the URL is a valid Wikipedia link
    return validators.url(url) and 'wikipedia.org' in url

def get_wikipedia_links(url):
    #Get unique Wikipedia links from the given URL
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = set()

    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/wiki/') and not re.search(r'(:|%|\/\w+\/)\w*\.\w*', href):
            full_url = f"https://en.wikipedia.org{href}"
            links.add(full_url)
    
    return links

def scrape_wikipedia(start_url, n):
    #Scrape Wikipedia links up to n cycles
    if not valid_wikipedia_link(start_url):
        raise ValueError("Invalid Wikipedia URL")
    if not (1 <= n <= 3):
        raise ValueError("n must be an integer between 1 and 3")
    
    visited = set()
    to_visit = [start_url]
    all_links = set()

    for cycle in range(n):
        if not to_visit:
            break
        
        next_to_visit = []
        
        for url in to_visit:
            if url in visited:
                continue
            
            visited.add(url)
            print(f"Scraping {url}")
            new_links = get_wikipedia_links(url)
            new_links = new_links - visited
            
            if len(all_links) >= 10:
                break
            
            if len(all_links) + len(new_links) > 10:
                new_links = set(list(new_links)[:10 - len(all_links)])
            
            all_links.update(new_links)
            next_to_visit.extend(new_links)
        
        to_visit = next_to_visit
    
    return all_links

def main():
    start_url = input("Enter a Wikipedia URL: ").strip()
    n = int(input("Enter the number of cycles 1 to 3: ").strip())
    
    try:
        links = scrape_wikipedia(start_url, n)
        print("\nUnique Wikipedia links found:")
        for link in links:
            print(link)
    except ValueError as e:
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")

if __name__ == "__main__":
    main()
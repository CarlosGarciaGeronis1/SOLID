import requests
import re
import csv
from bs4 import BeautifulSoup


class IMDBScraper:
    def __init__(self, url):
        self.url = url

    def scrape(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'lxml')
        movies = soup.select('td.titleColumn')
        links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
        crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
        ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
        votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]
        return self._process_data(movies, links, crew, ratings, votes)

    def _process_data(self, movies, links, crew, ratings, votes):
        movie_data = []
        for index in range(0, len(movies)):
            movie_string = movies[index].get_text()
            movie = (' '.join(movie_string.split()).replace('.', ''))
            movie_title = movie[len(str(index)) + 1:-7]
            year = re.search('\((.*?)\)', movie_string).group(1)
            place = movie[:len(str(index)) - (len(movie))]
            data = {"movie_title": movie_title,
                    "year": year,
                    "place": place,
                    "star_cast": crew[index],
                    "rating": ratings[index],
                    "vote": votes[index],
                    "link": links[index],
                    "preference_key": index % 4 + 1}
            movie_data.append(data)
        return movie_data


class CSVWriter:
    def __init__(self, filename, data):
        self.filename = filename
        self.data = data

    def write_to_csv(self):
        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=self.data[0].keys())
            writer.writeheader()
            for row in self.data:
                writer.writerow(row)


if __name__ == '__main__':
    imdb_scraper = IMDBScraper('http://www.imdb.com/chart/top')
    movie_data = imdb_scraper.scrape()
    csv_writer = CSVWriter('movie_results.csv', movie_data)
    csv_writer.write_to_csv()

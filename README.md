# Elasticsearch based Search Engine

## Our workflow

- 


## Salient features of our engine

- Scraping
    - Scraped ~7000 documents using ``https://en.wikipedia.org/wiki/Science_fiction_film`` as a seed using `BeautifulSoup`
    - Customizable depth
    - Saved in `.json` format with `paragraphs`, `table of contents` and `title` as fields

- Tokenization
    - Standard tokenizer
    - Token filters: `stop`, `lowercase`, `snowball stemmer`

- Support for `BM25` and `Jelinek-Mercer` Language Model

- Retrieval of top `k` relevant documents in order

- Support for `conjunctive` and `disjunctive` queries

- User interface with the following features
    - Dropdown keyword suggestions based on Levenstein distance using Fuzzy search
    - Snippets that displays the most relevant fragments built using `unified highlighter`
    - Interface to change between the models and modes as per user's requirements
    - Displaying results as clickable links for better access



- Pointers
    - _box-office_ vs _box office_
    - hollywood moon blockbuster
import urllib.request, json

def find_books(search_request):
    books = {}
    books['books'] = []
    link = 'https://www.googleapis.com/books/v1/volumes?q='
    link += search_request.replace(" ", "_")
    print(link)
    with urllib.request.urlopen(link) as url:
        data = json.loads(url.read().decode())
        try:
            for p in data['items']:
                volumeInfo = p['volumeInfo']
                try:
                    thumbnail = volumeInfo['imageLinks']['thumbnail']
                except KeyError:
                    thumbnail = None
                books['books'].append({
                    'title': volumeInfo.get('title'),
                    'authors': volumeInfo.get('authors'),
                    'published_date': volumeInfo.get('publishedDate'),
                    'categories': volumeInfo.get('categories'),
                    'average_rating': volumeInfo.get('averageRating'),
                    'ratings_count': volumeInfo.get('ratingsCount'),
                    'thumbnail': thumbnail
                    })
            return(books['books'])
        except KeyError:
            pass

from requests import get, post, delete


url = 'http://localhost:8080/api/'
print(get(f'{url}books').json())
print(get(f'{url}reviews').json())
post(f'{url}reviews', json={'author': 1, 'book': 1, 'text':'ddd', 'rate':5.0})
print(get(f'{url}reviews').json())


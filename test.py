def main_page_books(books):
    new = []
    last = 0
    for i in range(len(books)):
        if i % 3 == 0 and i != 0:
            new.append(books[i - 3:i])
            last = i
    if len(books) % 3 != 0:
        new.append(books[-(len(books) - last):])
    return new

print(main_page_books([1, 2, 3, 4, 5, 6, 7, 8]))

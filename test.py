def main_page_books(books):
    new = []
    last = 0
    i = 0
    a = []
    for i in range(len(books)):
        a.append(books[i])
        if (i + 1) % 7 == 0 or (i + 1) == len(books):
            new.append(a)
            a = []
    return new

print(main_page_books([1, 2, 3, 4, 5, 6, 7, 8]))
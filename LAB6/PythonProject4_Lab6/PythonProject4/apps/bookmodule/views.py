from django.shortcuts import render
from .models import Book


def index(request):
    name = request.GET.get("name") or "world!"
    return render(request, "bookmodule/index.html", {"name": name})


def index2(request, val1=0):
    from django.http import HttpResponse
    return HttpResponse("value1 = " + str(val1))


# ── Lab 6: HTML forms & in-memory book search ───────────────────────────────


def __getBooksList():
    """
    Return a static list of sample books (dicts with id, title, author).
    Used by searchBooks instead of the database for this lab exercise.
    """
    book1 = {
        "id": 12344321,
        "title": "Continuous Delivery",
        "author": "J.Humble and D. Farley",
    }
    book2 = {
        "id": 56788765,
        "title": "Reversing: Secrets of Reverse Engineering",
        "author": "E. Eilam",
    }
    book3 = {
        "id": 43211234,
        "title": "The Hundred-Page Machine Learning Book",
        "author": "Andriy Burkov",
    }
    return [book1, book2, book3]


def searchBooks(request):
    """
    GET: render the search form (search.html).
    POST: read keyword + checkbox options, filter __getBooksList(), render bookList.html.
    URL: /books/search (see libraryproject/urls.py + apps.bookmodule.urls).
    """
    if request.method == "POST":
        # Keyword from <input name="keyword">; strip so spaces alone do not search.
        keyword = (request.POST.get("keyword") or "").strip().lower()
        # Checkboxes only appear in POST when checked; value defaults to "on" in browsers.
        search_in_title = request.POST.get("option1")
        search_in_author = request.POST.get("option2")

        books = __getBooksList()
        filtered = []

        if keyword:
            for book in books:
                title_lower = book["title"].lower()
                author_lower = book["author"].lower()
                match = False
                # Respect selected fields: title and/or author.
                if search_in_title and keyword in title_lower:
                    match = True
                if not match and search_in_author and keyword in author_lower:
                    match = True
                if match:
                    filtered.append(book)

        return render(
            request,
            "bookmodule/bookList.html",
            {
                "books": filtered,
                "from_search": True,
                "keyword": keyword,
                "search_in_title": bool(search_in_title),
                "search_in_author": bool(search_in_author),
            },
        )

    # GET – show empty search form
    return render(request, "bookmodule/search.html")


def simple_query(request):
    mybooks = Book.objects.filter(title__icontains='and')
    return render(request, 'bookmodule/bookList.html', {'books': mybooks})


def complex_query(request):
    mybooks = Book.objects.filter(author__isnull=False).filter(title__icontains='and').filter(edition__gte=2).exclude(price__lte=100)[:10]
    if len(mybooks) >= 1:
        return render(request, 'bookmodule/bookList.html', {'books': mybooks})
    else:
        return render(request, 'bookmodule/index.html')

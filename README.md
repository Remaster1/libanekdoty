<h1 align="center"> libanekdoty</h1>
<p align="center">
    <i>Library for parse anekdoty.ru</i>
</p>

<h2>Examples:</h2>

```python
# Get all categories
from libanekdoty.categories import Categories
categories = Categories().get_all_categories()
```

```python
# Get random category
from libanekdoty.categories import Categories
category = Categories().get_random_category()
```

```python
# Get all jokes from random category
from libanekdoty.categories import Categories
from libanekdoty.jokes import Jokes
category = Categories().get_random_category()
jokes = Jokes(category["url"]).get_all_jokes()
```

```python
# Get jokes from selected page in random category
from libanekdoty.categories import Categories
from libanekdoty.jokes import Jokes
category = Categories().get_random_category()
jokes = Jokes(category["url"]).get_jokes_from_selected_page(2)
```


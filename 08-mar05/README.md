# Transform the products in a list of dictionaries in to an HTML table

The file `advanced_tools.p`y will show you how to do the same in an "easier" way but is out of the scope of this course.

You can convert a list of dictionaries into an HTML string using a for loop in Python. This is commonly done to format data as an HTML list (`\<ul\> `or `\<ol\>`) or table (`\<table\>`). 

#### Example: Creating an HTML Unordered List

This approach iterates through each dictionary in the list and formats each entry as a list item (\<li\>) with bold keys and regular values. 

```Python
    data = [
        {'name': 'Alice', 'age': 30, 'city': 'New York'},
        {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
        {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
    ]

    html_string = "<ul>\n"

    for item in data:
        html_string += "  <li>\n"
        # Iterate through key-value pairs in the current dictionary
        for key, value in item.items():
            html_string += f"    <b>{key.capitalize()}:</b> {value}<br>\n"
        html_string += "  </li>\n"

    html_string += "</ul>"

    print(html_string)

```
#### Output: 

```Bash
<ul>
  <li>
    <b>Name:</b> Alice<br>
    <b>Age:</b> 30<br>
    <b>City:</b> New York<br>
  </li>
  <li>
    <b>Name:</b> Bob<br>
    <b>Age:</b> 25<br>
    <b>City:</b> Los Angeles<br>
  </li>
  <li>
    <b>Name:</b> Charlie<br>
    <b>Age:</b> 35<br>
    <b>City:</b> Chicago<br>
  </li>
</ul>

```

#### Example: Creating an HTML Table

For more structured data, generating an HTML table is often better. This example creates a table with headers derived from the keys of the first dictionary. 

```Python
data = [
    {'name': 'Alice', 'age': 30, 'city': 'New York'},
    {'name': 'Bob', 'age': 25, 'city': 'Los Angeles'},
    {'name': 'Charlie', 'age': 35, 'city': 'Chicago'}
]

html_table_string = "<table>\n  <thead>\n    <tr>"

# Generate table headers (assuming all dictionaries have the same keys)
for key in data[0].keys():
    html_table_string += f"<th>{key.capitalize()}</th>"
html_table_string += "</tr>\n  </thead>\n  <tbody>\n"

# Generate table rows
for item in data:
    html_table_string += "    <tr>"
    for value in item.values():
        html_table_string += f"<td>{value}</td>"
    html_table_string += "</tr>\n"

html_table_string += "  </tbody>\n</table>"

print(html_table_string)

```

#### Output:

```Bash
<table>
  <thead>
    <tr><th>Name</th><th>Age</th><th>City</th></tr>
  </thead>
  <tbody>
    <tr><td>Alice</td><td>30</td><td>New York</td></tr>
    <tr><td>Bob</td><td>25</td><td>Los Angeles</td></tr>
    <tr><td>Charlie</td><td>35</td><td>Chicago</td></tr>
  </tbody>
</table>

```

Continuing with the past Daisy UI exercise:

 * Use a html file with an empty body tag and the Daisy UI links.
 * Create the html table using a for loop and the data optained from the freshco data.
 * Select a Daisy UI table component of yours
 * Use name, price, and url of the picture
 * Display the url links (`href="link"`) as a pictures with a size of 50 x 50 pixels (`witdth="50" height="50"` adjust as needed) in a html img tag.
 * Add a h1 tag on top of the table.
 * Add 2 square buttons in a new column to the right of the pictures, a red called delete and a green one called edit.
 * Write the code manually with one of 2 rows, until it looks good to your and then go over all the items and create the full string table.
 * Insert the table string in the body of the html file.
 * Read and write files as necessary. 
 * Check the `pandas...html` files in a browser as ugly reference of what should obtain, use the Daisy UI theme of your choice.
 * Deliver the python file in a new repo and provide a link to github pages, don't forget the readme.
 * Feel free to use more Daisy UI elements.

import re

from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

# Returns a list of all names of encyclopedia entries.
def list_entries():
    _, filenames = default_storage.listdir("entries")
    return list(sorted(re.sub(r"\.md$", "", filename)
                for filename in filenames if filename.endswith(".md")))

# Saves an encyclopedia entry, given its title and Markdown
# content. If an existing entry with the same title already exists,
# it is replaced.
def save_entry(title, content):
    filename = f"entries/{title}.md"
    if default_storage.exists(filename):
        default_storage.delete(filename)
    default_storage.save(filename, ContentFile(content))

# Retrieves an encyclopedia entry by its title. If no such
# entry exists, the function returns None.
def get_entry(title):
    try:
        f = default_storage.open(f"entries/{title}.md")
        return f.read().decode("utf-8")
    except FileNotFoundError:
        return None
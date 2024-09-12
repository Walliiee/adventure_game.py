import wikipedia as wiki

print(wiki.summary("Python programming language"))
print(wiki.search("Buffalo Bills"))
print(wiki.page("Buffalo Bills").content)
print(wiki.search("Buffalo Bills", results=2))

# https://wikipedia.readthedocs.io/en/latest/
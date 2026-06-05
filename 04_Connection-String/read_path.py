import os

# Die Recherche-Antwort: 
# In Python liest man Umgebungsvariablen mit os.environ.get("NAME") aus.

print("--- Aufgabe 4.1: PATH Variable ---")
path_variable = os.environ.get("PATH")

if path_variable:
    print("Inhalt der PATH-Variable:")
    print(path_variable)
else:
    print("Variable PATH wurde nicht gefunden.")
Wie werden die Documents verbunden?
GridFS nutzt zwei Collections: fs.files (für Metadaten) und fs.chunks (für die Daten). In der fs.chunks-Collection gibt es ein Feld namens files_id. Dieses Feld verweist auf die _id in der fs.files-Collection. So weiss MongoDB, welche Datenstücke zu welcher Datei gehören.

Codierung der Rohdaten:
Die Rohdaten werden als Binärdaten (BSON Binary) gespeichert. Sie werden nicht als Text oder String interpretiert, sondern Byte für Byte genau so, wie sie in der Datei vorliegen.
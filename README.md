# e-book-spider
crawler scripts to create books for my eReader

## 小說狂人

### EPUB File

Creates EPUB file with Title, Author, Description, and Chapters
```
python czBooks2epub.py https://czbooks.net/n/u866i
```
produces `book.epub`


### Text File

Dumps all chapters into one text file
```
python czBooks2txt.py https://czbooks.net/n/u866i
```
produces `{title}by{author}.txt`


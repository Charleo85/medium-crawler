# Medium Crawler
This crawler has built up the following dataset based on Medium.com with ground truth sentence and review correspondence.

You may contact Charlie Wu at jw7jb@virginia.edu to obtain the dataset

Crawler environment requirement 
- python 3.6
- postgresql environment on MacOS/Linux

To query data:
```
psql
```

Datebase Structure:

- ArticleTable
 
| Field   | Type      |    Info                |
| :-------------:|:-------------:| :----------------------|
| articleID           | SERIAL PRIMARY KEY |                        |
| articleMediumID     | text      |                        |
| articleTitle        | text      |                        |
| articleContent      | text      |                        |
| tag                 | varchar(300)     |                        |
| articleTime         |  timestamp        |                        |
| numberLikes         |   int           |                        |
| authorID            | int      |    link to Author Table|

- CommentTable
 
| Field   | Type      |  Info                    |
| :-------------:|:-------------:| :------------------------|
| commentID     | SERIAL PRIMARY KEY |                          |
| commentName   | text               |                          |
| commentContent| text               |                          |
| commentTime   | timestamp          |                          |
| authorID      | int                |                          |
| numberLikes   | int                |                          |
| articleID     | int                |  link to Article Table   |
| corrStnID     | varchar(300)       |  Match with SentenceTable|
***To add corrStnID instead of stnName***

- AuthorTable
 
| Field   | Type      | Info  |
| :-------------:|:-------------:| :---- |
| authorID      | SERIAL PRIMARY KEY |  |
| authorName    | varchar(300)       |    |
| authorMediumID| varchar(300)       |     |
| authorUserName| varchar(300)       |     |
| bio           | text               |     |

- SentenceTable

| Field   | Type      | Info  |
| :-------------:|:-------------:| :---- |
| stnID         |SERIAL PRIMARY KEY |  |
| stnName       |varchar(300)       |    |
| content       |text               |     |
| articleID     | int                |   link to Article Table  |



Disclaimer: The development is for academic use only. The developer shall not be responsible for any consequence from the user behavior of this program.
For the use of dataset, acknowledgement would be appreciated.



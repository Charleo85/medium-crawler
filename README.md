# Medium Crawler
This crawler has built up the following dataset based on Medium.com with ground truth sentence and review correspondence.

You may contact Charlie Wu at jw7jb@virginia.edu to obtain the dataset

Crawler environment requirement 
- python 3.6
- postgresql environment on MacOS/Linux

To query data:
```
psql medium
# \dt
# select $field from $table;
```

Datebase Table Structure:

- article
 
| Field   | Type      |    Info                |
| :-------------:|:-------------:| :----------------------|
| articleID           | SERIAL PRIMARY KEY |                        |
| mediumID     | varchar(300)      |                        |
| title        | text      |                        |
| highlight      | text      |                        |
| tag                 | varchar(300)     |                        |
| postTime         |  timestamp        |                        |
| numberLikes         |   int           |                        |
| corrAuthorID            | int      |    link to Author |

- comment

| Field   | Type      |  Info                    |
| :-------------:|:-------------:| :------------------------|
| commentID     | SERIAL PRIMARY KEY |                          |
| MediumID   | varchar(20)    |                          |
| Content| text               |                          |
| commentTime   | timestamp          |                          |
| numberLikes   | int                |                          |
| corrAuthorID      | int                |  link to Author  |
| corrArticleID     | int                |  link to Article   |
| corrStnID     | int       |  link to Sentence|

- author
 
| Field   | Type      | Info  |
| :-------------:|:-------------:| :---- |
| authorID      | SERIAL PRIMARY KEY |  |
| name    | varchar(50)       |    |
| mediumID| varchar(20)       |     |
| userName| varchar(50)       |     |
| bio           | text               |     |

- sentence

| Field   | Type      | Info  |
| :-------------:|:-------------:| :---- |
| stnID         |SERIAL PRIMARY KEY |  |
| MediumID       |varchar(10)       |    |
| content       |text               |     |
| corrArticleID     | int                |   link to Article  |

Disclaimer: The development is for academic use only. The developer shall not be responsible for any consequence from the user behavior of this program.
For the use of dataset, acknowledgement would be appreciated.



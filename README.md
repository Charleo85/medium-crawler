# Medium Crawler
This crawler has built up the following dataset based on Medium.com with ground truth sentence and review correspondence.

You may contact Charlie Wu at jw7jb@virginia.edu to obtain the dataset

Crawler environment requirement
- python 3.6
- postgresql environment on MacOS/Linux

Download chromedriver for your environment [here](https://github.com/SeleniumHQ/selenium/wiki/ChromeDriver) to project directory

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
| recommends       | int      |                        |
| tags             | varchar(300)     |  list of tags        |
| postTime         |  timestamp        |                        |
| numLikes         |   int           |                        |
| corrAuthorID     | int      |    link to author |

- comment

| Field   | Type      |  Info                    |
| :-------------:|:-------------:| :------------------------|
| commentID     | SERIAL PRIMARY KEY |                          |
| selfArticleID     | int      |  link to article   |
| corrArticleID     | int      |  link to article   |
| corrHighlightID   | int      |  link to highlight|

The detailed info of a comment is stored inside an article model as field **selfArticleID**

- author

| Field   | Type      | Info  |
| :-------------:|:-------------:| :---- |
| authorID      | SERIAL PRIMARY KEY |  |
| name    | varchar(50)       |    |
| mediumID| varchar(20)       |     |
| username| varchar(50)       |     |
| bio     | text               |     |

- sentence

| Field   | Type      | Info  |
| :-------------:|:-------------:| :---- |
| stnID         |SERIAL PRIMARY KEY |  |
| mediumID      |varchar(10)       |    |
| content       |text               |     |
| corrArticleID     | int           |   link to article  |

- highlight

| Field   | Type      | Info  |
| :-------------:|:-------------:| :---- |
| highlightID         |SERIAL PRIMARY KEY |  |
| content       |text               |     |
| numLikes      |int               |     |
| corrArticleID | int     |  link to article |
| corrStnMediumIDs | varchar(300) |  list of highlighted sentence|

Disclaimer: The development is for academic use only. The developer shall not be responsible for any consequence from the user behavior of this program.
For the use of dataset, acknowledgement would be appreciated.

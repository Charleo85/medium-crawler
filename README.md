# Medium Crawler
Output File Structure:
- data
  - article
     - 'name': string, --filename
     - 'parent': string,
     - 'child': string,
     - 'title': string,
     - 'content': string,
     - 'author': author,
     - 'sentences': string[],
     - 'tag': string[],
     - 'timestamp': timestamp,
  - comment
     - 'name': string, --filename,
     - 'parent': string,
     - 'child': string,
     - 'title': string,
     - 'content': string,
     - 'id': string,
     - 'creatorid': string,
     - 'username': string,
     - 'timestamp': timestamp,
  - truth: comments/article correspondence
     - 'name': string, --filename,
     - 'parent': string
     - 'child': string,
     - 'title': string,
     - 'content': string, 
     - 'sentenceid': string,
     - 'commentid': string,
     - 'creatorid': string,
- cache
  - log
  
    std/err outputs
  - html
  
    article html file
  - json
  
    http reponse json
  - variable
  
    pickle file for runtime variable snapshots 

Disclaimer: The development is for academic use only. The developer shall not be responsible for any consequence from the user behavior of this program.
For the use of dataset, acknowledgement would be appreciated.

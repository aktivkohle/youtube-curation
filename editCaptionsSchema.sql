# This will go into the main schema file and this file will be deleted if
# this method ends up working. 
# The following will be used to save each of the vectors to a file before 
# committing to sql
# https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.sparse.save_npz.html
# otherwise if there are performance issues can try one of these instead:
# https://stackoverflow.com/questions/8955448/save-load-scipy-sparse-csr-matrix-in-portable-data-format

ALTER TABLE youtubeProjectDB.captions ADD tfidfVector BLOB AFTER wordCount;

# It is vitally important that the same fixed vocabulary is used to create each of these 
# vectors. At the moment probably a dictionary with 429429 entries. 
# Each sparse matrix creates a file of about 1kB. 
# BLOB will store up to about 65kB whereas TINYBLOB stores 256 Bytes 
# Hence the decision to go with BLOB


# Oh no!
# pymysql.err.DataError: (1406, "Data too long for column 'tfidfVector' at row 1")

ALTER TABLE youtubeProjectDB.captions DROP COLUMN tfidfVector;

ALTER TABLE youtubeProjectDB.captions ADD tfidfVector MEDIUMBLOB AFTER wordCount;


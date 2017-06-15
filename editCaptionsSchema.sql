# This will go into the main schema file and this file will be deleted if
# this method ends up working. 
# The following will be used to save each of the vectors to a file before 
# committing to sql
# https://docs.scipy.org/doc/scipy-0.19.0/reference/generated/scipy.sparse.save_npz.html
# otherwise if there are performance issues can try one of these instead:
# https://stackoverflow.com/questions/8955448/save-load-scipy-sparse-csr-matrix-in-portable-data-format

ALTER TABLE youtubeProjectDB.captions ADD tfidfVector BLOB AFTER wordCount;
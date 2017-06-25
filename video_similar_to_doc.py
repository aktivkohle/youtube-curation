from PullVectorsFromSQLandRunSimilarity import p, nth_similar_tuple
from fit_one_document import pipe_fit_transform       # my own program

number_similar_videos = 5

def similar_to_doc(new_document):
    p_new = pipe_fit_transform(new_document)
    new_similarity_row = ((p * p_new.T).A.T)[0]  # remove extra (inappropriate) dimension
    similar_list = []
    for i in range(5):
        similar_list.append(nth_similar_tuple(i, new_similarity_row))
    return similar_list
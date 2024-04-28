from langchain_chroma import Chroma


def split_text(text):
    splitted_text = text.split("\n$$$\n")
    return splitted_text


def build_chroma_data(splitted_text, chroma_data_path, embeddings):
    Chroma.from_texts(splitted_text, embeddings, persist_directory=chroma_data_path)


def similarity_search(chroma_data_path, openai_response, embeddings):
    db = Chroma(persist_directory=chroma_data_path, embedding_function=embeddings)
    similarities = db.similarity_search(openai_response)
    best_match_content = similarities[0].page_content
    return best_match_content

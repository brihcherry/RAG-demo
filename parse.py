import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.document_loaders import Docx2txtLoader

'''
finds all documents in the specified directory, including nested folders, and 
returns lists containing the name and path of each file.

@param source_dir: string containing the source directory that should be searched.
    The source directory should be a subdirectory of the directory containing the 
    rest of the program; in other words, it should be a folder residing in the same place
    as the python scripts

@return a list of the path of each file relative to the location of the python script
@return a list of the name of each file corresponding to the same index in paths

'''
def find_documents(source_dir: str):
    paths = []
    filenames = []

    for root, _, files in os.walk(source_dir):
        for file_name in files:
            print("Found: " + file_name)
            file_extension = os.path.splitext(file_name)[1]
            source_file_path = os.path.join(root, file_name)
            if file_extension == ".pdf" or file_extension == ".docx":
                paths.append(source_file_path)
                filenames.append(file_name)
    
    return paths, filenames


'''
Loads and stores each document specified in the paths list as a dictionary object representing a document, 
which can be stored in the chroma DB we want to use. For now, this method ONLY reads pdf and docx files. 
In addition, pdf files are automatically split by page into separate document objects, and docx files
are automatically split according to the default parameters in RecursiveTextSplitter (the default splitter
for load_and_split). The pdf documents therefore contain 'source' and 'page' metadata, while the docx
metadata contains only 'source'. In both cases, 'source' contains the full relative path to the file 
that the document was extracted from.

@param paths: a list of path strings from this file to the file to be read
@param filenames: a list of file name strings corresponding to each file that will be read from the paths list

@return documents: a list of dictionaries that were extracted and split from the files in paths.
    each item in the list is a dictionary object:
    metadatas - another dictionary including 'source' and, for pdfs, 'page', each strings
    page_content - a string containing the text that was extracted from the original file. 

    so, documents[0] might look like :
        page_content:'here is the text contained in the file' metadata={'source':'path/to/file/'}
    and to extract the source from the metadata of an item would require something like:
        documents['metadatas'][0][idx]['source']

'''
def load_documents(paths: list, filenames: list):
    documents = []
    for idx, file_path in enumerate(paths):
        file_name = filenames[idx]
        file_extension = os.path.splitext(file_name)[1]

        if file_extension == ".pdf":
            loader = PyPDFLoader(file_path)
            these_docs = loader.load()
            documents = documents + these_docs

        elif file_extension == ".docx":
            loader = Docx2txtLoader(file_path)
            these_docs = loader.load_and_split()
            documents = documents + these_docs

        else:
            print(f"{file_name} is not a pdf or docx file")
    
    return documents



Program can be run from run.ipynb. 

The program is designed to process word documents and pdf files stored in SOURCE_DIRECTORY; there's currently a PDF of a physics textbook in the directory. The program reads the files in the directory, stores them in a Chroma vector database using a custom embedding function, then retrieves relevant information and uses it to prompt an LLM. 

This program runs locally, without internet access. However, it requires that oLLaMA be installed on the machine, or at least some other local LLM model. The current setup requires oLLaMA but this program can be modified to run without it, if necessary.

requirements.txt contains a list of some of the requirements, but there may be dependencies that aren't listed, especially because the program requires oLLaMA or another model.
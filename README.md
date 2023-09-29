# Poor Man's Vector Database

Works specifically with [LM Studio](https://github.com/lmstudio-ai).  It simply extracts text from a document (only pdf, docx, and txt though), cleans it a little and send you query and the text extracted to LM Studio for an answer.  This simulates a vector database, but in reality just appends all of the extracted text to a user's query and sends both to the LLM for a response.

* Download the repo files.

* Create virtual environment
```
python -m venv .
```

* Activate Virtual Environment
```
.\Scripts\activate
```

* Upgrade Pip
```
python -m pip install --upgrade pip
```

* Install Requirements
```
pip install -r requirements.txt
```

* Run program
```
python gui.py
```

# Contact

All suggestions (positive and negative) are welcome.  "bbc@chintellalaw.com" or feel free to message me on the [LM Studio Discord Server](https://discord.gg/aPQfnNkxGC).

### Screenshots:

![Screenshot 1](https://github.com/BBC-Esq/Chat_Doc_LM_Studio/raw/main/esq1.png)
![Screenshot 2](https://github.com/BBC-Esq/Chat_Doc_LM_Studio/raw/main/esq2.png)

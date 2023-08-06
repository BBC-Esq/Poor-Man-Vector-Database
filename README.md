## Introduction

Works specifically with [LM Studio](https://github.com/lmstudio-ai), so check it out and join the Discord channel as well!

I call this "POOR MAN'S" chatting with documents because it's not a vector database, it's not a normal database, it's not whatever the heck the Faiss library is...no...not even close.  It's actually simply extracting text from a document (only pdf, docx, and txt though), cleaning it a little (but not very well), and attaching to your query.

Works surprisingly well though.  ;-)  Enjoy!

### Instructions:

1. Download the `.exe` and simply click to run.
2. Install and get running LM Studio. Activate server mode. Make sure that the server information is listening on: `http://localhost:1234/v1` otherwise you'll have to modify "chat.py" accordingly.
3. If you don't use the `.exe`, you can simply run "gui.py."

Thanks for stopping by.

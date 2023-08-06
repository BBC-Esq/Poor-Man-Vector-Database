## Introduction

Works specifically with [LM Studio](https://github.com/lmstudio-ai), so check it out and join the Discord channel as well!

I call this "POOR MAN'S" chatting with documents because it's not a vector database...it's not a normal database...it's not whatever the heck the Faiss library is...no...not even close.

It operates by simply extracting text from a document (only pdf, docx, and txt though), cleaning the text a little (but not too much, that would require more time and effort), and attaching the cleaned text to a user's query before sending it to the LLM.

Works surprisingly well though. 😄 Enjoy!

### Instructions:

1. Download the .exe and simply click to run.
2. Install and get running LM Studio
3. Activate server mode and make sure that the server information is listening on: `http://localhost:1234/v1` otherwise you'll have to modify "chat.py" accordingly.

You can also just run gui.py instead of using the .exe but then you have to worry about installing dependencies."

Thanks for stopping by.

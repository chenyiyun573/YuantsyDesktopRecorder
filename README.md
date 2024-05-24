On Mac M1

```
python3 -m venv .venv
.venv/bin/activate
python3 -m pip install -r requirements.txt
```
On windows
```
python3 -m venv .venv
.venv/Scripts/activate
python -m pip install -r requirements.txt
```


pyinstaller --onefile --windowed --icon=favicon.ico recorder.py


20240523 16:53 
Complete the first version of recorder. I found mouse move contains too much screenshots which will slow down the PC greatly so I commented the mouse move screenshot out.


20240523 22:51
Add GPT4.py, for mac and linux:
```
export GPT4V_KEY="your_actual_api_key_here"
```
For windows:
```
setx GPT4V_KEY "your_actual_api_key"
```


20240523 23:30
Add GPT4o.py, on windows if use environ
```
setx AZURE_OPENAI_API_KEY "REPLACE_WITH_YOUR_KEY_VALUE_HERE" 
setx AZURE_OPENAI_ENDPOINT "REPLACE_WITH_YOUR_ENDPOINT_HERE"
```



20240524 01:23
GPT4.py works with image uploaded. 

20240524 02:41 PT
GPT4o.py works, simple_agent to control the laptop using GPT4o works.
But I found it cannot know the position where to click precisely. 
This version of code is stored as version 1.0.0

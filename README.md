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


# upindia-dl
Python script to get direct download link from upindia.mobi or uploadfile.cc or upload.mobi

## Dependencies
* requests

## Usage
```python
from upindia_dl import get_direct_download_link

url = "https://uploadfile.cc/444369/lhHgcsP"
direct_download_link = get_direct_download_link(url)
print(direct_download_link)
```

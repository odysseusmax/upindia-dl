import re
import logging
import urllib.parse

import requests

logger = logging.getLogger('upindia_dl')

def get_direct_download_link(url):
  REGEX = r'(http[s]*://(?:upindia|uploadfile|upload)\.(?:cc|mobi)+/\d{6}/\S{7})'
  match = re.findall(REGEX, url)
  if not match:
    return "The provided link do not match with the standard format."
  
  session = requests.Session()
  url = match[0]
  logger.debug(f"Matched url: {url}")
  file_id, file_code = url.split('/')[-2:]
  logger.debug(f"file_code: {file_code}, file_id: {file_id}")
  url_parts = urllib.parse.urlparse(url)
  req = session.get(url)
  page_html = req.text
  itemlink = re.findall(r'class="download_box_new[^"]*".*itemlink="([^">]+)"', page_html)
  if not itemlink:
    return "File does not exist!"
  
  itemlink = itemlink[0]
  itemlink_parsed = urllib.parse.parse_qs(itemlink)
  file_key = itemlink_parsed['down_key'][0]
  logger.debug(f"file_key: {file_key}")
  params = {
    'file_id':file_id,
    'file_code':file_code,
    'file_key':file_key,
    'serv':1
  }
  req_url = url_parts.scheme + '://' +  url_parts.netloc + "/download"
  r = session.head(req_url, params=params)
  dl_url = r.headers.get('location', None)
  if dl_url is None:
    return "This file cannot be downloaded at this moment!"
  logger.debug(dl_url)
  return dl_url

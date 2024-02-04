import requests
import json
from urllib.parse import unquote

try:
  agnt='Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
  
  url='https://api.alerts.in.ua/v3/alert_events/recent.json'
  r=requests.get(url, headers={'User-Agent': agnt})

  j=json.loads(r.text)

  for it in j['alert_events']:
    if ('m' not in it or 'nt' not in it) and 'su' in it:
      rt=requests.get(it['su'], headers={'User-Agent': agnt})

      trBody=rt.text
      
      titleIdenTag = "property=\"og:title\""
      titleStartTag = "content=\""
      titleCloseTag = "\">"

      msgIdenTag = "property=\"og:description\""
      msgStartTag = "content=\""
      msgCloseTag = "\">"

      i = trBody.index(titleIdenTag)
      i1 = trBody.index(titleStartTag, i) + len(titleStartTag)
      i2 = trBody.index(titleCloseTag, i1)
      title = trBody[i1:i2]
      #title=unquote(title)
      title=title.encode('utf-8')
      title=title.replace("&#33;", "!").replace("&#39;", "'").replace("&quot;", "\"")

      i = trBody.index(msgIdenTag)
      i1 = trBody.index(msgStartTag, i) + len(msgStartTag)
      i2 = trBody.index(msgCloseTag, i1)
      message=trBody[i1:i2]
      #message=unquote(message)
      message=message.encode('utf-8')
      message=message.replace("&#33;", "!").replace("&#39;", "'").replace("&quot;", "\"")
      
      it['nt']=title
      it['m']=message

  j_s=json.dumps(j)

  open('recent.json', 'w').write(j_s)
except Exception as e:
  open('recent.json', 'w').write(json.dumps({'error': str(e)}))

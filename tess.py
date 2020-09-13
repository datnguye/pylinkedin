from pylinkedin import profile

pid = 'tuiladat'
li_at = 'AQEDASP2AiAFk-ukAAABcs-U45EAAAF0qRGMmVYAw8VLz6nXhumoBSvbtNF3vE5XhTsz4Vc_JLL8cFoMkAIxAlKfZI5hJgUehhyumTpfUhtOoNh6fRUb7woNvMqN0rjR9eQqwUzGHYz7vDdz_I7hS_H4'
data = profile.crawl(profile_id=pid, li_at_cookie=li_at, debug=True, headless=False)

print(data)
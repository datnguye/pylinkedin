from pylinkedin import profile

pid = ''
data = profile.crawl(profile_id=pid)

print(data)
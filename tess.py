from pylinkedin import profile

pid = 'tuiladat'
li_at = 'AQEDASP2AiAAlo5oAAABcez8ApMAAAF04iydb1YAhzwZs678XaraVTntGvzj8U3i8Wb4BOhJrDmiJr3PH_dBm0WeqatNdyDnahaIO3bFtcXx-tQS7kFWon2iMZyC3WLlGxK3UrBl0fzHrhU0XfhgkIhl'
data = profile.crawl(profile_id=pid, li_at_cookie=li_at, debug=True, headless=False)

print(data)
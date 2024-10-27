from requests_html import HTMLSession

session = HTMLSession()
response = session.get('https://www.ea.com/ea-sports-fc/ultimate-team/web-app/')
response.html.render()  # This executes JavaScript

cookies = session.cookies.get_dict()

print(cookies)

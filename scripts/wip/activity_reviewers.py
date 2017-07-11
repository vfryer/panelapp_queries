'''
This program will retrieve all of the activity from PanelApp and store it in a database so that i can be queried at any time.
'''

import requests, bs4

activity_log_page = "https://panelapp.extge.co.uk/crowdsourcing/PanelApp/Activity"
headers = {'Content-Type':'txt/html'}

activity_page_html = requests.get(activity_log_page, headers = headers)
html_data = activity_page_html.text
soup = bs4(html_data)
print(soup)

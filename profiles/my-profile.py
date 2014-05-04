#!python
# implement a new api record_social, for any user who use this api, the visit will be recorded to shared file, so the profile will show the social graph of the latest visits happened in zoobar

global api

social_graph = api.call('record_social')

social_graph = social_graph[:3]

print 'Last 3 social visit:\n', '<ul>'

for username in social_graph:
  print '<li>', username, '</li>'

print '</ul>'

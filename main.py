import csv

import pprint

article_data = {}

with open('data/articles.csv', 'r') as f:
	csv_reader = csv.reader(f, delimiter=',')
	line_count = 0
	for row in csv_reader:
		if line_count <= 4:
			print(row)
		else:
			break
		line_count = line_count + 1

users = {}

with open('data/article_user.csv', 'r') as f:
	csv_reader = csv.reader(f, delimiter=',')
	line_count = 0
	for row in csv_reader:
		user_id = row[0]
		if line_count == 0:
			line_count += 1
			continue
		if user_id not in users:
			users[user_id] = [row[1]]
		else:
			users[user_id].append(row[1])
		if line_count >= 30:
			break
		line_count = line_count + 1

pprint.pprint(users)

print(line_count)


# Potential approaches:
# 	Generate a relatedness-score, semi-arbitrary algorithm, ie:
#		score = havent_read * user_relevance * article_relevance * popularity * recentness
# doing research on generating user_relevance and article_relevance, will write more Soon(TM)
#
#
#
# 
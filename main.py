import csv


import time
import math

from flask import request, jsonify
import flask
from flask_restful import Resource, Api
import flask_restful

import datetime


import tensorflow as tf

import tensorflow_hub as hub

import numpy as np


app = flask.Flask(__name__)
app.config["DEBUG"] = True

module_url = "https://tfhub.dev/google/universal-sentence-encoder/4"
model = hub.load(module_url)
print ("module %s loaded" % module_url)
def embed(input):
  return model(input)



class Recommender(Resource):
    def __init__(self):
        self.users = {}
        self.users_without_timestamp = {}
        self.article_data = {}
        self.readership = {}
        self.titles = []
        self.ids = []
        
        with open('data/articles.csv', 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                    continue
                # article_id = (headline, url, published_date)
                timestamp = datetime.datetime.timestamp(datetime.datetime.fromisoformat(row[3][:-2]))
                self.article_data[row[0]] = (row[1], row[2], timestamp)
                self.titles.append(row[1])
                self.ids.append(row[0])
                
        self.embeddings = embed(self.titles)
		
        with open('data/article_user.csv', 'r') as f:
            csv_reader = csv.reader(f, delimiter=',')
            line_count = 0
            for row in csv_reader:
                # user: [articles]
                user_id = row[0]
                article_id = row[1]
                timestamp = row[2]
                if line_count == 0:
                    line_count += 1
                    continue
                if user_id not in self.users:
                    self.users[user_id] = [(article_id, timestamp)]
                    self.users_without_timestamp[user_id] = [article_id]
                    
                else:
                    self.users[user_id].append((article_id, timestamp))
                    self.users_without_timestamp[user_id].append(article_id)
                    
                if article_id not in self.readership:
                    self.readership[article_id] = []
                self.readership[article_id].append(user_id)
        
        self.article_ids = self.article_data.keys()
        
        self.headline_scores = {article_id: {} for article_id in self.article_ids}
        
        for article_1 in self.article_ids:
            for article_2 in self.article_ids:
                if article_2 in self.headline_scores[article_1] and article_1 in self.headline_scores[article_2]:
                    continue
                score = (self.generate_relative_headline_scores(article_1, article_2) + 1) / 2
                self.headline_scores[article_1][article_2] = score
                self.headline_scores[article_2][article_1] = score
                
        
                
        		
    
    
    
    
    def generate_relative_headline_scores(self, article_1, article_2):
        
        index1 = self.ids.index(article_1)
        index2 = self.ids.index(article_2)
        
        score = np.inner(self.embeddings[index1], self.embeddings[index2])
        ### Will produce some number between 0 and 1 defining how related the headlines are
        ### For now produces 1 for all.
        
        return score
    
    def get_recentness_score(self, article_id):
        t = time.time()
        pub_date = self.article_data[article_id][2]
        tdelta = t - pub_date
        normalized_recency = (1 / math.log(tdelta))
        return normalized_recency
    
    def calculate_popularity_score(self, article_id):
        reader_count = len(self.readership[article_id])
        eased_popularity = 1 - (1/(2 + reader_count))
        return eased_popularity
    
    def calculate_score(self, user_id, article_id):
        if user_id in self.readership[article_id]:
            read_already = .5
        else:
            read_already = 1
        article_relevances = [self.generate_relative_headline_scores(article_id, read_article) for read_article in self.users_without_timestamp[user_id]]
        article_relevance = sum(article_relevances)/len(article_relevances)
        popularity = self.calculate_popularity_score(article_id)
        recentness = self.get_recentness_score(article_id)
        score = read_already * article_relevance * popularity * recentness
        return score

    # 	Generate a relatedness-score, semi-arbitrary algorithm, ie:
    #		score = havent_read * user_relevance * article_relevance * popularity * recentness

recommender = Recommender()


    
@app.route('/recommendations', methods=['GET'])
def get(recommender):
    try:
        user_id = request.args.get('user_id')
    except:
        user_id = '2bc424123e0a12d29c488bb6e565fe98d0a49b46'
    
    
    score_pairs = []
    
    for article in recommender.article_ids:
        score_pairs.append((recommender.calculate_score(user_id, article), article))
        
    score_pairs.sort()
    
    score_pairs.reverse()
    
    best_pairs = [(j, i) for i, j in score_pairs[:5]]

    return jsonify(best_pairs)
    

if __name__ == '__main__':
    app.run()
    
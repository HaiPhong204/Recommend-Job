from flask import Flask, request, jsonify
from flask_restful import Resource, Api, reqparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from pre_process_data import stopWords_Teencode
import string
import pandas as pd
import json

app = Flask(__name__)
api = Api(app)

# Đọc dữ liệu từ
jobs = pd.read_excel('job_data.xlsx')

# Tiền xử lý dữ liệu và tính cosine similarity
def remove_punctuation(text):
    punctuationfree="".join([i for i in text if i not in string.punctuation])
    return punctuationfree

jobs["description"] = jobs["description"].apply(stopWords_Teencode)
jobs["requirement"] = jobs["requirement"].apply(stopWords_Teencode)
jobs["description"] = jobs["description"].str.replace('\n', ' ')
jobs["requirement"] = jobs["requirement"].str.replace('\n', ' ')
jobs["description"] = jobs["description"].apply(lambda x:remove_punctuation(x))
jobs["requirement"] = jobs["requirement"].apply(lambda x:remove_punctuation(x))
jobs["user"] = jobs["user"].apply(lambda x: x.replace("'", '"'))
jobs["user"] = jobs["user"].apply(lambda x: json.loads(x))
jobs["packages"] = jobs["packages"].apply(lambda x: x.replace("'", '"'))
jobs["packages"] = jobs["packages"].apply(lambda x: json.loads(x))
tfidf_vectorizer = TfidfVectorizer()


def recommend_jobs(skill, exp):
    user_input = skill + " " + exp
    user_input_vector = tfidf_vectorizer.fit_transform([user_input])
    tfidf_matrix_descriptions = tfidf_vectorizer.transform(jobs["description"] + jobs["requirement"])
    cosine_sim_scores_new_user = cosine_similarity(user_input_vector, tfidf_matrix_descriptions)
    job_ranking_new_user = pd.Series(cosine_sim_scores_new_user[0], name="cosine_sim_score").sort_values(ascending=False).index
    recommended_jobs_new_user = jobs.iloc[job_ranking_new_user]
    recommended_jobs_new_user['createdAt'] = recommended_jobs_new_user['createdAt'].astype(str)
    recommended_jobs_new_user['updatedAt'] = recommended_jobs_new_user['updatedAt'].astype(str)
    return recommended_jobs_new_user.head(20)

def recommend_all_jobs(skill, exp):
    user_input = skill + " " + exp
    user_input_vector = tfidf_vectorizer.fit_transform([user_input])
    tfidf_matrix_descriptions = tfidf_vectorizer.transform(jobs["description"] + jobs["requirement"])
    cosine_sim_scores_new_user = cosine_similarity(user_input_vector, tfidf_matrix_descriptions)
    job_ranking_new_user = pd.Series(cosine_sim_scores_new_user[0], name="cosine_sim_score").sort_values(ascending=False).index
    recommended_jobs_new_user = jobs.iloc[job_ranking_new_user]
    recommended_jobs_new_user['createdAt'] = recommended_jobs_new_user['createdAt'].astype(str)
    recommended_jobs_new_user['updatedAt'] = recommended_jobs_new_user['updatedAt'].astype(str)
    return recommended_jobs_new_user.head(100)

class RecommendJobs(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('Skill', type=str, required=True, help='Skill cannot be blank')
            parser.add_argument('Experiences', type=str, required=True, help='Experiences cannot be blank')
            args = parser.parse_args()

            skill = args['Skill']
            exp = args['Experiences']

            stopWords_Teencode(skill)
            stopWords_Teencode(exp)
            skill = skill.replace('\n', ' ')
            exp = exp.replace('\n', ' ')
            remove_punctuation(skill)
            remove_punctuation(exp)
            recommended_jobs = recommend_jobs(skill, exp)

            return recommended_jobs.to_dict(orient='records')
        except Exception as e:
            return {'error': str(e)}, 500
    
class RecommendAllJobs(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('Skill', type=str, required=True, help='Skill cannot be blank')
            parser.add_argument('Experiences', type=str, required=True, help='Experiences cannot be blank')
            args = parser.parse_args()

            skill = args['Skill']
            exp = args['Experiences']

            stopWords_Teencode(skill)
            stopWords_Teencode(exp)
            skill = skill.replace('\n', ' ')
            exp = exp.replace('\n', ' ')
            remove_punctuation(skill)
            remove_punctuation(exp)
            recommended_jobs = recommend_all_jobs(skill, exp)

            return recommended_jobs.to_dict(orient='records')
        except Exception as e:
            return {'error': str(e)}, 500

class JobResource(Resource):
    def post(self):
        try:
            post = request.get_json()
            jobs = pd.read_excel('job_data.xlsx')
            data = pd.DataFrame(post, index=[0])
            existing_job = jobs[jobs['id'] == post['id']]
            if not existing_job.empty:
                jobs.loc[jobs['id'] == post['id']] = data
                message = 'Post updated successfully'
            else:
                jobs = jobs._append(data, ignore_index=True)
                message = 'Job added successfully'

            jobs.to_excel('job_data.xlsx', index=False)

            return {'message': message}, 201
        except Exception as e:
            return {'error': str(e)}, 500

# Thêm resource vào API
api.add_resource(JobResource, '/jobs') 
api.add_resource(RecommendJobs, '/recommend')
api.add_resource(RecommendAllJobs, '/recommend-all')

if __name__ == '__main__':
    app.run(debug=True)

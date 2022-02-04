from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.okxdx.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/movie', methods=["POST"])
def movie_POST():
    url_receive = request.form['url_give']
    star_receive = request.form['star_give']
    comment_receive = request.form['comment_give']

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    url = url_receive
    data = requests.get(url, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')

    title = soup.select_one("meta[property='og:title']")['content']
    image = soup.select_one("meta[property='og:image']")['content']
    description = soup.select_one("meta[property='og:description']")['content']
    doc = {
        'url':url_receive,
        'star': star_receive,
        'comment': comment_receive,
        'title': title,
        'image': image,
        'description': description
    }
    db.movie_posting.insert_one(doc)
    # print(url, star_receive, comment_receive + '||' + title, image, description)
    return jsonify({'msg':'영화가 등록 완료되었습니다.'})

@app.route('/movie', methods=["GET"])
def movie_GET():
    movie_list=list(db.movie_posting.find({},{'_id': False}))
    return jsonify({'movies':movie_list})


if __name__=='__main__':
    app.run('0.0.0.0', port=5000, debug=True)

#image,title,description,star, comment


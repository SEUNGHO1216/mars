from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.okxdx.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/book', methods=["POST"])
def post_POST():
    writer_receive = request.form['writer']
    message_receive = request.form['message']
    doc = {
        'writer':writer_receive,
        'message':message_receive
    }
    db.books.insert_one(doc)
    return jsonify({'msg':'방명록 등록완료!'})

@app.route('/book', methods=["GET"])
def post_GET():
    book_list=list(db.books.find({},{'_id': False}))
    return jsonify({'books':book_list})

if __name__=='__main__':
    app.run('0.0.0.0', port=5000, debug=True)
from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@cluster0.okxdx.mongodb.net/Cluster0?retryWrites=true&w=majority')
db = client.dbBucket

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']
    print(bucket_receive)
    bucketList=list(db.bucekts.find({},{'_id':False}))
    listCnt=len(bucketList)+1
    doc={
        'num':listCnt,
        'context':bucket_receive,
        'done':0
    }
    db.bucekts.insert_one(doc)
    return jsonify({'msg': '버킷리스트 작성 완료'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    print(num_receive)
    db.bucekts.update_one({'num':int(num_receive)},{'$set':{'done':1}})
    return jsonify({'msg': '축하합니다! 버킷리스트를 달성 완료했습니다!'})

@app.route("/bucket/cancel", methods=["POST"])
def bucket_cancel():
    num_receive = request.form['num_give']
    print(num_receive)
    db.bucekts.update_one({'num':int(num_receive)},{'$set':{'done':0}})
    return jsonify({'msg': '버킷리스트 달성을 취소합니다.'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucketList=list(db.bucekts.find({},{'_id':False}))
    return jsonify({'msg': bucketList})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
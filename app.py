from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

from pymongo import MongoClient
client = MongoClient('mongodb+srv://test:sparta@sparta.xob7d.mongodb.net/?retryWrites=true&w=majority')
db = client.dbsparta

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form['bucket_give']

    bucket_list = list(db.bucket.find({}, {'_id': False}))
    count = len(bucket_list) + 1 #num값을 리스트 개수+1로 만들어주기위한 변수
    print(count)
    doc = {
        'num':count,
        'bucket':bucket_receive,
        'done':0
    }
    db.bucket.insert_one(doc)

    return jsonify({'msg': '등록 완료!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form['num_give']
    #클라이언트에서 db로 받아오면 숫자형도 다 문자로 받아옴 그래서 숫자로 바꿔줘야함 int()
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 1}})
    # print(num_receive)
    return jsonify({'msg': '버킷 완료!'})

@app.route("/bucket/reset", methods=["POST"])
def bucket_reset():
    num_receive = request.form['num_give']
    #클라이언트에서 db로 받아오면 숫자형도 다 문자로 받아옴 그래서 숫자로 바꿔줘야함 int()
    db.bucket.update_one({'num': int(num_receive)}, {'$set': {'done': 0}})
    # print(num_receive)
    # return jsonify()
    return "reset"

@app.route("/bucket", methods=["GET"])
def bucket_get():
    bucket_list = list(db.bucket.find({},{'_id':False}))
    return jsonify({'buckets' :bucket_list})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)
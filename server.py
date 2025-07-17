from flask import Flask#flask server 구동코드
from flask import render_template #html 문서를 load 단 templates 폴더에 있는 html만
from flask import request ,redirect, make_response
from aws import detect_labels_local_file as label
from aws import compare_faces as cp
from werkzeug.utils import secure_filename
app = Flask(__name__)

#서버 주소/
# return html 문서
@app.route("/")
def index():
    return render_template("home.html")


@app.route("/compare", methods=["POST"])
def compare():
    try:
        if request.method=="POST":
            f1= request.files["file1"]
            f2= request.files["file2"]
            filename1 = secure_filename(f1.filename)
            filename2 = secure_filename(f2.filename)
            f1.save("static/"+filename1)
            f2.save("static/"+filename2)
            r= cp("static/"+filename1,"static/"+filename2)
            return r
    except:
        return "비교실패"

@app.route("/detect", methods=["POST"])
def detect():
    try:
        if request.method =="POST":
            f = request.files["file"]
            filename = secure_filename(f.filename)
            # 외부에서 온 이미지 파일등을 마음대로 저장할수 없음
            f.save("static/" + filename)
            r = label("static/" + filename)
            # 서버에  클라이언트가 보낸이미지 저장
            return r
    except:
        return "감지실패"



@app.route("/mbti", methods=["POST"])
def mbti():
    try:
        if request.method =="POST":
            mbti = request.form["mbti"]
            return f"당신의 MBTI는 {mbti}입니다"
    except:
        return "데이터 수신 실패"




@app.route("/login", methods=["GET"])
def login():
    try:
        if request.method == "GET":
            #login_id,login_pw
            login_id = request.args["login_id"]
            login_pw = request.args["login_pw"]

            if (login_id == "junhee") and (login_pw=="1234"):
                # 로그인 성공->로그인 성공 페이지로 이동
                # junhee님 환영합니다
                # response = make_response ("로그인 성공")
                response =make_response(redirect("/login/success"))
                response.set_cookie("user",login_id)
                
                return response
            else:
                return redirect("/")
                # 로그인 실패-> / 경로로 다시이동

            # return f"{login_id}님 환영합니다"
    except:
        return "로그인 실패"


@app.route("/login/success")
def login_success():
    id = request.cookies.get("user")
    return f"{id}님 로그인 성공입니다."
if __name__ == "__main__":
    #1. host
    #2. port
    app.run(host="0.0.0.0")
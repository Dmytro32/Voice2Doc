from flask import Flask,render_template,request
import model
import os
app = Flask(__name__)


@app.route('/')
def home():
    text=""
    return render_template('index.html',text=text)
@app.route('/process',methods=["POST"])
def audio():
    if request.method=="POST":
        if "audio_data" in request.files:
            data=request.files["audio_data"]
            set=model.get_set()
            print(f"{set=}")
            input_path=os.path.join(set["audio"]["WAVE_OUTPUT_FOLDER"], set["audio"]["WAVE_OUTPUT_FILENAME"] + ".webm")

            data.save(input_path)
            
            model.toWav()
            nl='\n'
            res=f"{nl} {model.openWhisper()}"
            print(f"{res=}")
            return  res
    
@app.route('/savepage')
def savepage():
    return render_template('document.html')
if __name__ == '__main__':

    app.run(host='0.0.0.0', port=5000, debug=True,ssl_context=('cert.pem', 'key.pem'))

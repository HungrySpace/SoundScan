from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///history.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#  заливка данных в базу
class OldRec(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # nullable=False - нельзя создавать пустое значение
    result = db.Column(db.String(300))
    comment = db.Column(db.String(300))
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<OldRec %r>' % self.id


#  парсинг аудио файла
def get_result(spectrogram):
    for s1 in spectrogram:
        for i in range(len(s1)):
            s1[i] = np.arctan((s1[i]**0.4)/10)

    # 2d -> 1d
    i1size = spectrogram.shape[0]
    i2size = spectrogram.shape[1]
    # print(i1size)
    # print(i2size)
    spectrogram2 = np.zeros((i1size))
    i1 = 0
    while i1 < i1size:
        i2 = 0
        # print('-------------------')
        while i2 < i2size:
            spectrogram2[i1] = spectrogram2[i1] + spectrogram[i1, i2]
            print(spectrogram[i1, i2],)
            i2 = i2 + 1
        i1 = i1 + 1
    b = [spectrogram2[i] for i in range(len(spectrogram2))]
    freq_step = 22100/2048
    return str(freq_step * b.index(max(b[0:200]))) + 'Hz, ' + str(freq_step * b.index(max(b[300:500]))) + 'Hz, ' + str(freq_step * b.index(max(b[600:800]))) + 'Hz, ' + str(freq_step * b.index(max(b[1200:1500]))) + 'Hz, ' + str(freq_step * b.index(max(b[1600:1900]))) + 'Hz'


# заись звука
def audiofile():
    # fs = 44100 4096
    fs = 4096
    second = 3
    myrecording = sd.rec(int(second * fs), samplerate=fs, channels=1)
    sd.wait()
    write('output.wav', fs, myrecording)
    return myrecording


#  главная страница
@app.route('/', methods=['POST', 'GET'])
def index():
    #  сли нажали на кнопку на главной страницы
    if request.method == "POST":
        myrecording = audiofile()
        comment = request.form['comment']
        result = get_result(myrecording)
        # записываем в бд значения
        article = OldRec(comment=comment, result=result)

        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/')
        except:
            return "Fail"
    else:
        return render_template("index.html")


@app.route('/project')
def project():
    return render_template("project.html")


@app.route('/history')
def history():
    rec = OldRec.query.order_by(OldRec.date.desc()).all()
    return render_template("history.html", rec=rec)


if __name__ == "__main__":
    app.run(debug=True)

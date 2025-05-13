from flask import Flask, render_template

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/analytic')
def analytic():
    return render_template('analytic.html')

@app.route("/ml")
def mobile_legends():
    return render_template("ml.html")

@app.route("/pubg")
def pubg():
    return render_template("pubg.html")

@app.route("/re")
def resident_evil():
    return render_template("re.html")


# Jalankan server
if __name__ == '__main__':
    app.run(debug=True)

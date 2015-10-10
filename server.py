from flask import Flask, request, render_template, url_for 
import playlistr

app = Flask(__name__)

@app.route('/')
def form():
	css = url_for('static',filename='css/bootstrap.min.css')
	return render_template('form.html',s=css) 

@app.route('/', methods=['POST'])
def form_post():
	return playlistr.make_playlist(request.form.get['text'])

if __name__ == "__main__":
	app.run()

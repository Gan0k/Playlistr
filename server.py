from flask import Flask, request, render_template 
import playlistr

app = Flask(__name__)

@app.route('/')
def form():
	return render_template('form.html') 

@app.route('/', methods=['POST'])
def form_post():
	return playlistr.make_playlist(request.form['text'])  

if __name__ == "__main__":
	app.run()

from flask import Flask, request, render_template, url_for, redirect
import playlistr_main as playlistr

app = Flask(__name__)
notfound = 'No videos found'

@app.route('/')
def form():
	css = url_for('static',filename='css/bootstrap.min.css')
	return render_template('form.html',s=css)

@app.route('/', methods=['POST'])
def form_post():
	pl = playlistr.make_playlist(request.form.get('text'))
	if pl == notfound: return notfound
	else: return redirect(pl, code=302)

if __name__ == "__main__":
	app.run(debug=True)

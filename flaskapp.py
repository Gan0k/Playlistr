from flask import Flask, request, render_template, url_for, redirect
import playlistr

app = Flask(__name__)
app.config.from_pyfile('flaskapp.cfg')

NOT_FOUND_MSG = 'No videos were found :('

@app.route('/')
def form():
	css = url_for('static',filename='css/bootstrap.min.css')
	return render_template('form.html',s=css)

@app.route('/', methods=['POST'])
def form_post():
	pl = playlistr.make_playlist(request.form.get('text'))
	if pl is None: return NOT_FOUND_MSG
	else: return redirect(pl, code=302)

if __name__ == "__main__":
	app.run()

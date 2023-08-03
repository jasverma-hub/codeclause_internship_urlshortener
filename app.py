from flask import Flask, render_template, request, redirect
import string
import random

app = Flask(__name__)
app.config['BASE_URL'] = "http://localhost:5000/"  # Change this to your production domain

# In a real project, you would use a database to store the shortened URLs.
url_mapping = {}


def generate_short_code():
    # Generate a random 6-character string for the short URL
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(6))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['url']
        short_code = generate_short_code()
        short_url = app.config['BASE_URL'] + short_code
        url_mapping[short_code] = original_url
        return render_template('index.html', short_url=short_url)

    return render_template('index.html')


@app.route('/<short_code>')
def redirect_to_original_url(short_code):
    original_url = url_mapping.get(short_code)
    if original_url:
        return redirect(original_url)
    else:
        return "Short URL not found!"


if __name__ == '__main__':
    app.run(debug=True)

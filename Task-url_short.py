from flask import Flask, request, redirect, render_template_string, abort
import random
import string

app = Flask(__name__)

# In-memory storage
url_mapping = {}

# Generate a short code
def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

# HTML template
HTML_TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <title>URL Shortener</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
      body {
        background-image: url('https://images.unsplash.com/photo-1517336714731-489689fd1ca8');
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
        padding-top: 80px;
        color: #fff;
      }

      .container {
        max-width: 600px;
        background-color: rgba(0, 0, 0, 0.6);  /* semi-transparent background */
        padding: 30px;
        border-radius: 10px;
        box-shadow: 0 0 15px rgba(0, 0, 0, 0.5);
      }

      input, button {
        border-radius: 5px !important;
      }

      a {
        color: #00d1ff;
      }
    </style>
  </head>
  <body>
    <div class="container text-center">
      <h1 class="mb-4">🔗 URL Shortener</h1>
      <form method="post">
        <div class="input-group mb-3">
          <input type="text" class="form-control" name="long_url" placeholder="Enter a long URL (e.g., https://example.com)" required>
          <button class="btn btn-primary" type="submit">Shorten</button>
        </div>
      </form>

      {% if short_url %}
        <div class="alert alert-success mt-4">
          Short URL: <a href="{{ short_url }}" target="_blank">{{ short_url }}</a>
        </div>
      {% endif %}
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"></script>
  </body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def home():
    short_url = None
    if request.method == 'POST':
        long_url = request.form['long_url']
        # Basic validation
        if not (long_url.startswith('http://') or long_url.startswith('https://')):
            long_url = 'http://' + long_url

        short_code = generate_short_code()
        while short_code in url_mapping:
            short_code = generate_short_code()
        url_mapping[short_code] = long_url
        short_url = request.host_url + short_code
    return render_template_string(HTML_TEMPLATE, short_url=short_url)

@app.route('/<short_code>')
def redirect_to_long_url(short_code):
    long_url = url_mapping.get(short_code)
    if long_url:
        return redirect(long_url)
    else:
        abort(404, description="Short URL not found.")

if __name__ == '__main__':
    app.run(debug=True, port=5000)

from flask import Flask, request, render_template, redirect, url_for, session
from libs.Youtube_functions import youtube_search, get_video_details, get_captions

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a random, secure value

api_key = 'AIzaSyA_GneRzf-BNyXTf-rogarI-fuVJsvG-YE'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form.get('value1')
        if query:
            search_results = youtube_search(api_key, query)
            session['search_results'] = search_results  # Store search results in session
        return render_template('index.html', results=search_results)

    search_results = session.get('search_results', None)  # Retrieve search results from session
    return render_template('index.html', results=search_results)

@app.route('/result', methods=['GET'])
def result():
    selected_index = request.args.get('select')
    video_details = None
    captions = None

    search_results = session.get('search_results', [])  # Retrieve search results from session

    if selected_index is not None:
        selected_index = int(selected_index)  # Convert to integer
        if 0 <= selected_index < len(search_results):
            selected_video_id = search_results[selected_index][0]
            video_details = get_video_details(selected_video_id, api_key)
            captions = get_captions(selected_video_id)

    return render_template('result.html', video_details=video_details, captions=captions)

if __name__ == '__main__':
    app.run(debug=True)

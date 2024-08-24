from flask import Flask, request, render_template, redirect, url_for
from libs.Youtube_functions import *  # Adjust import based on your file structure
#example of uploading and fetching the code
app = Flask(__name__)

api_key = 'AIzaSyA_GneRzf-BNyXTf-rogarI-fuVJsvG-YE'

@app.route('/', methods=['GET', 'POST'])
def index():
    search_results = None

    if request.method == 'POST':
        query = request.form.get('value1')
        if query:
            search_results = youtube_search(api_key, query)
        return render_template('index.html', results=search_results)

    return render_template('index.html', results=search_results)

@app.route('/result', methods=['GET'])
def result():
    selected_index = request.args.get('select')
    video_details = None
    captions = None

    if selected_index is not None:
        search_results = request.args.getlist('results')  # Get the search results passed as a list
        selected_video_id = search_results[int(selected_index)][0]
        video_details = get_video_details(selected_video_id, api_key)
        captions = get_captions(selected_video_id)

    return render_template('result.html', video_details=video_details, captions=captions)

if __name__ == '__main__':
    app.run(debug=True)

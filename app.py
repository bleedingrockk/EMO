from flask import Flask, request, render_template, redirect, url_for, session
from libs.Youtube_functions import *
from libs.classifier_model import *
from libs.n_gram import *

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
    comments_data = None
    author_list = []
    text_list = []
    top_commenters = []
    top_10_emojis = []
    cleaned_list = []
    categorised_dict = {}
    top_10_bigrams = ()
    top_5_trigrams = ()

    search_results = session.get('search_results', [])  # Retrieve search results from session

    if selected_index is not None:
        try:
            selected_index = int(selected_index)  # Convert to integer
            if 0 <= selected_index < len(search_results):
                selected_video_id = search_results[selected_index][0]
                video_details = get_video_details(selected_video_id, api_key)
                captions = get_captions(selected_video_id)
                comments_data = get_comments_with_replies(selected_video_id, api_key)  # Get comments with replies

                # Convert comments to lists
                author_list, text_list = save_comments_as_list(comments_data)
                
                # Get top commenters
                top_commenters = get_top_commenters(author_list)
                
                # Get the top 10 most common emojis
                top_10_emojis = extract_and_rank_top_emojis(text_list)


                #cleaned text
                cleaned_list = cleaned_strings_list(text_list)

                #Classified comments
                categorised_dict = classify_text(text_list)

                # Get the top 10 bigrams and top 5 trigrams
                top_10_bigrams = get_top_ngrams(text_list, 2, 10)
                top_5_trigrams = get_top_ngrams(text_list, 3, 5)

        except ValueError:
            pass  # Handle invalid index here if necessary

    return render_template('result.html',
                            video_details=video_details,
                            captions=captions,
                            authors=author_list,
                            text_list=text_list,
                            top_commenters=top_commenters, 
                            top_10_emojis=top_10_emojis, 
                            cleaned_list=cleaned_list, 
                            categorised_dict = categorised_dict,
                            top_10_bigrams = top_10_bigrams,
                            top_5_trigrams = top_5_trigrams)

if __name__ == '__main__':
    app.run(debug=True)
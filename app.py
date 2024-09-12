from flask import Flask, request, render_template, redirect, url_for, session
from libs.Youtube_functions import *
from libs.classifier_model import *
from libs.n_gram import *
from libs.visuals import * 

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
    video_id = request.args.get('video_id')  # New: Get video_id directly from query parameter
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
    plot_data = None
    pie_chart_base64 = None
    chart_data = None

    search_results = session.get('search_results', [])  # Retrieve search results from session

    # Case 1: When video_id is provided directly
    if video_id:
        selected_video_id = video_id

    # Case 2: When selected_index is provided and valid
    elif selected_index is not None:
        try:
            selected_index = int(selected_index)  # Convert to integer
            if 0 <= selected_index < len(search_results):
                selected_video_id = search_results[selected_index][0]
            else:
                selected_video_id = None
        except ValueError:
            selected_video_id = None

    # Proceed only if a valid video ID is available
    if selected_video_id:
        video_details = get_video_details(selected_video_id, api_key)
        thumbnail_url = get_thumbnail_url(selected_video_id, api_key)
        captions = get_captions(selected_video_id)
        comments_data = get_comments_with_replies(selected_video_id, api_key)  # Get comments with replies

        # Convert comments to lists
        author_list, text_list = save_comments_as_list(comments_data)
        
        # Get top commenters
        top_commenters = get_top_commenters(author_list)
        
        # Get the top 10 most common emojis
        top_10_emojis = extract_and_rank_top_emojis(text_list)
        
        # Plotting the Chart
        # Generate Base64-encoded image data
        chart_data = plot_top_10_emojis(top_10_emojis)

        # Cleaned text
        cleaned_list = cleaned_strings_list(text_list)

        # Classified comments
        categorised_dict = classify_text(text_list)

        # Get the top 10 bigrams and top 5 trigrams
        top_10_bigrams = get_top_ngrams(text_list, 2, 10)
        top_5_trigrams = get_top_ngrams(text_list, 3, 5)

        # Generate word cloud
        plot_data = generate_wordcloud_from_cleaned_text(cleaned_list)

        # Pie Chart   
        # Generate the pie chart as a base64 string
        pie_chart_base64 = create_pie_chart_base64(categorised_dict)

    return render_template('result.html',
                            video_details=video_details,
                            thumbnail_url=thumbnail_url,
                            captions=captions,
                            authors=author_list,
                            text_list=text_list,
                            top_commenters=top_commenters, 
                            top_10_emojis=top_10_emojis, 
                            cleaned_list=cleaned_list, 
                            categorised_dict=categorised_dict,
                            top_10_bigrams=top_10_bigrams,
                            top_5_trigrams=top_5_trigrams,
                            plot_data=plot_data,
                            pie_chart_base64=pie_chart_base64,
                            chart_data=chart_data)

if __name__ == '__main__':
    app.run(debug=True)
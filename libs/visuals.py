from wordcloud import WordCloud
import numpy as np
from PIL import Image
import io
import base64
import matplotlib.pyplot as plt


def generate_wordcloud_from_cleaned_text(cleaned_text_list):
    """
    Generates a word cloud image from a list of cleaned strings, applies a custom shape,
    and returns it as a base64-encoded string.
    
    Parameters:
        cleaned_text_list (list): A list of cleaned strings.
        
    Returns:
        str: The base64-encoded string of the word cloud image.
    """


    # Combine the list of cleaned strings into a single string
    text = " ".join(cleaned_text_list)
    
    # Create a WordCloud object with custom settings
    wordcloud = WordCloud(width=1200,
                        height=400,
                        background_color='black',
                        colormap='plasma',  # Color map
                        contour_color='white',  # Outline color
                        contour_width=1,  # Outline width
                        mode='RGB').generate(text)
    
    # Save the word cloud to a BytesIO object
    buf = io.BytesIO()
    wordcloud.to_image().save(buf, format='PNG')
    buf.seek(0)
    
    # Encode image to base64 for HTML embedding
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return plot_data



import matplotlib.pyplot as plt
import numpy as np
import io
import base64

def create_pie_chart_base64(my_dict):
    """
    Creates a pie chart from the count dictionary and returns it as a base64-encoded string.
    
    Parameters:
        my_dict (dict): A dictionary where keys are categories and values are lists of items.
        
    Returns:
        str: The base64-encoded string of the pie chart image.
    """
    # Count the number of values for each key
    count_dict = {key: len(values) for key, values in my_dict.items()}

    total_count = sum(count_dict.values())
    threshold = 0.05 * total_count  # 5% of the total count
    
    # Filter the dictionary to include only categories greater than the threshold
    filtered_count_dict = {key: count for key, count in count_dict.items() if count > threshold}
    
    if not filtered_count_dict:
        # If no categories meet the criteria, return an empty chart or a message
        return None
    
    labels = list(filtered_count_dict.keys())
    sizes = list(filtered_count_dict.values())
    
    # Define colors and shadow
    colors = plt.cm.Paired(np.linspace(0, 1, len(labels)))
    shadow = True
    
    # Determine which slices to explode
    explode = [0.2] * len(labels)  # Explode all slices for better visibility
    
    # Create a pie chart with a black background
    plt.figure(figsize=(12, 8), facecolor='black')  # Set figure background color
    plt.gca().set_facecolor('black')  # Set plot area background color
    
    wedges, texts, autotexts = plt.pie(sizes,
                                       labels=labels,
                                       autopct='%1.1f%%',
                                       startangle=140,
                                       colors=colors,
                                       shadow=shadow,
                                       explode=explode)  # Apply explosion to all slices

    # Improve readability of the labels and percentages with white color
    for text in texts:
        text.set_fontsize(14)
        text.set_color('white')  # Set text color to white for contrast
        text.set_fontweight('bold')
        
    for autotext in autotexts:
        autotext.set_fontsize(14)
        autotext.set_color('white')  # Set percentage text color to white for contrast
        autotext.set_fontweight('bold')
    
    plt.title('Enhanced Pie Chart of Category Counts', fontsize=18, fontweight='bold', color='white')  # Set title color to white
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the pie chart to a BytesIO object
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=1)
    buf.seek(0)
    
    # Encode image to base64 for HTML embedding
    pie_chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return pie_chart_base64

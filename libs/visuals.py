from wordcloud import WordCloud
import numpy as np
from PIL import Image
import io
import base64
import matplotlib.pyplot as plt


def generate_wordcloud_from_cleaned_text(cleaned_text_list):
    """
    Generates a word cloud image from a list of cleaned strings, applies a custom shape,
    and returns it as a base64-encoded string with a transparent background.
    
    Parameters:
        cleaned_text_list (list): A list of cleaned strings.
        
    Returns:
        str: The base64-encoded string of the word cloud image with a transparent background.
    """

    # Combine the list of cleaned strings into a single string
    text = " ".join(cleaned_text_list)
    
    # Create a WordCloud object with custom settings
    wordcloud = WordCloud(width=1200,
                            height=600,
                            background_color='blqck',  # Temporary white background
                            colormap='plasma',  # Color map
                            contour_color='black',  # Outline color
                            contour_width=1,  # Outline width
                            mode='RGBA'  # Mode that supports transparency (RGBA)
                            ).generate(text)
    
    # Convert WordCloud to an image
    wordcloud_image = wordcloud.to_image()
    
    # Convert the white background to transparency
    wordcloud_image = wordcloud_image.convert("RGBA")
    datas = wordcloud_image.getdata()

    new_data = []
    for item in datas:
        # Change white (or near white) to transparent
        if item[:3] == (255, 255, 255):  # Detect white pixels
            new_data.append((255, 255, 255, 0))  # Set to transparent
        else:
            new_data.append(item)
    
    # Update the image data with the new transparent background
    wordcloud_image.putdata(new_data)
    
    # Save the word cloud to a BytesIO object
    buf = io.BytesIO()
    wordcloud_image.save(buf, format='PNG')
    buf.seek(0)
    
    # Encode the image to base64 for HTML embedding
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
    
    # Create a pie chart without any background color
    plt.figure(figsize=(12, 8), facecolor='none')  # No figure background color
    plt.gca().set_facecolor('none')  # No plot area background color
    
    wedges, texts, autotexts = plt.pie(sizes,
                                        labels=labels,
                                        autopct='%1.1f%%',
                                        startangle=140,
                                        colors=colors,
                                        shadow=shadow,
                                        explode=explode)  # Apply explosion to all slices

    # Improve readability of the labels and percentages
    for text in texts:
        text.set_fontsize(14)
        text.set_color('white')  # Set text color to black for contrast
        text.set_fontweight('bold')
        
    for autotext in autotexts:
        autotext.set_fontsize(14)
        autotext.set_color('white')  # Set percentage text color to black for contrast
        autotext.set_fontweight('bold')
    
    plt.title('Enhanced Pie Chart of Category Counts', fontsize=18, fontweight='bold', color='white')  # Set title color to black
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Save the pie chart to a BytesIO object with a transparent background
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=1, transparent=True)  # Save with transparent background
    buf.seek(0)
    
    # Encode image to base64 for HTML embedding
    pie_chart_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return pie_chart_base64

# ------------------------------------------ EMOJI CHART- --------------------------------------------
def plot_top_10_emojis(top_10_emojis):
    """
    Create a horizontal bar chart for the top 10 most common emojis
    and return it as a base64-encoded string.
    
    Args:
        top_10_emojis: A list of tuples containing the top 10 most common emojis and their counts.
        
    Returns:
        str: The base64-encoded string of the bar chart image.
    """
    emojis, counts = zip(*top_10_emojis)

    # Create a BytesIO object to save the chart image
    buf = io.BytesIO()
    
    # Create the bar chart
    plt.figure(figsize=(5,4.28))
    
    # Define the gap between bars
    bar_height = 0.8 # Adjust the height of the bars to increase the gap
    plt.barh(emojis, counts, color=(24/255, 24/255, 24/255), height=bar_height)
    
    # Remove background color and extra space
    plt.gca().patch.set_visible(False)  # Remove the background
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    
    plt.gca().yaxis.set_visible(False)  # Hide y-axis labels
    plt.gca().xaxis.set_visible(False)  # Ensure x-axis is visible
    
    # Remove any extra space from the left of the y-axis
    plt.subplots_adjust(left=0.1, right=0.8, top=0.9, bottom=0.1)
        
    plt.gca().invert_yaxis()  # Invert y-axis to have the highest counts at the top
    plt.tight_layout()  # Adjust layout to make room for labels
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0, transparent=True)
    plt.close()

    # Encode the image to base64
    buf.seek(0)
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return plot_data
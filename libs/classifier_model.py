from transformers import BertForSequenceClassification, BertTokenizer
import torch

# Path to the directory where the model and tokenizer are saved
model_path = 'D:/Christ University/4 Trimester/WEB PROJECT/Gir_dir/EMO/saved_model'
# Load the model and tokenizer
try:
    model = BertForSequenceClassification.from_pretrained(model_path)
    tokenizer = BertTokenizer.from_pretrained(model_path)
except Exception as e:
    print(f"Error loading model or tokenizer: {e}")
    raise

# Switch the model to evaluation mode
model.eval()
# Define label mapping
label_mapping = {
    0: 'Anger/Disgust',
    1: 'Happy/Joy',
    2: 'Neutral',
    3: 'Question',
    4: 'Sad',
    5: 'Suggestion',
    6: 'Surprise',
    7: 'Thankful'
}

# Define the prediction function
def predict_emotion(text):
    print('Trying')
    try:
        # Tokenize the input text
        inputs = tokenizer(text, return_tensors='pt', padding=True, truncation=True)
        print('Took inpus')
        # Make prediction
        with torch.no_grad():
            outputs = model(**inputs)
        print('Fetch outputs')
        # Get predicted class
        predictions = torch.argmax(outputs.logits, dim=1)
        predicted_index = predictions.item()
        
        # Convert prediction index to label
        predicted_label = label_mapping.get(predicted_index, 'Unknown label')
        print(f'------{text}-------------------{predicted_label}----------------------')
        return predicted_label
    except Exception as e:
        print(f"Error predicting emotion: {e}")
        return 'Error'

# Initialize dictionary with categories
categories = ["Anger/Disgust", "Happy/Joy", "Neutral", "Question", "Sad", "Suggestion", "Surprise", "Thankful"]

my_dict = {key: [] for key in categories}
print("Initialized dictionary:", my_dict)

def classify_text(text_list):
    print('trying big one')
    try:
        for text in text_list:
            if len(text) > 10:
                print('length passed')
                category = predict_emotion(text)
                print('value predicted')
                if category in my_dict:
                    print('adding')
                    my_dict[category].append(text)
                    print('added')
                else:
                    print(f"Category '{category}' not in predefined categories")
    except Exception as e:
        print(f"Error classifying text: {e}")


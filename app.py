# This works with neutrality
# finiteautomata/bertweet-base-sentiment-analysis

# The origianl, but doesn't have neutrality
# readerbench/RoBERT-large-sentiment

from tkinter import Label
from flask import Flask, render_template, request
from transformers import pipeline
from googletrans import Translator
from datetime import datetime

app = Flask(__name__)
sentiment_analyzer = pipeline(
        "sentiment-analysis",
        model="finiteautomata/bertweet-base-sentiment-analysis"
    )
translator = Translator()
analysis_results = []


def translate_to_english(text):
    try:
        detection = translator.detect(text)
        if detection.lang == 'en':
            return text, text, 'en'
        translation = translator.translate(text, src='ro', dest='en')
        return translation.text, text, detection.lang

    except Exception as e:
        print(f"Eroare traducere: {e}")
        return text, text, 'unknown'


def analyze_sentiment(text):
    result = sentiment_analyzer(text)
    return result[0]


def get_sentiment_info(label, confidence):
    if label == 'POS': #Pozitiv
        if confidence > 0.8:
            return "😊", "#28a745", "Pozitiv"
        else:
            return "🙂", "#6f42c1", "Posibil Pozitiv"
    if label == 'NEU':  #Neutru
        if confidence > 0.8:
            return "😐", "#FFA500", "Neutru"
        else:
            return "😐", "#FFA500", "Posibil Neutru"
    if label == 'NEG':  #Negativ
        if confidence > 0.8:
            return "😞", "#dc3545", "Negativ"
        else:
            return "😞", "#fd7e14", "Posibil Negativ"

@app.route('/')
def index():
    return render_template('index.html', results=analysis_results)


@app.route('/analyze', methods=['POST'])
def analyze():
    user_input = request.form['text_input']

    if user_input.strip():
        translated_text, original_text, detected_lang = translate_to_english(user_input)
        result = analyze_sentiment(translated_text)
        label = result['label']
        confidence = result['score']
        emoji, color, description = get_sentiment_info(label, confidence)
        analysis_entry = {
            'id': len(analysis_results) + 1,
            'text': original_text,  # Store original Romanian text
            'translated_text': translated_text if translated_text != original_text else None,
            'detected_language': detected_lang,
            'sentiment': description,
            'confidence': confidence,
            'emoji': emoji,
            'color': color,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        analysis_results.insert(0, analysis_entry)  # Most recent first
        print("=" * 60)
        print(f"Email Analysis #{analysis_entry['id']}")
        print(f"Detected Language: {detected_lang}")
        print(f"Original Text: '{original_text}'")
        if translated_text != original_text:
            print(f"Translated Text: '{translated_text}'")
        print(f"Sentiment: {description}")
        print(f"Confidence: {confidence:.4f}")
        print(f"Time: {analysis_entry['timestamp']}")
        print("=" * 60)
        return render_template('index.html', results=analysis_results, success=True)
    return render_template('index.html', results=analysis_results,
                           error="Vă rog să introduceți conținutul email-ului pentru analiză!")
if __name__ == '__main__':
    app.run(debug=True)
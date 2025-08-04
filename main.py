from transformers import pipeline
sentiment_analyzer = pipeline("sentiment-analysis")
def analyze_sentiment(text):
    result = sentiment_analyzer(text)
    return result[0]
if __name__ == "__main__":
    userInput = "Mario is a cool Italian person"
    print("Mario is judged as:")
    print("-"*40)
    result = analyze_sentiment((userInput))
    label = result['label']
    confidence = result['score']

    print(f"User input: '{userInput}'")
    print(f"Sentiment: {label}")
    print(f"Confidence: {confidence:.4f}")
    print("-" * 40)
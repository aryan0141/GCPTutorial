from django.http import HttpResponse
import json
import os
from google.cloud import translate_v2
from google.cloud import language
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"Google_Vision_API_Key.json"


def index(request):
    return render(request, "index.html")

# We have to exempt the csrf token, so that those requests can also be considered, which do not contain the csrf token.
@csrf_exempt
def englishToFrench(request):
    if request.method == "POST":
        # Initializes the translate model
        translate_model = translate_v2.Client()

        # Received the text from the POST Request
        text = request.POST["engText"]

        # Target language is choosen as French
        target = "fr"
        output = translate_model.translate(text, target_language=target)
        # Return the output in JSON Format
        return HttpResponse(json.dumps(output["translatedText"]))  

# Exempting the csrf token
@csrf_exempt
def sentimentAnalysis(request):
    if request.method == "POST":
        text = request.POST["text"]
        client = language.LanguageServiceClient()
        document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

        response = client.analyze_sentiment(document=document)
        sentiment = response.document_sentiment
        results = dict(
            text=text,
            score=f"{sentiment.score:.1%}",
            magnitude=f"{sentiment.magnitude:.1%}",
        )
        if "-" in results["score"]:
            return HttpResponse(json.dumps(f"Negative Sentiment with Score: {results['score']}")) 

        return HttpResponse(json.dumps(f"Positive Sentiment with Score: {results['score']}"))
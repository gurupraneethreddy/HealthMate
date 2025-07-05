import os
import io
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from dotenv import load_dotenv
from PIL import Image
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.ai.textanalytics import TextAnalyticsClient
from data import fetch_response_data

load_dotenv()

app = Flask(__name__)
app.secret_key = "supersecretkey"

VISION_KEY = "G1F1oBUUmLVIcrKIwuZfXw88cp1boE7rJnBJxVsZBQu2bp8U5Y9qJQQJ99BCACi5YpzXJ3w3AAAFACOGKW83"
VISION_ENDPOINT = "https://healthcare-computervision.cognitiveservices.azure.com/"

try:
    vision_client = ImageAnalysisClient(
        endpoint=VISION_ENDPOINT,
        credential=AzureKeyCredential(VISION_KEY)
    )
except Exception as e:
    print(f"Error initializing Vision client: {e}")
    exit()

LANGUAGE_KEY = os.getenv("LANGUAGE_KEY")
LANGUAGE_ENDPOINT = os.getenv("LANGUAGE_ENDPOINT")

try:
    language_client = TextAnalyticsClient(
        endpoint=LANGUAGE_ENDPOINT,
        credential=AzureKeyCredential(LANGUAGE_KEY)
    )
except Exception as e:
    print(f"Error initializing Language client: {e}")
    exit()

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class AWSLexClient:
    def __init__(self, region, bot_name, bot_alias,bot_id, alias_id):
        self.region = region
        self.bot_name = bot_name
        self.bot_alias = bot_alias
        self.bot_id = bot_id
        self.alias_id = alias_id
        self.endpoint = f"https://{bot_name}.lex.{region}.amazonaws.com"

    def invoke_lambda(self, message, lambda_function):
        raise NotImplementedError("AWS Lambda integration not configured.")

    def post_text(self, message):
        raise NotImplementedError("AWS Lex post_text not implemented.")

try:
    lex_client = AWSLexClient(
        region="ap-southeast-1",
        bot_name="HealthcareBot",
        bot_alias="TestBotAlias",
        bot_id="1CS3L2RJTA",
        alias_id="TSTALIASID"
    )
except Exception as e:
    print(f"AWS Lex client setup: {e}")

def _handle_input(message):
    return fetch_response_data(message)

def get_response(message):
    try:
        lex_client.post_text(message)
    except NotImplementedError:
        return _handle_input(message)

def analyze_image(image_bytes):
    try:
        visual_features = [
            VisualFeatures.TAGS,
            VisualFeatures.CAPTION,
            VisualFeatures.DENSE_CAPTIONS
        ]
        result = vision_client.analyze(
            image_data=image_bytes,
            visual_features=visual_features
        )
        return result
    except Exception as e:
        return {"error": str(e)}

def analyze_sentiment(text):
    try:
        documents = [text]
        response = language_client.analyze_sentiment(documents=documents, show_opinion_mining=True)
        return response[0] if not response[0].is_error else {"error": "Sentiment analysis failed"}
    except Exception as e:
        return {"error": str(e)}

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    image_path = None
    service_chosen = False
    selected_service = None

    if request.method == "POST":
        service_chosen = True
        selected_service = request.form.get("service")

        if selected_service == "computer-vision":
            file = request.files.get("image")
            if not file:
                flash("No image uploaded!")
                return redirect(url_for("home"))

            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)

            with Image.open(file_path) as image:
                image_bytes = io.BytesIO()
                image.save(image_bytes, format=image.format)
                image_bytes = image_bytes.getvalue()

            result = analyze_image(image_bytes)
            image_path = f"uploads/{file.filename}"

        elif selected_service == "sentiment-analysis":
            file = request.files.get("text_file")
            if not file:
                flash("No text file uploaded!")
                return redirect(url_for("home"))

            text = file.read().decode('utf-8')
            result = analyze_sentiment(text)

    return render_template("index.html", result=result, image_path=image_path, service_chosen=service_chosen, selected_service=selected_service)

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message")
    response = get_response(user_message)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
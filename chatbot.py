import spacy
from data_processing import predict_prices, load_data

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")

data = load_data('data/ethereum_price.csv')

def get_intent(user_message):
    doc = nlp(user_message.lower())
    intents = {
        "grafik harga historis": ["grafik harga historis", "historical price chart", "show me the historical prices"],
        "prediksi harga minggu": ["prediksi harga minggu depan", "forecast next week", "next week prediction"],
        "prediksi harga bulan": ["prediksi harga bulan depan", "forecast next month", "next month prediction"],
        "prediksi harga tahun": ["prediksi harga tahun depan", "forecast next year", "next year prediction"],
        "prediksi harga": [
            "prediksi harga 1 minggu", "prediksi harga 2 minggu", "prediksi harga 3 minggu", "prediksi harga 4 minggu",
            "prediksi harga 1 bulan", "prediksi harga 2 bulan", "prediksi harga 3 bulan", "prediksi harga 4 bulan",
            "prediksi harga 5 bulan", "prediksi harga 6 bulan", "prediksi harga 7 bulan", "prediksi harga 8 bulan",
            "prediksi harga 9 bulan", "prediksi harga 10 bulan", "prediksi harga 11 bulan",
            "prediksi harga 1 tahun", "prediksi harga 2 tahun", "prediksi harga 3 tahun", "prediksi harga 4 tahun", "prediksi harga 5 tahun"
        ]
    }
    
    for intent, patterns in intents.items():
        for pattern in patterns:
            if pattern in doc.text:
                return intent
    return None

def get_response(user_message):
    intent = get_intent(user_message)
    
    if intent == "grafik harga historis":
        response = "Berikut grafik harga historis: <img src='/static/historical_data.png' alt='Historical Data'>"
    elif intent in ["prediksi harga minggu", "prediksi harga bulan", "prediksi harga tahun", "prediksi harga"]:
        if '1 minggu' in user_message:
            periods = 7
        elif '2 minggu' in user_message:
            periods = 14
        elif '3 minggu' in user_message:
            periods = 21
        elif '4 minggu' in user_message:
            periods = 28
        elif '1 bulan' in user_message:
            periods = 30
        elif '2 bulan' in user_message:
            periods = 60
        elif '3 bulan' in user_message:
            periods = 90
        elif '4 bulan' in user_message:
            periods = 120
        elif '5 bulan' in user_message:
            periods = 150
        elif '6 bulan' in user_message:
            periods = 180
        elif '7 bulan' in user_message:
            periods = 210
        elif '8 bulan' in user_message:
            periods = 240
        elif '9 bulan' in user_message:
            periods = 270
        elif '10 bulan' in user_message:
            periods = 300
        elif '11 bulan' in user_message:
            periods = 330
        elif '1 tahun' in user_message:
            periods = 365
        elif '2 tahun' in user_message:
            periods = 730
        elif '3 tahun' in user_message:
            periods = 1095
        elif '4 tahun' in user_message:
            periods = 1460
        elif '5 tahun' in user_message:
            periods = 1825
        else:
            response = "Maaf, saya tidak mengerti pertanyaan Anda."
            return response
        
        if periods <= 1825:
            prediction = predict_prices(data, periods=periods)
            response = f"Prediksi harga untuk {periods//365} tahun ke depan: {prediction:.2f} USD"
            response += f"<img src='/static/prediction_{periods}.png' alt='Prediction Chart'>"
        else:
            response = "Maaf, prediksi hanya tersedia sampai 5 tahun ke depan."
    else:
        response = "Maaf, saya tidak mengerti pertanyaan Anda."
    return response

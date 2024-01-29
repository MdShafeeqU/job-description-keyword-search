from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods = ['GET','POST'])
def process_request():
    data = request.get_json()

    selected_text = data.get('text','')
    # print('Text Selected: ', selected_text)

    processed_text = selected_text.upper()

    print("Processed Text: ", processed_text)
    # return jsonify({'message': 'OK'})
    return jsonify({'processed_text': processed_text})

if __name__ == '__main__':
    app.run(port=8080)
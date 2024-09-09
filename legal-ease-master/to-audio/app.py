from flask import Flask, render_template, request, send_file, Response
import tempfile
import pyttsx3
import PyPDF2
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/text_to_speech', methods=['POST'])
def text_to_speech():
    text = request.form['text']
    rate = int(request.form['rate'])
    voice = request.form['voice']
    
    speaker = pyttsx3.init()
    speaker.setProperty('rate', rate)
    speaker.setProperty('voice', voice)
    speaker.say(text)
    speaker.runAndWait()
    
    return "Audio generated successfully"


@app.route('/pdf_to_speech', methods=['POST'])
def pdf_to_audio():
    file = request.files['file']
    start_page = int(request.form['start_page'])
    end_page = int(request.form['end_page'])
    rate = int(request.form['rate'])
    voice = request.form['voice']
    
    pdf_reader = PyPDF2.PdfReader(file)
    output_text = ""
    for page_number in range(start_page - 1, end_page):
        page = pdf_reader.pages[page_number]
        output_text += page.extract_text()
    
    speaker = pyttsx3.init()
    speaker.setProperty('rate', rate)
    speaker.setProperty('voice', voice)
    speaker.say(output_text)
    speaker.runAndWait()
    
    return "Audio generated successfully"

# Route to stop the audio playback
@app.route('/stop_audio', methods=['GET'])
def stop_audio():
    global stop_audio
    stop_audio = True
    return "Audio playback stopped"

if __name__ == '__main__':
    app.run(debug=True)


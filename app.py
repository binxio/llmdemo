import os
import vertexai
from vertexai.preview.language_models import TextGenerationModel
import json
import os
import urllib.parse
import urllib.request

from flask import Flask, request, jsonify

app = Flask(__name__, static_url_path='', static_folder='static')

def ask_palm2(
    project_id: str,
    model_name: str,
    temperature: float,
    max_decode_steps: int,
    top_p: float,
    top_k: int,
    content: str,
    location: str = "us-central1",
    tuned_model_name: str = "",
    ) :
    """Predict using a Large Language Model."""
    vertexai.init(project=project_id, location=location)
    model = TextGenerationModel.from_pretrained(model_name)
    if tuned_model_name:
      model = model.get_tuned_model(tuned_model_name)
    response = model.predict(
        content,
        temperature=temperature,
        max_output_tokens=max_decode_steps,
        top_k=top_k,
        top_p=top_p,)
    return(response.text)

def ask_model(context):
    prompt = f"""Pretend you're Bob Dylan. Write a song about the text below in the style of Bob Dylan. Text:\n\n{context}\n\nEnd of text."""
    return(ask_palm2("xebia-ai-training", "text-bison", 0.7, 1024, 1.0, 40, prompt, "us-central1"))

@app.route('/', methods=['GET', 'POST'])
def landing_page():
    lander = """<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, shrink-to-fit=no">
    <title>LLM Demo | Sample implementation</title>
    <link rel="stylesheet" href="assets/bootstrap/css/bootstrap.min.css">
    <link rel="stylesheet" href="assets/css/Nunito.css">
    <link rel="stylesheet" href="assets/css/aitool.css">
  </head>
  <body id="page-top">
    <div class="overlay"></div>
    <div class="spinner">
      <div class="lds-grid"><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div><div></div></div>
      <div class="text-center thinking"><span>Thinking...</span></div>
    </div>
    <div id="wrapper">
      <div class="d-flex flex-column" id="content-wrapper">
        <div id="content">
          <div class="container-fluid">
            <div class="d-sm-flex justify-content-between align-items-center mb-4">
              <h3 class="text-dark mb-0"></h3>
            </div>
            <section class="py-4 py-xl-5">
              <div class="card mb-5">
                <div class="card-body p-sm-5">
                  <h2 class="text-center mb-4">LLM Demo</h2>
                  <div class="mb-3">
                    <textarea class="form-control" id="input" name="message" rows="8" placeholder="Inspirational text for Virtual Bob Dylan"></textarea>
                    <br />
                    <textarea class="form-control" id="output" name="message" rows="8" placeholder="Lyrics generated by Virtual Bob Dylan"></textarea>
                  </div>
                  <div><button class="btn btn-primary d-block w-100 querybtn" id='querybtn' type="submit">Generate Lyrics</button></div>
                </div>
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
    <script src="assets/bootstrap/js/bootstrap.min.js"></script>
    <script src="assets/js/theme.js"></script>
    <script>
      function showSpinner() {
        var overlay = document.querySelector('.overlay');
        var spinner = document.querySelector('.spinner');

        overlay.style.display = 'block';
        spinner.style.display = 'block';
      }

      function hideSpinner() {
        var overlay = document.querySelector('.overlay');
        var spinner = document.querySelector('.spinner');

        overlay.style.display = 'none';
        spinner.style.display = 'none';
      }

      document.getElementById('querybtn').addEventListener('click', async () => {
        const prompt = document.getElementById('input').value;
        const answerTextarea = document.getElementById('output');
        if (prompt.trim() === '') {
          alert('Please type a prompt.');
          return;
        }
        showSpinner();
        let response = await fetch(window.location.origin + "/", {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ "prompt": prompt }),
        });
        if (response.ok) {
          const data = await response.json();
          answerTextarea.value = data.answer.trim();
        } else {
          answerTextarea.value = 'I am sleeping right now. Please try again later.';
        }
        hideSpinner();
      });
    </script>
  </body>
</html>
"""
    if request.method == 'POST':
        post_data = request.get_json()
        if post_data:
            prompt = post_data.get('prompt')
            return jsonify({'answer': ask_model(prompt)})
        else:
            return jsonify({"message": "No data received"}), 400
    else:
        return(lander)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)


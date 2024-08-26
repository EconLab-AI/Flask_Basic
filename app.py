import os
from flask import Flask, redirect, render_template, request, send_from_directory, url_for
from langchain_openai import AzureOpenAI

app = Flask(__name__)

# Umgebungsvariablen für Azure OpenAI
api_key = os.environ.get('API_KEY')
api_version = os.environ.get('API_VERSION')
azure_deployment = os.environ.get('AZURE_DEPLOYMENT')
model_name = os.environ.get('MODEL_NAME')

@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   req = request.form.get('req')

   # Azure OpenAI Client
   llm = AzureOpenAI(
       api_key=api_key,
       api_version=api_version,
       azure_deployment=azure_deployment,
       model_name=model_name,
   )

   response = llm.invoke(req)
   
   if req:
       print('Request for hello page received with req=%s' % req)
       return render_template('hello.html', req=response)
   else:
       print('Request for hello page received with no req or blank req -- redirecting')
       return redirect(url_for('index'))

if __name__ == '__main__':
   app.run(host='0.0.0.0', port=8000)

from flask import Flask, render_template, redirect, url_for
from flask import request, jsonify
from flask_apscheduler import APScheduler
import random 
import json 
import os
import subprocess
import sys
from collections import Counter
try:
    from datasets import load_dataset
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'datasets'])
finally:
    from datasets import load_dataset

prob_mt_ar = {
    'وصف':'صف',
    'تحديد':'حدد',
    'خلاصة':'لخص',
    'شرح':'اشرح',
    'اسم': 'سم'
}
prob_mt_en = {
    'وصف': 'describe',
    'تحديد': 'determine',
    'خلاصة':'summarize',
    'شرح':'explain',
    'اسم': 'name'
}

usa_related_words = [
    'الولايات المتحدة',
    'أمريكا',
    'نيويورك',
    'واشنكن',
    'لوس أنجلوس',
    'سان فرانسيسكو',
    'الهند',
    'الصين',
    'اليابان'
]

poem_related_words =[
    'قصيدة',
    'هايكو',
    'قصيده'
]

rem_indices = []
all_indices = []
curr_idx = 10_001
dataset = load_dataset('arbml/cidar', verification_mode='no_checks')

# set configuration values
class Config:
    SCHEDULER_API_ENABLED = True

app = Flask(__name__)
app.config.from_object(Config())

scheduler = APScheduler()

class Config:
    SCHEDULER_API_ENABLED = True

scheduler.init_app(app)

def get_finished_indices():
    return set()

def load_data():
    alpaca_arabic = load_dataset('arbml/alpagasus_cleaned_concatenated_ar')
    # new_column = list(range(len(alpaca_arabic['train'])))
    # alpaca_arabic['train'] = alpaca_arabic['train'].add_column("index", new_column)

    def filter_dataset(example):
        alphabets = 'abcdefghijklmnopqrstuvwxyz'
        inp = (example['instruction']+example['input']).strip() if 'input' in example else example['instruction'].strip()
        out = example['output']
        
        inp_en = example['instruction_en']+example['input_en'] if 'input_en' in example else example['instruction_en']
        # English insturctions
        # for alph in alphabets:
        #     if alph in inp+out:
        #         return True
        
        # empty insturctions
        # if inp.strip() == "" or out.strip() == "":
        #     return True
        
        # insturctions containing foreigh stuff
        for word in usa_related_words + poem_related_words:
            if word in inp:
                return True
        
        #instructions including certain words
        # for key in prob_mt_ar:
        #     if key in inp.split(' ')[0] and prob_mt_en[key] in inp_en.lower():
        #         return True
        # return False

    english_data = alpaca_arabic.filter(filter_dataset)
    # include random indices 
    extra_indices = []
    # random insturctions
    # extra_indices = [random.randint(0, len(alpaca_arabic['train'])-1) for _ in range(1000)]

    # all instructions 
    extra_indices = [i for i in range(len(alpaca_arabic['train']))]

    all_indices = set([sample['index'] for sample in english_data['train']] + extra_indices)

    return all_indices, alpaca_arabic

def save_json(entry):
    data = []
    if os.path.exists('static/data/dataset.json'):
        with open('static/data/dataset.json', encoding="utf-8") as f:
            data = json.load(f)
    
    new_entry = {}
    for key in entry:
        if key in ['instruction', 'output', 'index', 'version', 'Reviewed by']:
            new_entry[key] = entry[key]
    data.append(new_entry)

    with open('static/data/dataset.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii = False, indent=2)

@app.route('/api/submit',methods = ['POST', 'GET'])
def submit():
    if request.method == 'POST':
        element = {k:request.form[k] for k in request.form}
        element['version'] = 'v2'
        save_json(element)
    return render_template('index.html')
   
@app.route('/api/data')
def send_data():
    finished_indices = get_finished_indices()
    rem_indices = set(all_indices) - finished_indices
    index = random.choice(list(rem_indices))
    element = [ex for ex in dataset['train'] if index == int(ex['index'])][0]
    return jsonify(element)

@app.route('/api/getConNames')
def get_cont_names():
    with open('static/data/dataset.json', encoding="utf-8") as f:
        data = json.load(f)
    return jsonify(Counter([elm['Reviewed by'].strip().split(' ')[0].strip() for elm in data]))

@app.route('/api/getCon', methods = ['POST', 'GET'])
def get_cont():
    print(request.form)
    name = request.form['Reviewed by']
    with open('static/data/dataset.json', encoding="utf-8" ) as f:
        data = json.load(f)
    return jsonify({
        "num_cont":len([elm for elm in data if elm['Reviewed by'] == name])
    })

def get_max_idx():
    with open('static/data/dataset.json', encoding="utf-8") as f:
        data = json.load(f)
    return max([int(ex['index']) for ex in data])

@app.route('/api/empty')
def send_empty_data():
    element = {
            "instruction":'',
            "output" :'',
            "index":get_max_idx() + 1
        }
    return jsonify(element)

@app.route('/api/saved')
def send_saved_data():
    element = {
            "instruction":'',
            "output" :'',
            "index":-1
        }
    with open('static/data/dataset.json', encoding="utf-8") as f:
        data = json.load(f)
    if len(data):
        saved_indices = list(range(len(data)))
        index = random.choice(saved_indices)
        element = data[index]
    return jsonify(element)

@scheduler.task('interval', id='do_push_hf', hours=1)
def push_hub():
    TOKEN = os.environ.get('HF_TOKEN')
    subprocess.run(["huggingface-cli", "login", "--token", TOKEN])
    with open('static/data/dataset.json', encoding="utf-8") as f:
        data = json.load(f)
    
    if len(data):
        dataset = load_dataset("json", data_files="static/data/dataset.json",  download_mode = "force_redownload")
        dataset.push_to_hub('arbml/cidarv2')

def init_dataset():
    global rem_indices, dataset, all_indices
    os.makedirs('static/data', exist_ok=True)
    try:
        data = []
        for i, ex in enumerate(dataset['train']):
            ex['Reviewed by'] = ''
            ex['version'] = 'v1'
            all_indices.append(int(ex['index']))
            for word in usa_related_words:
                if word in ex['instruction'] + ex['output']:
                    rem_indices.append(int(ex['index']))
                    break
            else:
                data.append(ex)
    except:
        data = []

    with open('static/data/dataset.json', 'w', encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii = False, indent=2)
    
@app.route('/explore')
def explore():
    return render_template('explore.html')

@app.route('/review')
def review():
    return render_template('review.html')

@app.route('/')
def index():
    return render_template('index.html')

init_dataset()
scheduler.start()

if __name__ == '__main__':
    app.run(port=5000)

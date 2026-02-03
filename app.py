from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
import requests
import webbrowser
import threading
import time

app = Flask(__name__)
CORS(app)

# Fix Vue.js/Jinja2 conflict (if needed in future)
app.jinja_env.variable_start_string = '[['
app.jinja_env.variable_end_string = ']]'

@app.route('/')
def index():
    return render_template('tracker.html')

@app.route('/api/issues')
def get_issues():
    # 1. Get Credentials from Headers
    api_key = request.headers.get('X-Redmine-Key')
    base_url = request.headers.get('X-Redmine-Url')

    if not api_key or not base_url:
        return jsonify({"error": "Missing API Key or Redmine URL in Settings"}), 400

    base_url = base_url.rstrip('/')

    # 2. Build Params
    params = request.args.to_dict()
    params['key'] = api_key
    params['limit'] = 100
    if 'status_id' not in params:
        params['status_id'] = 'open' 
    params['include'] = 'description,relations'

    all_issues = []
    offset = 0
    
    try:
        # --- PAGINATION LOOP ---
        while True:
            params['offset'] = offset
            resp = requests.get(f"{base_url}/issues.json", params=params)
            resp.raise_for_status()
            data = resp.json()
            
            issues_batch = data.get('issues', [])
            if not issues_batch:
                break
                
            all_issues.extend(issues_batch)
            
            if len(issues_batch) < int(params['limit']):
                break
                
            offset += int(params['limit'])

        # --- SMART FETCH FOR BLOCKERS ---
        missing_ids = set()
        loaded_ids = set(issue['id'] for issue in all_issues)

        for issue in all_issues:
            if 'relations' in issue:
                for rel in issue['relations']:
                    if rel['issue_to_id'] == issue['id'] and rel['relation_type'] == 'blocks':
                         if rel['issue_id'] not in loaded_ids:
                             missing_ids.add(rel['issue_id'])
            if 'parent' in issue:
                if issue['parent']['id'] not in loaded_ids:
                    missing_ids.add(issue['parent']['id'])

        if missing_ids:
            ids_list = list(missing_ids)
            for i in range(0, len(ids_list), 100):
                chunk = ids_list[i:i + 100]
                extra_params = {
                    'key': api_key,
                    'issue_id': ",".join(str(x) for x in chunk),
                    'status_id': '*',
                    'limit': 100
                }
                extra_resp = requests.get(f"{base_url}/issues.json", params=extra_params)
                if extra_resp.ok:
                    all_issues.extend(extra_resp.json().get('issues', []))

        return jsonify({'issues': all_issues})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500

def open_browser():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:5000")

def main():
    print("Starting Next Cycle Tracker...")
    # Open browser automatically in a separate thread
    threading.Thread(target=open_browser).start()
    app.run(port=5000)

if __name__ == '__main__':
    main()
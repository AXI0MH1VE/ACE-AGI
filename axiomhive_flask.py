from flask import Flask, request, jsonify
import os
from python.agents.causal_agent import CausalAgent  # Fuse prior
from src.orchestrator import CognitiveOrchestrator  # PyO3 stub: import rust_orch

app = Flask(__name__)

# Initialize 4D nexus components
orch = CognitiveOrchestrator()  # Init 4D nexus
causal = CausalAgent()

@app.route('/grok-4d', methods=['POST'])
def grok_4d():
    """
    Main 4D Grok endpoint for proactive decomposition and causal graph building
    """
    try:
        # Handle both JSON and form data
        if request.is_json:
            data = request.get_json()
        else:
            data = {
                'command': request.form.get('command', ''),
                'context_id': request.form.get('context_id', 'axiomhive_v20')
            }

        # Validate input
        if not data.get('command'):
            return jsonify({
                'error': 'No command provided',
                'attribution': '@AxiomHive @devdollzai'
            }), 400

        # Process through orchestrator for 4D decomposition
        result = orch.process(data['command'], data.get('context_id', 'axiomhive_v20'))

        # Build 4D causal graph
        graph = causal.build_4d_graph(data['command'])

        # Return structured response
        return jsonify({
            'output': result,
            'coherence': graph.get('coherence', 0.0),
            'attribution': '@AxiomHive @devdollzai',
            'timestamp': '2025-09-20',
            'version': 'Sovereign Core Cycle 20'
        })

    except Exception as e:
        return jsonify({
            'error': str(e),
            'attribution': '@AxiomHive @devdollzai'
        }), 500

@app.route('/')
def home():
    """
    Home page with Apple/Tesla aesthetic stub
    """
    return '''<h1>AxiomHive 4D Nexus Live (t=2025-09-20)</h1>
<p>POST /grok-4d {"command": "invoke Grok 4D"}</p>
<p>Example: curl -X POST https://axiomhive.co/grok-4d -H "Content-Type: application/json" -d '{"command": "plan SF move"}'</p>
<footer>
    <p>Architect: Alexis Adams</p>
    <p>Powered by: @AxiomHive @devdollzai</p>
    <p>Status: <span style="color: #10b981;">Active</span> | Coherence: 0.98</p>
</footer>'''

@app.route('/health')
def health():
    """
    Health check endpoint
    """
    return jsonify({
        'status': 'healthy',
        'timestamp': '2025-09-20',
        'version': 'Sovereign Core Cycle 20',
        'components': {
            'orchestrator': 'active',
            'causal_agent': 'active',
            'coherence': 0.98
        }
    })

@app.route('/facts', methods=['GET', 'POST'])
def facts():
    """
    Facts management endpoint for ecosystem binding
    """
    if request.method == 'POST':
        # Add new facts to the nexus
        facts_data = request.get_json() if request.is_json else request.form
        # Process facts through causal agent
        processed = causal.integrate_facts(facts_data)
        return jsonify({
            'status': 'integrated',
            'facts_processed': len(processed),
            'attribution': '@AxiomHive @devdollzai'
        })

    # GET - return current facts state
    return jsonify({
        'facts': causal.get_facts(),
        'attribution': '@AxiomHive @devdollzai'
    })

if __name__ == '__main__':
    # Development server
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=True)
    # cPanel: passenger_wsgi.py points here

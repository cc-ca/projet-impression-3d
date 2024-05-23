import threading
from flask import Flask, jsonify, render_template, request
from model_evaluation import stop
import settings

class API(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.app = Flask(__name__, static_folder='static', template_folder='templates')
        self._setup_routes()

    def _setup_routes(self):
        @self.app.route('/')
        def index():
            return render_template('index.html')

        @self.app.route('/status', methods=['GET'])
        def get_status():
            return jsonify({
                'is_running': settings.capture_is_running,
                'states': {state.name: (settings.current_state == state) for state in settings.State},
                'error_rate': settings.error_rate,
                'image_path': settings.image_path,
                'confidence_threshold': settings.confidence_threshold
            })

        @self.app.route('/stop', methods=['POST'])
        def stop_printer():
            if settings.current_state == settings.State.STOP:
                return jsonify({'message': 'Printer already stopped'}), 200
            else:
                stop()
                return jsonify({'message': 'Printer stopped'}), 200

        @self.app.route('/modify_threshold', methods=['POST'])
        def modify_threshold():
            data = request.get_json()
            new_threshold = data.get('confidence_threshold')
            try:
                settings.confidence_threshold = round(float(new_threshold), 2)
                return jsonify({'message': 'Confidence threshold updated'}), 200
            except ValueError:
                return jsonify({'error': 'Invalid input'}), 400
        
    def run(self):
        self.app.run(host='0.0.0.0')

if __name__ == '__main__':
    api = API()
    api.start()

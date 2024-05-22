import threading
from flask import Flask, jsonify, render_template
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
                'image_name': settings.image_name
            })

        @self.app.route('/stop', methods=['POST'])
        def stop_printer():
            stop()
            return jsonify({'message': 'Printer stopped'}), 200

    def run(self):
        self.app.run(host='0.0.0.0')

if __name__ == '__main__':
    api = API()
    api.start()

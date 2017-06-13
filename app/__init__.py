from application import create_app, get_config

import logging

if __name__ == "__main__":
    config_class_string = 'config.Production'
    config_obj = get_config(config_class_string)

    app = create_app(config_obj)

    app.run(host = '0.0.0.0', port = '5000')
    

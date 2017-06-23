from application import get_config, create_app

config_class_string = 'app.config.Testing'
config_obj = get_config(config_class_string)
app = create_app(config_obj)

if __name__ == "__main__":
    app.run()


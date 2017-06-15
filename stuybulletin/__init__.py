from manage import create_app, parse_options, log_messages

app = create_app(parse_options())
app.run(host = '0.0.0.0', port = 5000)

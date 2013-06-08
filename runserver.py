from finder import app
import logging
import sys


handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)
app.run(debug=True)

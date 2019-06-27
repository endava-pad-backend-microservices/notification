from flask import Flask,redirect
from flask_restplus import Api,Resource
from flask_cors import CORS
import Config as configuration

##get and do configurations
config = configuration.configure()

app = Flask(__name__)
api = Api(app,title="Notification",default="Notification",default_label="")
cors = CORS(app)
app.config["CROS_HEADERS"] = "Content-Type"

@api.route("/v2/api-docs",doc=False)
class SwaggerController(Resource):
    @classmethod
    def get(self):
        url = "http://localhost:"+config["port"]+"/"+api.specs_url.split("/")[3]
        print(url)
        return redirect(url)

if __name__ == "__main__":
    app.run(debug=False, host=config["host"], port=config["port"])
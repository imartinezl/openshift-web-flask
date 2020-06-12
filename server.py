import os
from flask import Flask, render_template, session, redirect, url_for, jsonify, request
from flask_script import Manager,Server
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import Form
from wtforms import FloatField, SubmitField, StringField
from wtforms.validators import InputRequired, DataRequired
import tensorflow as tf
print(tf.__version__)
model = tf.keras.models.load_model('my_model')
print(model.summary())
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess my string'

CORS(app)

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


@app.route('/', methods=['POST'])
def index():
    content = request.get_data()
    print(content)
    result = model.predict([content.decode("utf-8")])
    print(result)
    # example_texts = ["This was an absolutely terrible movie. Don't be lured in by Christopher Walken or Michael Ironside. Both are great actors, but this must simply be their worst role in history. Even their great acting could not redeem this movie's ridiculous storyline. This movie is an early nineties US propaganda piece. The most pathetic scenes were those when the Columbian rebels were making their cases for revolutions. Maria Conchita Alonso appeared phony, and her pseudo-love affair with Walken was nothing but a pathetic emotional plug in a movie that was devoid of any real meaning. I am disappointed that there are movies like this, ruining actor's like Christopher Walken's good name. I could barely sit through it.",
    # "This is the kind of film for a snowy Sunday afternoon when the rest of the world can go ahead with its own business as you descend into a big arm-chair and mellow for a couple of hours. Wonderful performances from Cher and Nicolas Cage (as always) gently row the plot along. There are no rapids to cross, no dangerous waters, just a warm and witty paddle through New York life at its best. A family film in every sense and one that deserves the praise it received."]
    # result = model.predict(example_texts)
    # print(result)
    return jsonify({'result': result.tolist()})
    return render_template('base.html')


if __name__ == '__main__':
    manager.add_command('runserver', Server(host=os.getenv('IP', '0.0.0.0'),port=int(os.getenv('PORT', 8080))))
    manager.run()

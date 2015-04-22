import os
from flask import Flask, request, send_from_directory
from flask import render_template
from constants import Category, categories

app = Flask(__name__, static_folder='static', static_url_path='')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['UPLOAD_FOLDER'] = os.path.realpath('.') + '/uploads/'

def get_c_id(c_id):
    try:
        vcid = int(c_id)
        if vcid in [c.value for c in Category]:
            return vcid
        else:
            return Category.painting_and_calligraphy1.value
    except Exception, e:
        print 'got exception, %s' % str(e)
        return Category.painting_and_calligraphy1.value


@app.route('/')
@app.route('/category/<int:c_id>/')
def category_list(c_id=Category.painting_and_calligraphy1.value):
    valid_c_id = get_c_id(c_id)
    active_category = valid_c_id
    images = []
    return render_template('index.html',
                            active_category=active_category,
                            categories=categories,
                            images=images)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


if __name__ == '__main__':
    app.run(debug=True)


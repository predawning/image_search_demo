import os
import uuid
import glob
from flask import Flask, request, send_from_directory
from flask import render_template, redirect, url_for
from constants import Category, categories
from search import match, getDes

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

def get_images(c_id, upload_img=''):
    spath = "static/dataset/%s/pages/*.jpg" % c_id
    images = glob.glob(spath)
    r_d = []
    if upload_img:
        upload_img = '.' + upload_img
        des1 = getDes(upload_img)
        for imagePath in images:
            des2 = getDes(imagePath)
            pts = match(des1, des2)
            print '%s file with %s maches' % (imagePath, pts)
            r_d.append([imagePath, pts])
        r_d = sorted(r_d, key=lambda x:x[1], reverse=True)
        return [p[0] for p in r_d]
    else:
        return images


@app.route('/')
@app.route('/category/<int:c_id>/')
@app.route('/search/<int:c_id>/<upload_img>/')
def category_list(c_id=Category.painting_and_calligraphy1.value,
                  upload_img=''):
    valid_c_id = get_c_id(c_id)
    active_category = valid_c_id
    if upload_img:
        upload_img = '/uploads/%s.jpg' % upload_img
    images = get_images(valid_c_id, upload_img)[:12]
    images = [imagePath.replace('static/', '/') for imagePath in images]

    return render_template('index.html',
                            active_category=active_category,
                            categories=categories,
                            upload_img=upload_img,
                            images=images)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/upload', methods=['GET', 'POST'])
def upload_test():
    """Upload a new file."""
    if request.method == 'POST':
        file = request.files['upload']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return redirect(url_for('uploaded_file',
                                    filename=filename))
    return (
        u'<form method="POST" enctype="multipart/form-data">'
        u'  <input name="upload" type="file">'
        u'  <button type="submit">Upload</button>'
        u'</form>'
    )

# Route that will process the file upload
@app.route('/category/<int:c_id>/upload/', methods=['POST'])
def upload(c_id):
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        #filename = secure_filename(file.filename)
        upload_img = str(uuid.uuid1())
        filename = upload_img + '.jpg'
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print 'saved image %s' % filename
        # Redirect the user to the uploaded_file route, which
        # will basicaly show on the browser the uploaded file
        return redirect(url_for('category_list',
                                c_id=c_id,
                                upload_img=upload_img))
    else:
        return redirect(url_for('category_list'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=39000)


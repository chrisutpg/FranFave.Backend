from flask import Blueprint, render_template

test1 = Blueprint('test', __name__, url_prefix='/test')
search = Blueprint('search', __name__, url_prefix='/test')


@test1.route('/test1', methods=['GET'])
def test():
    return render_template('test.html')

@search.route('/test2', methods=['GET'])
def test2():
    return render_template('test2.html')
from bson import ObjectId
from flask_restful import Resource, reqparse
from model.articles import Articles
from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

modelArticles = Articles()

parser = reqparse.RequestParser()
parser.add_argument('title', type=str, required=True, help="Parameter 'title' can not be blank", location='form')
parser.add_argument('content', type=str, required=True, help="Parameter 'content' can not be blank", location='form')
parser.add_argument('username', type=str, required=True, help="Parameter 'username' can not be blank", location='form')
parser.add_argument('date', type=str, required=True, help="Parameter 'date' can not be blank", location='form')


UPLOAD_FOLDER = "uploads/articles"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif"}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


class ArticlesController(Resource):
    # @jwt_required()
    def get(self, articleId=None):
        skip = int(request.args.get("skip", 0))
        limit = int(request.args.get("limit", 8))
        if articleId:
            result = modelArticles.findArticleById(articleId)
            if result['status']:
                return result, 200
            else:
                return result, 404
        else:
            return modelArticles.findAllArticles(skip=skip, limit=limit)

    @jwt_required()
    def post(self):
        image = request.files.get('image')
        args = parser.parse_args()

        # Check for duplicate title
        try:
            articles_data = modelArticles.findAllArticles()
            if articles_data.get('data'):
                listTitles = [article['title'] for article in articles_data['data']]
                if args['title'] in listTitles:
                    return {'status': False, 'message': 'Title sudah ada'}, 400
        except Exception as e:
            return {"status": False, "error": str(e)}, 500

        # Save image file and get filename
        saved_images = []
        for image in request.files.getlist('image'):
            if image and allowed_file(image.filename):
                filename = secure_filename(image.filename)
                image_path = os.path.join(UPLOAD_FOLDER, filename)
                image.save(image_path)
                saved_images.append(filename)
            else:
                return {"status": False, "message": "Image file is required or invalid"}, 400
            
        data = {
            'title': args['title'],
            'content': args['content'],
            'username': args['username'],
            'date': args['date'],
            'image': saved_images
        }

        resultInsert = modelArticles.insertArticles(data)
        return {'status': resultInsert.get('status'), 'message': resultInsert.get('message'), 'data': data}, 200 if resultInsert.get('status') else 400

import datetime
from flask_restful import Resource, reqparse
from model.emotion import Emotion
from flask import request

emotion = Emotion()
parser = reqparse.RequestParser()
parser.add_argument('username', type=str, required=True, help="Parameter 'username' can not be blank")
parser.add_argument('date', type=str, required=True, help="Parameter 'date' can not be blank")  # Accept as string
parser.add_argument('emotion', type=str, required=True, help="Parameter 'emotion' can not be blank")

class EmotionController(Resource):
    def get(self):
        result = emotion.findAllEmotions()
        return result
    
    def post(self):
        args = parser.parse_args()
        try:
            datetime.datetime.fromisoformat(args['date'])
        except ValueError:
            return {"message": "Parameter 'date' must be in ISO format"}, 400

        data = {
            'username': args['username'],
            'date': args['date'],
            'emotion': args['emotion']
        }
        resultInsert = emotion.insertEmotion(data)
        return resultInsert, 200 if resultInsert.get('status') == True else 400
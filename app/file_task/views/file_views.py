from flask_restful import abort, reqparse, request
from flask import send_file
from flask_apispec import use_kwargs, marshal_with, doc
from flask_apispec.views import MethodResource
from marshmallow import fields, Schema
from io import BytesIO
from app.file_task.models.file_model import FileModel

import zipfile
import os


class fileSchema(Schema):
    file_success = fields.Bool()


class FileView(MethodResource):
    """File View"""

    @doc(description='DEMO FILE API', tags=['File'])
    # @use_kwargs({'file_id': fields.Str(required=True)}, location='headers')
    @marshal_with(fileSchema)
    def get(self, **kwargs):
        # file_id = kwargs.get('file_id')
        try:
            last_item = FileModel.query.filter_by(current_cursor=True).first()
            if not last_item:
                download = FileModel.query.first()
            else:
                current_item = last_item.id + 1
                download = FileModel.query.get(current_item)
                download.current_cursor = True
            # zipf = zipfile.ZipFile('file.zip', 'w')
            return send_file(BytesIO(download.data), attachment_filename=download.filename, as_attachment=True)
        except Exception as e:
            print(e)
            abort(500, message='internal error')

    @doc(description='DEMO FILE API', tags=['File'])
    @marshal_with(fileSchema)
    def post(self, **kwargs):
        try:
            file = request.files['file_1']
            upload = FileModel(filename=file.filename, data=file.read())
            FileModel.save(upload)
        except Exception as e:
            print(e)
            abort(500, message='internal error')
        else:
            return {'file_success': True}, 200
import codecs
import csv
import functools

from flask import jsonify, request

from .db import db


def expects_file(extensions=['txt', 'csv']):
    def decorator_expects_file(view):
        functools.wraps(view)

        def new_view(*args, **kwargs):
            if 'file' not in request.files:
                return jsonify({'message': 'No file in data'}), 400
            file = request.files['file']
            if file.filename == '':
                return jsonify({'message': 'No file selected'}), 400
            extension = file.filename.lower().rpartition('.')[2]
            if extension not in extensions:
                return jsonify({'message': 'Invalid file extension'}), 400
            return view(*args, file, **kwargs)
        return new_view
    return decorator_expects_file


class FileEmptyError(Exception):
    pass


class FieldError(Exception):
    def __init__(self, field_name, *args, **kwargs):
        self.field_name = field_name
        super().__init__(*args, **kwargs)


class MissingFieldError(FieldError):
    pass


class InvalidFieldError(FieldError):
    pass


def csv_to_dicts(
    file,
    required_fields=[],
    optional_fields=[],
    restrict_fields=False
):
    rows = csv.reader(file)
    header_row = next(rows, None)
    if header_row is None:
        raise FileEmptyError
    fields = [field.strip() for field in header_row]
    for required_field in required_fields:
        if required_field not in fields:
            raise MissingFieldError(required_field)
    if restrict_fields:
        accepted_fields = required_fields + optional_fields
        for field in fields:
            if field not in accepted_fields:
                raise InvalidFieldError(field)
    return [
        {fields[i]: v for i, v in enumerate(row)}
        for row in rows
    ]


expects_csv_file = expects_file(extensions=['csv'])


@expects_csv_file
def import_csv_view(model, file, required_fields=[], optional_fields=[]):
    try:
        records = [
            model(**d) for d in csv_to_dicts(
                codecs.iterdecode(file, 'utf-8'),
                required_fields=required_fields,
                optional_fields=optional_fields,
                restrict_fields=True,
            )
        ]
    except FileEmptyError:
        return (
            jsonify({
                'message': 'File is empty'
            }),
            400
        )
    except MissingFieldError as error:
        return (
            jsonify({
                'message': f'Missing field "{error.field_name}" in CSV header'
            }),
            400
        )
    except InvalidFieldError as error:
        return (
            jsonify({
                'message': f'Invalid field "{error.field_name}" in CSV header'
            }),
            400
        )
    db.session.add_all(records)
    db.session.commit()

    return jsonify(), 200

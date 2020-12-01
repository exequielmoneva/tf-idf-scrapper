from marshmallow import Schema, fields


class TfIdfSchema(Schema):
    term = fields.String()
    tf_idf = fields.Float()


class ReturnSchema(Schema):
    terms = fields.Nested(TfIdfSchema)


tfidf = TfIdfSchema()
tfidf = TfIdfSchema(many=True)
jresponse = ReturnSchema()
jresponse = ReturnSchema(many=True)

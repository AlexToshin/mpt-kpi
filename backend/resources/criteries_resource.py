from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from services.certificates_generator import Certificate, certificates_list
from services.criteries_generator import Criterion, criteries_list

class UserCertificatesResource(Resource):
    @login_required
    def get(self):
        # Параметры запроса: фильтрация по пользователю
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=False, default=current_user.id)
        args = parser.parse_args()

        # Фильтрация сертификатов по user_id (эмуляция через чётность ID)
        user_certificates = [cert for cert in certificates_list if cert.id % 2 == args['user_id'] % 2]

        result = []
        for cert in user_certificates:
            criterion = next((c for c in criteries_list if c.id == cert.criterion_id), None)
            if criterion:
                result.append({
                    "id": cert.id,
                    "preview_url": cert.preview_url,
                    "criterion": {
                        "id": criterion.id,
                        "name": criterion.name,
                        "mark_from": criterion.mark_from,
                        "mark_to": criterion.mark_to
                    }
                })

        return result, 200

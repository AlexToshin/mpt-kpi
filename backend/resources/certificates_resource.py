from flask_restful import Resource, reqparse
from flask_login import login_required, current_user
from services.certificates_generator import Certificate, certificates_list
from services.criteries_generator import Criterion, criteries_list

class CertificatesResource(Resource):
    @login_required
    def get(self):
        # Параметры запроса: user_id, page, per_page
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=False, default=current_user.id)
        parser.add_argument('page', type=int, required=False, default=1)
        parser.add_argument('per_page', type=int, required=False, default=5)
        args = parser.parse_args()

        # Фильтрация сертификатов по user_id (эмуляция через чётность ID)
        user_certificates = [cert for cert in certificates_list if cert.id % 2 == args['user_id'] % 2]

        # Пагинация
        total = len(user_certificates)
        start = (args['page'] - 1) * args['per_page']
        end = start + args['per_page']
        paginated_certs = user_certificates[start:end]

        # Формируем ответ с учётом пагинации
        result = []
        for cert in paginated_certs:
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

        # Возвращаем данные и информацию о пагинации
        return {
            "certificates": result,
            "pagination": {
                "total": total,
                "page": args['page'],
                "per_page": args['per_page']
            }
        }, 200

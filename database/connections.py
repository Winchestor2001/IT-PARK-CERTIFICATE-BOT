from playhouse.shortcuts import model_to_dict

from data.config import ADMINS
from .models import *
from utils.misc.context import districts_statistics


async def add_user(user_id: int, username: str):
    with db:
        if not Users.select().where(Users.user_id == user_id).exists():
            Users.create(user_id=user_id, username=username)


async def insert_user_certificate(unique_id, file_id, category, district):
    with db:
        Certificate.create(
            certificate_id=unique_id, certificate=file_id, certificate_category=category, certificate_district=district
        )


async def get_certificate_by_id(unique_id):
    with db:
        certificate = Certificate.select().where(Certificate.certificate_id == unique_id)
        certificate = [model_to_dict(item) for item in certificate]
        return certificate[0]


async def get_all_certificates():
    with db:
        certificates = Certificate.select()
        certificates = [model_to_dict(item) for item in certificates]
        return certificates


async def filter_districts(data):
    with db:
        result = []
        for item in data.values():
            districts = Certificate.select().filter(certificate_district=item)
            result.append(len([model_to_dict(item) for item in districts]))
        return result


async def get_total_certificate():
    with db:
        total_certificate = Certificate.select().count()
        return total_certificate


async def filter_district_category(district):
    with db:
        ks = Certificate.select().where((Certificate.certificate_district == district) & (Certificate.certificate_category == 'Kampyuter s.')).count()
        android = Certificate.select().where((Certificate.certificate_district == district) & (Certificate.certificate_category == 'Android')).count()
        back = Certificate.select().where((Certificate.certificate_district == district) & (Certificate.certificate_category == 'Backend')).count()
        front = Certificate.select().where((Certificate.certificate_district == district) & (Certificate.certificate_category == 'Frontend')).count()
        graphic = Certificate.select().where((Certificate.certificate_district == district) & (Certificate.certificate_category == 'Graphic design')).count()
        robot = Certificate.select().where((Certificate.certificate_district == district) & (Certificate.certificate_category == 'Robotics')).count()
        dx = Certificate.select().where((Certificate.certificate_district == district) & (Certificate.certificate_category == 'Davlat xodimi')).count()
        ssv = Certificate.select().where((Certificate.certificate_district == district) & (Certificate.certificate_category == 'SSV')).count()

        return districts_statistics.format(
            ks, android, back, front, graphic, robot, dx, ssv
        )


import random
from datetime import date, datetime

from django.core.management.base import BaseCommand
from django.utils import timezone

from models import Class, Course, Venue


class Command(BaseCommand):
    help = "Seeder database"

    def handle(self, *args, **kwargs):
        # TODO: add arguement for table name
        self.venues()
        self.courses()
        self.groups()

    def groups(self, *args, **kwargs):
        self.stdout.write("Populating classes table")

        programs = [
            "B.Ed. (Arts)",
            "B.Ed. (Social Science)",
            "B.Ed. (Social Studies)",
            "B.Ed. (Accounting)",
            "B.Ed. (Management)",
            "B.Ed. (Science),",
            "B.Ed. (Mathematics)",
            "B.Ed. (Computer Science)",
            "B.Ed. (Health Science)",
            "B.Ed. (Health, Physical Education & Recreation)",
            "B.Ed. (Home Economics)",
            "B.Sc. (Computer Science)",
            "B.Sc. (Engineering Physics)",
            "B.Sc. (Industrial Chemistry)",
            "B.Sc. (Information Technology)",
            "B.Sc. (Laboratory Technology)",
            "B.Sc. (Mathematics)",
        ]
        levels = [1, 2, 3, 4]

        for p in programs:
            now = datetime.now()
            start = date(now.year - random.choice(levels), 8, 21)
            end = date(start.year + 4, 8, 21)
            Class(
                program=p,
                size=random.randint(50, 150),
                admission_year=start,
                completion_year=end,
            ).save()

    def venues(self, *args, **kwargs):
        self.stdout.write("Populating venues table")
        data = [f"G{i+1}" for i in range(20)]
        data.extend([f"LT{i+1}" for i in range(20)])
        data.extend([f"CALC{i+1}" for i in range(10)])

        for v in data:
            Venue(name=v, capacity=random.randint(50, 150)).save()

    def courses(self, *args, **kwargs):
        self.stdout.write("Populating courses table")
        data = [
            {"code": "INF311", "title": "DATA STRUCTURES", "credit_hours": 3},
            {"code": "INF315", "title": "DISCRETE MATHEMATICS", "credit_hours": 3},
            {
                "code": "INF309",
                "title": "INFORMATION SYSTEM MANAGEMENT 3",
                "credit_hours": 3,
            },
            {"code": "INF305", "title": "NETWORK COMPUTING I", "credit_hours": 3},
            {"code": "INF307", "title": "SOFTWARE ENGINEERING", "credit_hours": 3},
            {"code": "INF313", "title": "WEB TECHNOLOGY I", "credit_hours": 3},
            {"code": "CMS108", "title": "COMMUNICATIVE SKILLS", "credit_hours": 3},
            {"code": "INF110", "title": "COMPUTER HARDWARE", "credit_hours": 3},
            {
                "code": "LED120",
                "title": "EARLY CHILDHOOD CARE AND DEVELOPMENT",
                "credit_hours": 2,
            },
            {
                "code": "ITS101",
                "title": "INFORMATION TECHNOLOGY SKILLS",
                "credit_hours": 2,
            },
            {
                "code": "INF112",
                "title": "MATHEMATICS FOR COMPUTING II",
                "credit_hours": 3,
            },
            {"code": "INF102", "title": "PROGRAMMING", "credit_hours": 3},
        ]
        for course in data:
            Course(
                code=course["code"],
                title=course["title"],
                credit_hours=course["credit_hours"],
            ).save()

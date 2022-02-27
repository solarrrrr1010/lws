import math, json

from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.core.cache import cache

from temp.models import Person, VisitOccurrence, Death, Concept

# 환자 수, 방문 수 통계 제공
class Statistics(View):
    def get(self, request):
        # 방문자의 출생연도와 방문연도를 가져와 (방문일자-출생연도)+1을 통해 방문 당시 나이대를 확인
        # 10세 단위 변경을 위해 방문자의 나이대를 모두 정수 내림 계산
        age_list = [
            math.floor(j / 10) * 10
            for j in [
                (i["visit_start_date"].year - i["person__year_of_birth"]) + 1
                for i in VisitOccurrence.objects.select_related("person").values(
                    "person__year_of_birth", "visit_start_date"
                )
            ]
        ]

        result = {
            "person_result ": {
                "total_person": len(Person.objects.all()),
                "gender": {
                    "Male": len(Person.objects.filter(gender_source_value="M")),
                    "Female": len(Person.objects.filter(gender_source_value="F")),
                },
                "race": {
                    "asian": len(Person.objects.filter(race_source_value="asian")),
                    "black": len(Person.objects.filter(race_source_value="black")),
                    "white": len(Person.objects.filter(race_source_value="white")),
                },
                "ethnicity": {
                    "hispanic": len(
                        Person.objects.filter(ethnicity_source_value="hispanic")
                    ),
                    "nonhispanic": len(
                        Person.objects.filter(ethnicity_source_value="nonhispanic")
                    ),
                },
                "death": "pk값 부재로 접근 불가",  # len(Death.objects.all())
            },
            "visit_result": {
                "visit_type": {
                    "inpatient": len(
                        VisitOccurrence.objects.filter(visit_concept_id=9201)
                    ),
                    "outpatient": len(
                        VisitOccurrence.objects.filter(visit_concept_id=9202)
                    ),
                    "emergency": len(
                        VisitOccurrence.objects.filter(visit_concept_id=9203)
                    ),
                },
                "visit_gender": {
                    "Male": len(
                        VisitOccurrence.objects.filter(person__gender_source_value="M")
                    ),
                    "Female": len(
                        VisitOccurrence.objects.filter(person__gender_source_value="F")
                    ),
                },
                "visit_race": {
                    "asian": len(
                        VisitOccurrence.objects.filter(
                            person__race_source_value="asian"
                        )
                    ),
                    "black": len(
                        VisitOccurrence.objects.filter(
                            person__race_source_value="black"
                        )
                    ),
                    "white": len(
                        VisitOccurrence.objects.filter(
                            person__race_source_value="white"
                        )
                    ),
                },
                "visit_ethnicity": {
                    "hispanic": len(
                        VisitOccurrence.objects.filter(
                            person__ethnicity_source_value="hispanic"
                        )
                    ),
                    "nonhispanic": len(
                        VisitOccurrence.objects.filter(
                            person__ethnicity_source_value="nonhispanic"
                        )
                    ),
                },
                "visit_age": {
                    "10대 이하": age_list.count(0),
                    "10대": age_list.count(10),
                    "20대": age_list.count(20),
                    "30대": age_list.count(30),
                    "40대": age_list.count(40),
                    "50대": age_list.count(50),
                    "60대": age_list.count(60),
                    "70대": age_list.count(70),
                    "80대": age_list.count(80),
                    "90대": age_list.count(90),
                    "100대": age_list.count(100),
                    "110대": age_list.count(110),
                },
            },
        }
        return JsonResponse(result, status=200)


class ConceptInfo(View):
    def get(self, request):
        search = {
            "cc": "condition_concept",
            "ctc": "condition_type_concept",
            "cstc": "condition_status_concept",
            "csoc": "condition_source_concept",
            "dc": "drug_concept",
            "dtc": "drug_type_concept",
            "rc": "route_concept",
            "dsc": "drug_source_concept",
            "gc": "gender_concept",
            "rac": "race_concept",
            "vc": "visit_concept",
            "vtc": "visit_type_concept",
            "vsc": "visit_source_concept",
            "dtoc": "discharge_to_concept",
        }

        key = request.GET.get("data")
        offset = int(request.GET.get("offset", 1))
        limit = 10

        if not cache.get(search[key]):
            concept_info = Concept.objects.prefetch_related(search[key]).values(
                search[key]
            )

            result = [i for i in concept_info if i[search[key]] != None]
            cache.set(search[key], result, 300)

        context = {"concept_info": cache.get(search[key])[offset : offset + limit]}

        return JsonResponse(context, status=200)

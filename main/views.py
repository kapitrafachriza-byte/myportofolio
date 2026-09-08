from django.shortcuts import render

from main.models import Experience


def show_main(request):
    context = {
        "name": "Kapitra Fachriza Utomo",
        "npm": "2506623231",
        "study_program": "S1 Sistem Informasi",
        "bio": (
            "Information Systems student at Universitas Indonesia. "
            "Previously completed Highschool in just 2 consecutive year "
            "through accelerated program, reflecting my ability to adapt and learn."
        ),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Kapitra Fachriza Utomo",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)
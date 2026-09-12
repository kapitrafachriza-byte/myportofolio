from django.shortcuts import render

from main.models import Experience, Skill


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
        "experience_list": Experience.objects.all(),
    }
    return render(request, "index.html", context)


def show_experience(request):
    context = {
        "name": "Kapitra Fachriza Utomo",
        "experience_list": Experience.objects.all(),
    }
    return render(request, "experience.html", context)


def show_skills(request):
    categories = [
        ("programming", "green"),
        ("infosys", "blue"),
        ("softskill", "orange"),
    ]
    grouped_skills = []
    for cat_key, dot_color in categories:
        skills = Skill.objects.filter(category=cat_key)
        if skills.exists():
            grouped_skills.append({
                "title": skills.first().get_category_display(),
                "dot_color": dot_color,
                "skills": skills,
            })
    context = {
        "name": "Kapitra Fachriza Utomo",
        "grouped_skills": grouped_skills,
        "skill_list": Skill.objects.all(),
    }
    return render(request, "skills.html", context)

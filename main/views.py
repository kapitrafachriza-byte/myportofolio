import json

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.core import serializers

from main.forms import ExperienceForm
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
    raw_response = get_experience_json(request)
    experiences_data = json.loads(raw_response.content)

    category_dict = dict(Experience.EXPERIENCE_CHOICES)
    experience_list = []
    for item in experiences_data:
        fields = item["fields"]
        fields["id"] = item["pk"]
        fields["get_category_display"] = category_dict.get(
            fields.get("category"), fields.get("category")
        )
        fields["is_ongoing"] = fields.get("ended_at") is None
        experience_list.append(fields)

    filter_query = request.GET.get("title", "")

    context = {
        "name": "Kapitra Fachriza Utomo",
        "experience_list": experience_list,
        "filter_query": filter_query,
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


def create_experience(request):
    form = ExperienceForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("main:show_experience")

    context = {"form": form}
    return render(request, "create_experience.html", context)


def get_experience_json(request):
    title_query = request.GET.get("title", "")
    experiences = Experience.objects.all()

    if title_query:
        experiences = experiences.filter(title__icontains=title_query)

    experience_data = serializers.serialize("json", experiences)
    return HttpResponse(experience_data, content_type="application/json")


def edit_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    form = ExperienceForm(request.POST or None, instance=experience)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect("main:show_experience")

    context = {"form": form}
    return render(request, "edit_experience.html", context)


def delete_experience(request, id):
    experience = get_object_or_404(Experience, pk=id)
    experience.delete()
    return redirect("main:show_experience")


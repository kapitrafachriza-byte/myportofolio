from django.urls import path

from main.views import (
    show_main,
    show_experience,
    show_skills,
    create_experience,
    get_experience_json,
    edit_experience,
    delete_experience,
    toggle_star,
)

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path("experience/json/", get_experience_json, name="get_experience_json"),
    path("skills/", show_skills, name="show_skills"),
    path("create-experience/", create_experience, name="create_experience"),
    path("edit-experience/<uuid:id>/", edit_experience, name="edit_experience"),
    path("delete-experience/<uuid:id>/", delete_experience, name="delete_experience"),
    path("experience/<uuid:experience_id>/star/", toggle_star, name="toggle_star"),
]


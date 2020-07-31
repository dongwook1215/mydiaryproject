from django.shortcuts import render
from .models import Diary
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.


def main(request):
    diary = Diary.objects.all().order_by("-id")
    return render(request, "main.html", {"diary": diary})


def detail(request, diary_id):
    diary_all = Diary.objects.all().order_by("-id")
    count = Diary.objects.count()
    diary = get_object_or_404(Diary, page_number=diary_id)
    return render(request, "detail.html", {"diary_detail": diary, "row_count": count})


def next(request, diary_id):
    count = Diary.objects.count()

    if diary_id + 1 > count:
        return redirect("/detail/1")
    else:
        return redirect("/detail/" + str(diary_id + 1))


def before(request, diary_id):
    count = Diary.objects.count()
    if diary_id - 1 == 0:
        return redirect("/detail/" + str(count))
    else:
        return redirect("/detail/" + str(diary_id - 1))


def write(request):
    if request.method == "POST":
        diary = Diary()
        diary.title = request.POST["title"]
        diary.body = request.POST["body"]
        diary.pub_date = timezone.datetime.now()
        diary.page_number = Diary.objects.count() + 1
        diary.save()
        return redirect("/detail/" + str(diary.page_number))
    else:
        return render(request, "write.html")


def rewrite(request, diary_id):
    if request.method == "POST":
        diary = get_object_or_404(Diary, page_number=diary_id)
        diary.title = request.POST["title"]
        diary.body = request.POST["body"]
        diary.pub_date = timezone.datetime.now()
        diary.save()
        return redirect("/detail/" + str(diary_id))
    else:
        diary = get_object_or_404(Diary, page_number=diary_id)
        return render(request, "rewrite.html", {"diary": diary})


def remove(request, diary_id):
    diary = get_object_or_404(Diary, page_number=diary_id)
    diary.delete()

    object_all = Diary.objects.all()
    for item in object_all:
        if item.page_number > diary_id:
            item.page_number = item.page_number - 1
            item.save()
        else:
            pass

    return redirect("/")

from django.shortcuts import render


def view_flowers(request):
    return render(request, "index.html")


def view_catalog(request):
    return render(request, "catalog.html")


def view_card(request):
    return render(request, "card.html")


def view_consultation(request):
    return render(request, "consultation.html")


def view_order(request):
    return render(request, "order.html")


def view_order_step(request):
    return render(request, "order-step.html")


def view_quiz(request):
    return render(request, "quiz.html")


def view_quiz_step(request):
    return render(request, "quiz-step.html")


def view_result(request):
    return render(request, "result.html")

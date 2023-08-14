from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from flower_shop import settings
from flowers import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.view_flowers, name="ViewFlowers"),
    path('catalog', views.view_catalog, name="ViewCatalog"),
    path('card', views.view_card, name="ViewCard"),
    path('consultation', views.view_consultation, name="ViewConsultation"),
    path('order', views.view_order, name="ViewOrder"),
    path('order-step', views.view_order_step, name="ViewOrderStep"),
    path('quiz', views.view_quiz, name="ViewQuiz"),
    path('quiz-step', views.view_quiz_step, name="ViewQuizStep"),
    path('result', views.view_result, name="ViewResult"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

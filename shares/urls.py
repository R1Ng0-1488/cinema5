from django.urls import path

from .views import ShareDetailVuew, PdfFilesView, ShareListView

urlpatterns = [
    path('shares/<slug:slug>', ShareDetailVuew.as_view(), name='share_detail'),
    path('shares/', ShareListView.as_view(), name='share_list'),
    path('documents/<slug:slug>', PdfFilesView.as_view(), name='pdf_file'),
]
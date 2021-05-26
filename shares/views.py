from django.shortcuts import render
from django.views.generic import DetailView, View, ListView
from django.http import HttpResponse

from django.core.files.storage import FileSystemStorage

from .models import Share, PdfFiles, City
# Create your views here.


class ShareListView(ListView):

	def get_queryset(self):
		city_slug = self.request.path.split('/')[1]
		city = City.objects.get(slug=city_slug)
		queryset = Share.objects.filter(city=city)
		return queryset


class ShareDetailVuew(DetailView):
    model = Share


class PdfFilesView(View):
    def get(self, request, city_slug, slug):
        pdf = PdfFiles.objects.get(slug=slug)
        fs = FileSystemStorage()
        with fs.open(pdf.file.name) as f:
            response = HttpResponse(f, content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{pdf.file.name}"'
        return response

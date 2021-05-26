
from .models import Share, PdfFiles
from movie.models import City


def shares(request):
    context = dict()
    try:
        city = City.objects.get(slug=str(request.path.split('/')[1]))
        share = Share.objects.filter(city=city)
        context['first_shares'] = share[:3]
        l = share[3:]
        context['last_shares'] = [l[i:i+3] for i in range(0, len(l), 3)]
    except City.DoesNotExist:
        pass
    context['pdf_files'] = PdfFiles.objects.all()
    return context

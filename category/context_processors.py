from .models import Category

def menu_links(request):
    links = Category.objects.all().order_by('-id')
    context={
        'links':links
    }
    return context
from .models import Category

def menu_links(request):
    links = Category.objects.all()
    context={
        'links':links
    }
    return context
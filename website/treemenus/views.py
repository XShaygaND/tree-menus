from django.shortcuts import render
from django.http import HttpResponseNotFound

from .models import MenuItem


def index(request):
    return render(request, 'treemenus/index.html')

def menu_view(request):
    def find_active_child(path, menu_items):
        for item in menu_items:
            if path == item.url:
                return item
        return None
    
    def create_hierarchy(menu_items, active_item, scope_item=None):
        item_list = []

        scope_item = active_item if not scope_item else scope_item

        if active_item.children:
            for parent in active_item.children.all():
                if parent.children:
                    for child in parent.children.all():
                        item_list.append(child)
                    item_list.append(parent)

                else:
                    item_list.extend(active_item.children.all())
        
        if scope_item.children and scope_item != active_item:
            item_list.extend(scope_item.children.all())

        item_list.append(scope_item)

        if scope_item.parent:
            item_list.extend(create_hierarchy(menu_items=menu_items, active_item=active_item, scope_item=scope_item.parent))

        else:
            item_list.extend([item for item in menu_items if not item.parent])

        item_list = list(dict.fromkeys(item_list))

        return item_list

    menu_name = request.path.split('/')[2]
    items = MenuItem.objects.filter(menu__name=menu_name).prefetch_related('children', 'menu')
    if not items:
        return HttpResponseNotFound(f"<h1>404 Not Found!</h1>\n<h2>`{menu_name}` Doesn't exist</h2>")

    active_item = find_active_child(request.path, items)
    if not active_item:
        return render(request, 'treemenus/menu.html', {
            'menu_items': [item for item in items if not item.parent],
            'active_item': active_item,
            'menu': items[0].menu,
            })

    menu_items = create_hierarchy(items, active_item)[::-1]

    return render(request, 'treemenus/menu.html', {
        'menu_items': menu_items,
        'active_item': active_item,
        'menu': items[0].menu,
        })

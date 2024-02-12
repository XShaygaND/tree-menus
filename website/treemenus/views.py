from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponse

from .models import MenuItem


def index(request):
    return render(request, 'treemenus/index.html')

def menu_view(request):
    def get_children(menu_items, active_item):
        return [item for item in menu_items if item.parent == active_item]
    
    def get_parent(menu_items, active_item):
        for item in menu_items:
            children = get_children(menu_items, item)
            print(children)
            if active_item in children:
                return item
            
    def find_active_child(path, menu_items):
        for item in menu_items:
            if path == item.url:
                return item
        return None
    
    def create_hierarchy(menu_items, active_item, scope_item=None):
        item_list = []

        scope_item = active_item if not scope_item else scope_item

        if active_item.children:
            for parent in get_children(menu_items, active_item):
                if parent.children:
                    for child in get_children(menu_items, parent):
                        item_list.append(child)
                    item_list.append(parent)

                else:
                    item_list.extend(get_children(menu_items, active_item))
        
        if scope_item.children and scope_item != active_item:
            item_list.extend(get_children(menu_items, scope_item))

        item_list.append(scope_item)

        if scope_item.parent:
            item_list.extend(create_hierarchy(menu_items=menu_items, active_item=active_item, scope_item=get_parent(menu_items, scope_item)))

        else:
            item_list.extend([item for item in menu_items if not item.parent])

        item_list = list(dict.fromkeys(item_list))

        return item_list

    menu_name = request.path.split('/')[2]
    items = MenuItem.objects.filter(name=menu_name).select_related('parent')
    if not items:
        return HttpResponseNotFound(f"<h1>404 Not Found!</h1>\n<h2>`{menu_name}` Doesn't exist</h2>")

    active_item = find_active_child(request.path, items)
    if not active_item:
        return render(request, 'treemenus/menu.html', {
            'menu_items': [item for item in items if not item.parent],
            'active_item': active_item,
            'menu_name': items[0].name,
            'menu_url': '/'.join(request.path.split('/')[:3]),
            })

    menu_items = create_hierarchy(items, active_item)[::-1]

    return render(request, 'treemenus/menu.html', {
        'menu_items': menu_items,
        'active_item': active_item,
        'menu_name': items[0].name,
        'menu_url': '/'.join(request.path.split('/')[:3]),
        })

from django.template import Library

from treemenus.models import MenuItem

register = Library()

@register.inclusion_tag('templatetags/menu_template.html', takes_context=True)
def draw_menu(context, menu_name):
    def find_active_child(path, menu_items):
        for item in menu_items:
            if path == item.url:
                return item
        return None
    
    def create_hierarchy(menu_items, active_item):
        item_list = []

        if active_item.children:
            item_list.extend(active_item.children.all())

        item_list.append(active_item)

        if active_item.parent:
            item_list.extend(create_hierarchy(menu_items=menu_items, active_item=active_item.parent))

        else:
            item_list.extend([item for item in menu_items if not item.parent])

        item_list = list(dict.fromkeys(item_list))

        return item_list

    menu_items = {}

    path = context['request'].path
    items = MenuItem.objects.filter(menu__name=menu_name).prefetch_related('children')
    if not items:
        return {'menu_items': menu_items}

    active_item = find_active_child(path, items)
    if not active_item:
        return {
            'menu_items': [item for item in items if not item.parent],
            'active_item': active_item,
            'menu': items[0].menu,
            }

    menu_items = create_hierarchy(items, active_item)[::-1]
    return {
        'menu_items': menu_items,
        'active_item': active_item,
        'menu': items[0].menu,
        }

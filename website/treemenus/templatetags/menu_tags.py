from django.template import Library

from treemenus.models import MenuItem

register = Library()

@register.inclusion_tag('templatetags/menu_template.html', takes_context=True)
def draw_menu(context, menu_name):
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

    menu_items = {}

    path = context['request'].path
    items = MenuItem.objects.filter(name=menu_name).select_related('parent')
    if not items:
        return {'menu_items': menu_items}

    active_item = find_active_child(path, items)
    if not active_item:
        return {
            'menu_items': [item for item in items if not item.parent],
            'active_item': active_item,
            'menu_name': items[0].name,
            'menu_url': '/'.join(items[0].url.split('/')[:3]),
            }

    menu_items = create_hierarchy(items, active_item)[::-1]

    return {
        'menu_items': menu_items,
        'active_item': active_item,
        'menu_name': items[0].name,
        'menu_url': '/'.join(items[0].url.split('/')[:3]),
        }

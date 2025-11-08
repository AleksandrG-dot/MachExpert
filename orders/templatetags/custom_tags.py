from django import template

register = template.Library()


@register.filter(name="has_group")
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@register.filter(name="group_convert")
def group_convert(group):
    if group == "directors":
        answer = "Директора"
    elif group == "manager":
        answer = "Менеджеры"
    elif group == "process_engineer":
        answer = "Технологи"
    elif group == "plan_disp_department":
        answer = "Диспетчера"
    elif group == "supply_service":
        answer = "Снабжение"
    elif group == "hr_department":
        answer = "Отдел кадров"
    else:
        answer = "Не изв. гр."
    return answer

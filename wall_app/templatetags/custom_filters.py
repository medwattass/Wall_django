from django import template

register = template.Library()

@register.filter
def time_diff_minutes(value, current_time):
    time_difference = current_time - value
    return time_difference.total_seconds() // 60
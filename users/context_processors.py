

from users.forms import WidgetLoginForm



def widget_register_form(request):
    
    form = WidgetLoginForm()
    return {'widget_form' : form}

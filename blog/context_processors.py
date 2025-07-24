from .forms import SubscriberForm



def newsletter_form_processor(request):
    return {'newsletter_form': SubscriberForm()}
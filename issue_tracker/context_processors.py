from issue_tracker.forms import SimpleSearchForm


def search_form(request):
    return {'search_form': SimpleSearchForm(request.GET)}

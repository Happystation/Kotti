import warnings

from pyramid.exceptions import NotFound
from pyramid.view import render_view_to_response

from kotti.resources import IContent
from kotti.resources import Document

from kotti.views.util import search_content


def view_content_default(context, request):
    """This view is always registered as the default view for any Content.

    Its job is to delegate to a view of which the name may be defined
    per instance.  If a instance level view is not defined for
    'context' (in 'context.defaultview'), we will fall back to a view
    with the name 'view'.

    The session variable 'current_view' can be set by other views. This way
    it is possible to get back to this view. Currently this is used by the
    'contents' view. If this view is called we get back to the normal behavior
    to get the 'default' view view itself.
    """
    if 'current_view' in request.session:
        del request.session['current_view']
    view_name = context.default_view or 'view'
    response = render_view_to_response(context, request, name=view_name)
    if response is None:  # pragma: no coverage
        warnings.warn("Failed to look up default view called %r for %r" %
                      (view_name, context))
        raise NotFound()
    return response


def view_node(context, request):  # pragma: no coverage
    return {}  # BBB


def search_results(context, request):
    results = []
    if u'search-term' in request.POST:
        search_term = request.POST[u'search-term']
        results = search_content(search_term, request)
    return {'results': results}


def includeme(config):
    config.add_view('kotti.views.view.view_content_default', context=IContent)

    config.add_view(
        context=Document,
        name='view',
        permission='view',
        renderer='kotti:templates/view/document.pt',
        )

    config.add_view(
        context=IContent,
        name='folder_view',
        permission='view',
        renderer='kotti:templates/view/folder.pt',
        )

    config.add_view(
        name='search',
        permission='view',
        renderer='kotti:templates/view/search.pt',
        )

    config.add_view(
        search_results,
        name='search-results',
        permission='view',
        renderer='kotti:templates/view/search-results.pt',
        )

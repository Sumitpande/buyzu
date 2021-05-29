# from django.views.generic import DetailView, ListView, TemplateView, RedirectView, View
# from haystack.views import SearchView
# from haystack.forms import SearchForm
# from haystack.query import SearchQuerySet, AutoQuery
# from haystack.utils import Highlighter
# from django.db.models import Q
# # from biostar.const import STOPWORDS

# from django.conf import settings
# from biostar.server.views import BaseListMixin
# from biostar.server.ajax import ajax_error, ajax_success, ajax_error_wrapper, json_response, access_control_allow_origin
# from django.contrib.flatpages.sitemaps import FlatPageSitemap
# from django.contrib.sitemaps import GenericSitemap
# from biostar.apps.posts.models import Post, Tag
# import logging

# logger = logging.getLogger(__name__)

# info_dict = {
#     'queryset': Post.objects.all(),
# }

# sitemaps = {
#     'flatpages': FlatPageSitemap,
#     'posts': GenericSitemap(info_dict, priority=0.6),
# }


# class SiteSearch(SearchView):
#     extra_context = lambda x: dict(topic="search", page_title="Search")


# def slow_highlight(query, text):
#     "Invoked only if the search backend does not support highlighting"
#     highlight = Highlighter(query)
#     value = highlight.highlight(text)
#     return value


# def join_highlights(row):
#     "Joins the highlighted text"
#     if type(row.highlighted) is dict:
#         return ''

#     # Unable to highlight by the back end
#     if not row.highlighted:
#         return ''

#     return '<br>'.join(x for x in row.highlighted)


# class Search(BaseListMixin):
#     template_name = "search/search.html"
#     paginate_by = settings.PAGINATE_BY
#     context_object_name = "results"
#     page_title = "Search"

#     def get_queryset(self):
#         self.q = self.request.GET.get('q', '')

#         if not self.q:
#             return []

#         #content = AutoQuery(self.q)
#         #query = SearchQuerySet().filter(content=content).highlight()[:50]
#         #for row in query:
#         #    context = join_highlights(row)
#         #    context = context or slow_highlight(query=self.q, text=row.content)
#         #    row.context = context
#         #return query
#         return []

#     def get_context_data(self, **kwargs):
#         context = super(Search, self).get_context_data(**kwargs)
#         context['q'] = self.q
#         return context


# def suggest_tags(request):
#     "Returns suggested tags"
#     q = request.GET.get('q', None)
#     if q:
#         tags = Tag.objects.filter(name__icontains = q).order_by('-count')[:10]
#     else:
#         tags = Tag.objects.all().order_by('-count')[:10]

#     data = [t.name for t in tags]
#     data = list(filter(None, data))

#     return json_response(data)

# @access_control_allow_origin
# def suggest_similar_posts(request):
#     "Returns similar post titles"
#     data = []
#     q = request.GET.get('q', None)
#     if q:
#         q = q.lower().split()
#         keywords = [word for word in q if not word in STOPWORDS]
#         keywords = [word for word in keywords if len(word)>2]
#         if len(keywords) > 0:
#             p = Q()
#             for keyword in keywords:
#                 p |= Q(title__icontains = keyword)
#             posts = Post.objects.filter(p,type=Post.QUESTION)[:10]
#             data = [str(post.id) + " - " + str(post.title) for post in posts]
#     return json_response(data)


# #@ajax_error_wrapper
# def search_title(request):
#     "Handles title searches"
#     q = request.GET.get('q', '')

#     content = AutoQuery(q)
#     results = SearchQuerySet().filter(content=content).highlight()[:50]

#     items = []
#     for row in results:
#         try:
#             ob = row.object

#             # Why can this happen?
#             if not ob:
#                 continue
#             context = join_highlights(row)
#             context = context or slow_highlight(query=q, text=row.content)
#             text = "%s" % row.title
#             items.append(
#                 dict(id=ob.get_absolute_url(), text=text, context=context, author=row.author,
#                      url=ob.get_absolute_url()),
#             )
#         except Exception as exc:
#             logger.error(content)
#             logger.error(exc)
#             pass

#     payload = dict(items=items)
#     return json_response(payload)
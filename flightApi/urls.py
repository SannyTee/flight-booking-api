"""implement API urls here."""
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from flightApi.views import user_auth, api_status, flights, admin_ops

# pylint: disable=invalid-name
welcome_message = api_status.ApiStatusViewSet.as_view({
    'get': 'retrieve'
})

user_signup = user_auth.UserAuthViewSet.as_view({
    'post': 'create',
})

user_login = user_auth.UserAuthViewSet.as_view({
    'post': 'login'
})

user_flights = flights.FlightViewset.as_view({
    'post': 'create'
})

admin_flights = admin_ops.AdminOpsViewSet.as_view({
    'get': 'retrieve_flight_booking'
})

urlpatterns = format_suffix_patterns([
    url(r'^$', welcome_message, name='welcome_message'),
    url(r'^api/v1/auth/signup/$', user_signup, name='user_signup'),
    url(r'^api/v1/auth/login/$', user_login, name='user_login'),
    url(r'^api/v1/flights/$', user_flights, name='user_flights'),
    url(r'^api/v1/admin/flights/$', admin_flights, name='admin_flights')
])

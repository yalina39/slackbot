import pytest
from django import urls
from django.contrib.auth import get_user_model


#def setup_module(module):
    #event_hook = reverse('event-hook')

@pytest.mark.parametrize('param', [('event_hook')])
def test_render_views(client, param):
    url = urls.reverse(param)
    resp = client.get(url)
    assert resp.status_code == 200


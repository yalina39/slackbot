import pytest

from actions.models import Message


@pytest.mark.django_db
def test_message_create():
    message = Message.objects.create(channel = "C036XB9U8P5", user = "U036QL3HWNS", text = "Hello, this is my card number - 2720822463109651", pattern="mastercard")
    assert message.channel == "C036XB9U8P5"
    assert message.user == "U036QL3HWNS"
    assert message.text == "Hello, this is my card number - 2720822463109651"
    assert message.pattern == "mastercard"
    assert str(message) == message.pattern

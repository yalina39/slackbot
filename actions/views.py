from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json
from django.http import HttpResponse, JsonResponse
import slack
from django.views.generic import ListView
from .models import Message
import re

def isValidMasterCardNo(string):

    regex = "^(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}$"
    p = re.compile(regex)
    if re.search(p, string):
        return True
    else:
        return False
        
def isValidVisaCardNo(string):

    regex = "^4[0-9]{12}(?:[0-9]{3})?$"
    p = re.compile(regex)    
    if re.match(p, string) is None:
        return False
    else:
        return True


@csrf_exempt
def event_hook(request):
    client = slack.WebClient(token=settings.BOT_USER_ACCESS_TOKEN)
    json_dict = json.loads(request.body.decode('utf-8'))    

    if json_dict['token'] != settings.VERIFICATION_TOKEN:
        return HttpResponse(status=403)    

    if 'type' in json_dict:
        if json_dict['type'] == 'url_verification':
            response_dict = {"challenge": json_dict['challenge']}
            return JsonResponse(response_dict, safe=False)
    
    if 'event' in json_dict:
        event_msg = json_dict['event']
        if ('subtype' in event_msg) and (event_msg['subtype'] == 'bot_message'):
            return HttpResponse(status=200)

    if event_msg['type'] == 'message':
        msg_txt = event_msg['text']
        word_list = msg_txt.split()
        num_list = [num for num in filter(lambda num: num.isnumeric(), word_list)]
        if num_list == []:
            return HttpResponse(status=200)
        else:
            for i in range(len(num_list)):
                if isValidMasterCardNo(num_list[i]) == True:
                    Message.objects.create(user = event_msg['user'], channel = event_msg['channel'], text = event_msg['text'], pattern = 'mastercard')
                    return HttpResponse(status=200)
                elif isValidVisaCardNo(num_list[i]) == True:
                    Message.objects.create(user = event_msg['user'], channel = event_msg['channel'], text = event_msg['text'], pattern = 'visa')
                    return HttpResponse(status=200)
                else:
                    return HttpResponse(status=200)
    return HttpResponse(status=200)






from django.views.generic import View

class RetrieveUserInfo(View):
    def retrieve_all_info(self, request):
        print(request.body)
        # Mock user
        response['display_name'] = "BobRoss"
        response['avatar'] = "https://cdn.britannica.com/03/193803-050-CBC590FA/Bob-Ross.jpg"
        response['friends'] = []
        response['online'] = True
        response['stats'] = stats
        return HttpResponse(json.dumps(response), content_type='application/json')

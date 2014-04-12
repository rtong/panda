from django.contrib import admin
from events.models import Event

class EventAdmin(admin.ModelAdmin):
    list_display=('event_id','name','description','start_time',
		  'end_time','location','latitude','longitude',
	          'venue_id')

admin.site.register(Event,EventAdmin)



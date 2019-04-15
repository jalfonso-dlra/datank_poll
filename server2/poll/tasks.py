from celery.decorators import task
from .models import Poll, Option, Vote

# This is the decorator which a celery worker uses
@task(name="create_poll")
def create_poll(data):
    poll = Poll(title=data.get('title'))
    poll.save()
    for option in data.get('options'):
        option_obj = Option(name=option, poll=poll)
        option_obj.save()
    return True


@task(name="create_vote")
def create_vote(data):
    vote = Vote(poll_option_id=data.get('option_id'))
    vote.save()
    return True

from celery.decorators import task

# This is the decorator which a celery worker uses
@task(name="create_poll")
def create_poll(poll):
    return True


@task(name="create_vote")
def create_vote(vote):
    return True

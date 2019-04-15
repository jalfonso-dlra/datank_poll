from rest_framework import serializers
from .models import Poll

from datetime import timedelta
from django.utils import timezone


class OptionVoteCountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    count = serializers.SerializerMethodField()

    def get_count(self, obj):

        option_votes = obj.option_vote.all()
        if self.context.get('hourly'):
            min_date = timezone.now() - timedelta(hours=1)
            option_votes = option_votes.filter(date_created__gte=min_date)
        return option_votes.count()


class PollCountGlobalSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    title = serializers.CharField()
    options = serializers.SerializerMethodField()

    def get_options(self, obj):
        return OptionVoteCountSerializer(obj.poll_option.all(), many=True,
                                         context={'hourly': self.context.get('hourly')}).data


class PollRetrieveSerializer(serializers.Serializer):
    poll_id = serializers.IntegerField()
    hourly = serializers.BooleanField(required=False)

    def validate_poll_id(self, value):
        poll = Poll.objects.filter(pk=value).first()
        if not poll:
            raise serializers.ValidationError('poll_id not exist')
        return value

    def retrieve(self):
        poll = Poll.objects.filter(pk=self.validated_data.get('poll_id')).first()
        return PollCountGlobalSerializer(poll, context={'hourly': self.validated_data.get('hourly')}).data

from rest_framework import serializers
from .tasks import create_poll, create_vote
from .models import Poll, Option, Vote

class OptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Option
        fields = '__all__'


class PollSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()

    def get_options(self, obj):
        return OptionSerializer(obj.poll_option.all(), many=True).data

    class Meta:
        model = Poll
        fields = '__all__'


class PollCreateSerializer(serializers.Serializer):
    title = serializers.CharField()
    options = serializers.ListField(child=serializers.CharField(), min_length=2)

    def create(self,):
        poll = Poll(title=self.validated_data.get('title'))
        poll.save()
        for option in self.validated_data.get('options'):
            option_obj = Option(name=option, poll=poll)
            option_obj.save()
        create_poll.delay(self.validated_data)
        return PollSerializer(poll).data


class VoteCreateSerializer(serializers.Serializer):
    poll_id = serializers.IntegerField()
    option_id = serializers.IntegerField()

    def validate(self, data):
        errors = dict()
        poll = Poll.objects.filter(pk=data.get('poll_id')).first()
        if poll:
            option = poll.poll_option.filter(pk=data.get('option_id')).first()
            if not option:
                errors['option_id'] = 'option_id not exist'
        else:
            errors['poll_id'] = 'poll_id not exist'
        if errors:
            raise serializers.ValidationError(errors)
        return data

    def vote(self):
        vote = Vote(poll_option_id=self.validated_data.get('option_id'))
        vote.save()
        create_vote.delay(self.validated_data)
        return {'status': True}

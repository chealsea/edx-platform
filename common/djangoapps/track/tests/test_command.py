from StringIO import StringIO
# from django.core.management import call_command
from django.test import TestCase
from track.command import TrackedCommand
#from mock import sentinel
#from track.views import server_track
import json
from eventtracking import tracker as eventtracker

class CommandsTestBase(TestCase):
    # create a command here?  And then test that it performs tracking?
    # Then I'm not sure it belongs in util. This is pretty standalone. 
    # Put it into commands (and test_commands.py)?

#    def call_command(self, name, *args, **kwargs):
#        """Call management command and return output"""
#        out = StringIO()  # To Capture the output of the command
#        call_command(name, *args, stdout=out, **kwargs)
#        out.seek(0)
#        return out.read()

    class DummyCommand(TrackedCommand):
        def handle(self, *args, **options):
            # print "This is a test.  Got options: " + str(options)
#            request = None
#            server_track(request, str(sentinel.event_type), '{}')
#            return "This is another test.  Got options: " + str(options)
            return json.dumps(eventtracker.get_tracker().resolve_context())

    def _run_dummy_command(self, *args, **kwargs):
        out = StringIO()  # To Capture the output of the command
        self.DummyCommand().execute(*args, stdout=out, **kwargs)
        out.seek(0)
        return json.loads(out.read())

    def test_command(self):
        args = ['whee']
        kwargs = {'key1': 'default', 'key2': True}
        json_out = self._run_dummy_command(*args, **kwargs)
        self.assertEquals(json_out['command'], 'unknown')
        self.assertEquals(json_out['command_args'], args)
        self.assertEquals(json_out['command_options'], kwargs)

    def test_password_in_command(self):
        args = []
        kwargs = {'password': 'default'}
        json_out = self._run_dummy_command(*args, **kwargs)
        self.assertEquals(json_out['command'], 'unknown')
        self.assertEquals(json_out['command_args'], args)
        self.assertEquals(json_out['command_options'], {'password': '********'})

    def test_removed_args_in_command(self):
        args = []
        kwargs = {'settings': 'dummy', 'pythonpath': 'whee'}
        json_out = self._run_dummy_command(*args, **kwargs)
        self.assertEquals(json_out['command'], 'unknown')
        self.assertEquals(json_out['command_args'], args)
        self.assertEquals(json_out['command_options'], {})

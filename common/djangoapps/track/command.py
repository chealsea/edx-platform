from django.core.management.base import BaseCommand

from eventtracking import tracker


class TrackedCommand(BaseCommand):
    """Provides management command calling info to tracking context."""
    prog_name = 'unknown'

    def create_parser(self, prog_name, subcommand):
        """Overrides create_parser to snag command line."""
        self.prog_name = "{} {}".format(prog_name, subcommand)
        return super(TrackedCommand, self).create_parser(prog_name, subcommand)

    def execute(self, *args, **options):
        """Overrides execute to add command line to tracking context."""
        # Make a copy of options, and obfuscate (obliterate) particular values.
        options_dict = dict(options)

        censored_opts = ['password']
        for opt in censored_opts:
            if opt in options_dict:
                options_dict[opt] = '*' * 8

        removed_opts = ['settings', 'pythonpath', 'stdout', 'stderr']
        for opt in removed_opts:
            if opt in options_dict:
                del options_dict[opt]

        context = {
            'command': self.prog_name,
            'command_args': args,
            'command_options': options_dict,
        }
        COMMAND_CONTEXT_NAME = 'edx.mgmt.command'
        with tracker.get_tracker().context(COMMAND_CONTEXT_NAME, context):
            super(TrackedCommand, self).execute(*args, **options)

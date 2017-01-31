from functools import partial

import click

warn = partial(click.secho, fg='yellow')
success = partial(click.secho, fg='green')
error = partial(click.secho, fg='red')
log = click.echo

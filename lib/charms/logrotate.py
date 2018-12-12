import sys
import os
import json

from typing import Any, Dict

from jinja2 import Template

from charmhelpers.core.hookenv import (
    config, relation_get, in_relation_hook, charm_dir)


def juju_header() -> str:
    """
    Place holder for output file
    header.

    :return: String
    """
    return (
        '#-------------------------------------------------#\n'
        '# This file is Juju managed - do not edit by hand #\n'
        '#-------------------------------------------------#\n'
    )


def render_template(
    template: str, destination: str, context: Dict[str, Any]) -> None:
    """
    Render the configuration file template.

    :param template: String template name
    :param destination: String path to write template
    :param context: Dictionary context to render
    """
    template_file = os.path.join(charm_dir(), 'templates', template)
    with open(template_file) as f:
        template_object = Template(f.read())

    with open(destination, 'w') as f:
        f.write(juju_header())
        f.write(template_object.render(context))
    os.chmod(destination, 0o444)


class Configuration:
    compression_extensions = {'gzip': '.gz', 'bzip2': '.bz2', 'xz': '.xz'}

    def app_name(self):
        return str(config('application_name'))

    def compress(self, logname):
        return self.get_config(logname, 'compress')

    def compresscmd(self, logname):
        return self.get_config(logname, 'compresscmd')

    def compressext(self, logname):
        if self.compresscmd(logname) in self.compression_extensions:
            ext = self.compression_extensions[self.compresscmd(logname)]
        else:
            ext = ''
        return self.get_config(logname, 'compressext', ext)

    def dateext(self, logname):
        return self.get_config(logname, 'dateext')

    def path(self, logname):
        return str(self.logfile(logname)['path'])

    def get_config(self, logname, what, default=''):
        if what in self.logfile(logname):
            return str(self.logfile(logname)[what])
        elif config(what):
            return config(what)
        else:
            return default

    def group(self, logname):
        return self.get_config(logname, 'group')

    def logfile(self, logname):
        l = self.logfiles()[logname]
        return l

    def logfiles(self):
        if config('logfiles'):
            from_config = json.loads(str(config('logfiles')))
        else:
            from_config = {}
        if in_relation_hook():
            try:
                from_relation = json.loads(str(relation_get('logfiles')))
            except ValueError:
                from_relation = {}
        else:
            from_relation = {}  # Local config overrides relation config

        return dict(
            [x for x in from_relation.items()] + \
            [x for x in from_config.items()]
        )

    def owner(self, logname):
        return self.get_config(logname, 'owner')

    def period(self, logname):
        return self.get_config(logname, 'period')

    def perms(self, logname):
        return self.get_config(logname, 'perms')

    def postrotate(self, logname):
        return self.get_config(logname, 'postrotate')

    def prerotate(self, logname):
        return self.get_config(logname, 'prerotate')

    def when(self, logname):
        return self.get_config(logname, 'when')

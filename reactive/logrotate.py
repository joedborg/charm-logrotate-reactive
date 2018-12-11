import os

from charms.logrotate import Configuration, render_template
from charms.reactive import when, when_not, set_flag

from charmhelpers.core.hookenv import status_set, log


conf = Configuration()


@when('apt.installed.logrotate')
@when('apt.installed.gzip')
@when('apt.installed.bzip2')
@when('apt.installed.xz-utils')
@when_not('logrotate.installed')
def install_logrotate() -> None:
    """
    Triggerd after all of the 
    required packages are installed.

    :return: None
    """
    status_set('active', 'Logrotate is ready.')
    set_flag('logrotate.installed')

@when('logrotate.installed')
@when('config.changed')
def configure_logrotate() -> None:
    """
    Apply logrotate configuration.

    :return: None
    """
    status_set('maintenance', 'Applying configuration.')
    for logname in conf.logfiles():
        log('Adding logrotate entry for {}'.format(logname))
        tmpl_data = {}
        tmpl_data['path'] = conf.path(logname)
        tmpl_data['when'] = conf.when(logname)
        tmpl_data['compress'] = conf.compress(logname)
        tmpl_data['compresscmd'] = conf.compresscmd(logname)
        tmpl_data['compressext'] = conf.compressext(logname)
        tmpl_data['dateext'] = conf.dateext(logname)
        tmpl_data['period'] = conf.period(logname)
        tmpl_data['perms'] = conf.perms(logname)
        tmpl_data['owner'] = conf.owner(logname)
        tmpl_data['group'] = conf.group(logname)
        tmpl_data['prerotate'] = conf.prerotate(logname)
        tmpl_data['postrotate'] = conf.postrotate(logname)
        logrotate_path = '/etc/logrotate.d/{}'.format(logname)
        render_template('logrotate.tmpl', logrotate_path, tmpl_data)
        os.chmod(logrotate_path, 0o444)
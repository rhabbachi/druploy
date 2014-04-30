# vim: set syntax=python ts=4 sw=4 expandtab:
import os
from os.path import join
from fabric.api import *
from fabric.utils import *
from fabric.colors import *
from fabric.context_managers import *
from fabric.contrib.files import *
from druploy.exceptions import *
from druploy.utils import Utils

class Domain(object):

    @staticmethod
    def list():
        pass

    def __init__(self, deployment, name, aliases=[], username=None, password=None):
        self.deployment = deployment
        self.server = self.deployment.server
        self.aliases = aliases
        self.name = name
        self.full_name = "{0}.{1}.{2}".format(self.deployment.project.name, self.deployment.name, self.name)
        self.domain_path = join(self.deployment.path.domain, self.name)
        self.username = username
        self.password = password
        self.htpasswd_path = join(self.deployment.path.domain, self.name + ".htpasswd")

    def create(self):
        with settings(**self.server.settings()):
            require = None
            if self.username is None or self.password is None:
                Utils.notice("Username or password missing, discarding password protection.")
            else:
                # Site will be password protected
                # Create password file
                self.htpasswd()
                require = "valid-user"
            context = {
                "name": self.name,
                "full_name": self.full_name,
                "aliases": self.aliases,
                "document_root": self.deployment.drupal_site.path,
                "auth_type": "Basic",
                "auth_name": "Authentication Required",
                "auth_user_file": self.htpasswd_path,
                "require": require
            }
            upload_template('vhost.conf', self.domain_path, context,
                            use_jinja=True,
                            template_dir=env.template_dir,
                            backup=False,
                            mode=0644)
            self.server.symlink(self.domain_path, join('/etc/apache2/sites-available', self.full_name), force=True, sudo=True)

    def delete(self):
        pass

    def enable(self):
        self.server.sudo("a2ensite {0}".format(self.full_name))
        self.server.sudo("service apache2 reload")

    def disable(self):
        self.server.sudo("a2dissite {0}".format(self.full_name))
        self.server.sudo("service apache2 reload")

    def htpasswd(self):
        Utils.notice("Generating htpasswd file...")
        self.server.sudo_or_run("htpasswd -bc " + self.htpasswd_path
                        + " " + self.username
                        + " " + self.password)

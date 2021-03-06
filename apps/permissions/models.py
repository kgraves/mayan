from __future__ import unicode_literals

import logging

from django.contrib.auth.models import Group
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from .managers import RoleManager, StoredPermissionManager

logger = logging.getLogger(__name__)


@python_2_unicode_compatible
class StoredPermission(models.Model):
    namespace = models.CharField(max_length=64, verbose_name=_('Namespace'))
    name = models.CharField(max_length=64, verbose_name=_('Name'))

    objects = StoredPermissionManager()

    def __init__(self, *args, **kwargs):
        from .classes import Permission

        super(StoredPermission, self).__init__(*args, **kwargs)
        try:
            self.volatile_permission = Permission.get(
                {'pk': '%s.%s' % (self.namespace, self.name)},
                proxy_only=True
            )
        except KeyError:
            # Must be a deprecated permission in the database that is no
            # longer used in the current code
            pass

    def __str__(self):
        return unicode(getattr(self, 'volatile_permission', self.name))

    def natural_key(self):
        return (self.namespace, self.name)

    class Meta:
        ordering = ('namespace',)
        unique_together = ('namespace', 'name')
        verbose_name = _('Permission')
        verbose_name_plural = _('Permissions')

    def requester_has_this(self, user):
        logger.debug('user: %s', user)
        if user.is_superuser or user.is_staff:
            return True

        # Request is one of the permission's holders?
        for group in user.groups.all():
            for role in group.roles.all():
                if self in role.permissions.all():
                    return True

        logger.debug('Fallthru')
        return False


@python_2_unicode_compatible
class Role(models.Model):
    label = models.CharField(
        max_length=64, unique=True, verbose_name=_('Label')
    )
    permissions = models.ManyToManyField(
        StoredPermission, related_name='roles', verbose_name=_('Permissions')
    )
    groups = models.ManyToManyField(
        Group, related_name='roles', verbose_name=_('Groups')
    )

    objects = RoleManager()

    def __str__(self):
        return self.label

    def get_absolute_url(self):
        return reverse('permissions:role_list')

    def natural_key(self):
        return (self.label,)
    natural_key.dependencies = ['auth.Group', 'permissions.StoredPermission']

    class Meta:
        ordering = ('label',)
        verbose_name = _('Role')
        verbose_name_plural = _('Roles')

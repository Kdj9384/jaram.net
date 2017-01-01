import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from main.models import Member


class EventGroup(models.Model):
    title = models.CharField(_('행사 그룹'), max_length=255, null=False, blank=False)
    color = models.CharField(_('그룹 색'), max_length=255, null=False, blank=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']
        verbose_name = _('행사 그룹')
        verbose_name_plural = _('행사 그룹')


class Event(models.Model):
    writer = models.ForeignKey(Member)
    category = models.ForeignKey(EventGroup)
    start_date = models.DateTimeField(_('시작 날짜'), null=False, blank=False, default=datetime.datetime.now)
    end_date = models.DateTimeField(_('종료 날짜'), null=False, blank=False,
                                    default=datetime.datetime.now() + datetime.timedelta(hours=1))
    title = models.CharField(_('제목'), max_length=255, null=False, blank=False)
    description = models.TextField(_('내용'), null=False, blank=False)
    all_day = models.BooleanField(_('하루종일'), default=False)
    link_page = models.CharField(_('연결 페이지'), max_length=255, null=True, blank=True, default='')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-start_date']
        verbose_name = _('행사')
        verbose_name_plural = _('행사')
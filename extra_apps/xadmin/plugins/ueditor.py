# -*- coding: utf-8 -*-
# author = minjie
from django.conf import settings
from django.db.models import TextField

import xadmin
from xadmin.views import BaseAdminPlugin, CreateAdminView, UpdateAdminView, ModelFormAdminView
from DjangoUeditor.models import UEditorField
from DjangoUeditor.widgets import UEditorWidget


class XadminUEditorWidget(UEditorWidget):
    def __init__(self, **kwargs):
        self.ueditor_options = kwargs
        self.Media.js = None
        super(XadminUEditorWidget, self).__init__(kwargs)


class UEditorPlugin(BaseAdminPlugin):
    # 识别样式style_fields
    def get_field_style(self, attrs, db_field, style, **kwargs):
        if style == 'ueditor':
            if isinstance(db_field, UEditorField):
                # 固定写法
                widget = db_field.formfield().widget
                param = {}
                param.update(widget.ueditor_settings)
                param.update(widget.attrs)
                return {'widget': XadminUEditorWidget(**param)}
        return attrs

    def block_extrahead(self, context, nodes):
        js = '<script type="text/javascript" src="%s"></script>' % (settings.STATIC_URL + "ueditor/ueditor.config.js")
        js += '<script type="text/javascript" src="%s"></script>' % (settings.STATIC_URL + "ueditor/ueditor.all.min.js")
        nodes.append(js)


xadmin.site.register_plugin(UEditorPlugin, CreateAdminView)
xadmin.site.register_plugin(UEditorPlugin, UpdateAdminView)


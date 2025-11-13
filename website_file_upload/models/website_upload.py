# -*- coding: utf-8 -*-
import base64
import binascii
import mimetypes

from odoo import api, fields, models


class WebsiteUpload(models.Model):
    _name = "website.upload"
    _description = "Website Upload"

    name = fields.Char(required=True, string="Nome")
    data = fields.Binary(string="Arquivo", required=True, attachment=False)
    filename = fields.Char(string="Nome do Arquivo")
    mimetype = fields.Char(string="Tipo MIME")
    file_size = fields.Integer(string="Tamanho (bytes)", readonly=True)
    description = fields.Text(string="Descrição")
    active = fields.Boolean(default=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            self._update_metadata(vals)
        return super().create(vals_list)

    def write(self, vals):
        self._update_metadata(vals)
        return super().write(vals)

    @staticmethod
    def _update_metadata(vals):
        data = vals.get("data")
        if data:
            if isinstance(data, str):
                data = data.encode()
            try:
                raw = base64.b64decode(data)
            except binascii.Error:
                raw = b""
            vals["file_size"] = len(raw)
        filename = vals.get("filename")
        if filename and not vals.get("mimetype"):
            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype:
                vals["mimetype"] = mimetype

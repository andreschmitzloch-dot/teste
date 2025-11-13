# -*- coding: utf-8 -*-
import base64

from odoo import http, _
from odoo.http import request

MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "application/pdf",
    "text/plain",
}


class WebsiteUploadController(http.Controller):
    @http.route(
        "/website/file/upload",
        type="http",
        auth="public",
        website=True,
        csrf=True,
        methods=["GET", "POST"],
    )
    def upload_file(self, **post):
        values = {
            "success": False,
            "error": False,
            "max_file_size_mb": MAX_FILE_SIZE // (1024 * 1024),
            "allowed_mimetypes": ", ".join(sorted(ALLOWED_MIME_TYPES)) or _("Qualquer"),
        }
        if request.httprequest.method == "POST":
            uploaded_file = request.httprequest.files.get("upload_file")
            name = post.get("name") or (uploaded_file.filename if uploaded_file else False)
            description = post.get("description")

            if not uploaded_file or uploaded_file.filename == "":
                values["error"] = _("Nenhum arquivo foi selecionado.")
                return request.render("website_file_upload.upload_form", values)

            file_content = uploaded_file.read()
            if not file_content:
                values["error"] = _("O arquivo enviado está vazio.")
                return request.render("website_file_upload.upload_form", values)

            if len(file_content) > MAX_FILE_SIZE:
                values["error"] = _(
                    "O arquivo excede o limite de %s MB." % (MAX_FILE_SIZE // (1024 * 1024))
                )
                return request.render("website_file_upload.upload_form", values)

            mimetype = uploaded_file.mimetype
            if ALLOWED_MIME_TYPES and mimetype not in ALLOWED_MIME_TYPES:
                values["error"] = _(
                    "Tipo de arquivo não permitido: %s" % (mimetype or _("desconhecido"))
                )
                return request.render("website_file_upload.upload_form", values)

            encoded_data = base64.b64encode(file_content)
            request.env["website.upload"].sudo().create(
                {
                    "name": name or uploaded_file.filename,
                    "data": encoded_data,
                    "filename": uploaded_file.filename,
                    "mimetype": mimetype,
                    "description": description,
                }
            )
            values["success"] = _("Arquivo enviado com sucesso!")
        return request.render("website_file_upload.upload_form", values)

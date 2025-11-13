=====================
Website File Upload
=====================

Este módulo adiciona um formulário público para upload de arquivos no website do Odoo, com validações básicas e uma interface backend para revisão.

Limites e validações
=====================

* **Tamanho máximo:** 5 MB por arquivo (configurado no controlador em ``MAX_FILE_SIZE``).
* **Tipos aceitos:** ``image/jpeg``, ``image/png``, ``application/pdf`` e ``text/plain`` (configurados em ``ALLOWED_MIME_TYPES``).
* **Limpeza:** recomenda-se criar um cron (``Settings > Technical > Automation > Scheduled Actions``) para remover arquivos expirados ou arquivados conforme a política da empresa. Caso utilize integrações com antivírus, configure uma varredura periódica sobre os binários armazenados.

Instalação e uso
================

1. Instale o módulo via Apps.
2. Acesse ``/website/file/upload`` para visualizar o formulário público.
3. Os arquivos enviados ficam disponíveis no menu **Website › Configuration › Uploads** para usuários internos autorizados.

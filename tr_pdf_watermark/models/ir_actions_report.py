import io
import logging

from PyPDF2 import PdfFileReader as PdfReader, PdfFileWriter as PdfWriter
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import Color
from reportlab.pdfgen import canvas

from odoo import models

_logger = logging.getLogger(__name__)

REPORT_MAP = {
    # Invoices
    'account.account_invoices': 'tr_watermark.invoice',
    'account.account_invoices_without_payment': 'tr_watermark.invoice',
    'account.report_invoice': 'tr_watermark.invoice',
    'account.report_invoice_with_payments': 'tr_watermark.invoice',
    'account_edi_ubl_cii.action_report_account_invoices_generated_by_odoo': 'tr_watermark.invoice',
    # Sale Orders
    'sale.action_report_saleorder': 'tr_watermark.sale',
    'sale.report_saleorder': 'tr_watermark.sale',
    'sale.action_report_pro_forma_invoice': 'tr_watermark.sale',
    # Purchase Orders
    'purchase.action_report_purchase_order': 'tr_watermark.purchase',
    'purchase.report_purchase_quotation': 'tr_watermark.purchase',
    'purchase.report_purchaseorder': 'tr_watermark.purchase',
    'purchase.report_purchasequotation': 'tr_watermark.purchase',
}

TEXT_MAP = {
    'tr_watermark.invoice': 'tr_watermark.invoice_text',
    'tr_watermark.sale': 'tr_watermark.sale_text',
    'tr_watermark.purchase': 'tr_watermark.purchase_text',
}


class IrActionsReport(models.Model):
    _inherit = 'ir.actions.report'

    def _get_watermark_config(self, report_name):
        get = self.env['ir.config_parameter'].sudo().get_param
        param_key = REPORT_MAP.get(report_name)
        if not param_key or not get(param_key):
            return None, None
        text = get(TEXT_MAP.get(param_key, ''), '') or 'CONFIDENTIAL'
        color = get('tr_watermark.color') or '#cccccc'
        return text, color

    def _make_watermark_pdf(self, text, color, width, height):
        """Generate a single-page PDF with the watermark text."""
        buf = io.BytesIO()
        c = canvas.Canvas(buf, pagesize=(width, height))

        # Parse color
        try:
            if color.startswith('#'):
                r = int(color[1:3], 16) / 255
                g = int(color[3:5], 16) / 255
                b = int(color[5:7], 16) / 255
                wm_color = Color(r, g, b, alpha=0.35)
            else:
                wm_color = Color(0.8, 0.8, 0.8, alpha=0.35)
        except Exception:
            wm_color = Color(0.8, 0.8, 0.8, alpha=0.35)

        c.saveState()
        c.setFillColor(wm_color)
        c.setFont('Helvetica-Bold', 80)
        c.translate(width / 2, height / 2)
        c.rotate(45)
        c.drawCentredString(0, 0, text)
        c.restoreState()
        c.save()
        buf.seek(0)
        return buf

    def _render_qweb_pdf(self, report_ref, res_ids=None, data=None):
        pdf_content, report_type = super()._render_qweb_pdf(
            report_ref, res_ids=res_ids, data=data)

        try:
            if isinstance(report_ref, str):
                report_name = report_ref
            else:
                report = self._get_report(report_ref)
                ext_ids = report.get_external_id()
                report_name = ext_ids.get(str(report.id), '') or report.report_name or ''

            _logger.info('PDF Watermark: checking report_name=%s', report_name)
            text, color = self._get_watermark_config(report_name)
            if not text:
                return pdf_content, report_type

            _logger.info('PDF Watermark: report=%s applying="%s"', report_name, text)

            reader = PdfReader(io.BytesIO(pdf_content))
            writer = PdfWriter()

            for i in range(reader.getNumPages()):
                page = reader.getPage(i)
                box = page.mediaBox
                w = float(box.getWidth())
                h = float(box.getHeight())
                wm_buf = self._make_watermark_pdf(text, color, w, h)
                wm_page = PdfReader(wm_buf).getPage(0)
                page.mergePage(wm_page)
                writer.addPage(page)

            out = io.BytesIO()
            writer.write(out)
            return out.getvalue(), report_type

        except Exception as e:
            _logger.error('TR PDF Watermark ERROR: %s', e, exc_info=True)
            return pdf_content, report_type

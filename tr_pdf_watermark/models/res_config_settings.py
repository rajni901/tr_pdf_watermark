from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    tr_wm_invoice = fields.Boolean(
        string='Invoices', config_parameter='tr_watermark.invoice')
    tr_wm_invoice_text = fields.Char(
        string='Invoice Watermark', config_parameter='tr_watermark.invoice_text')

    tr_wm_sale = fields.Boolean(
        string='Sale Orders', config_parameter='tr_watermark.sale')
    tr_wm_sale_text = fields.Char(
        string='Sale Order Watermark', config_parameter='tr_watermark.sale_text')

    tr_wm_purchase = fields.Boolean(
        string='Purchase Orders', config_parameter='tr_watermark.purchase')
    tr_wm_purchase_text = fields.Char(
        string='Purchase Order Watermark', config_parameter='tr_watermark.purchase_text')

    tr_wm_color = fields.Char(
        string='Watermark Color',
        config_parameter='tr_watermark.color',
        default='rgba(200,200,200,0.35)',
    )

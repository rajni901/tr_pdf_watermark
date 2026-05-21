{
    'name': 'PDF Watermark',
    'version': '19.0.1.0.0',
    'category': 'Technical',
    'summary': 'Add text watermarks to PDF reports — DRAFT, PAID, CONFIDENTIAL, CANCELLED or custom text. Works on Invoices, Sale Orders, Purchase Orders.',
    'description': """
PDF Watermark — by Technical Rajni
====================================
Add diagonal text watermarks to any Odoo PDF report.

Features:
- Pre-set watermarks: DRAFT, PAID, CONFIDENTIAL, CANCELLED, COPY
- Custom watermark text
- Apply to Invoices, Sale Orders, Purchase Orders
- Configure color and opacity
- No extra libraries required
- Configure from Settings in seconds
    """,
    'author': 'Technical Rajni',
    'website': 'https://www.technicalrajni.com',
    'license': 'OPL-1',
    'depends': ['web', 'account', 'sale_management', 'purchase'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'images': ['static/description/banner.png'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'price': 10.00,
    'currency': 'USD',
}

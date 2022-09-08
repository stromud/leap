{
    'name': 'Leap',
    'version': '14.1.0.2',
    'category': 'Agenzia immobiliare',
    'sequence': 15,
    'summary': 'vendite',
    'depends': [
        'base',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/leap_property_view.xml',
        'views/leap_property_offer_view.xml',
        'views/leap_property_type_view.xml',
        'views/leap_property_tag_view.xml',
        'views/leap_manu_view.xml',
        'views/res_users.xml',
        'report/leap_property_templates.xml',
        'report/leap_property_reports.xml',
        'data/leap.property.type.csv',
    ],
    'demo': [
        "data/demo_data.xml"
    ],
    'installable': True,
    'application': True,
} #allellllllllllllllllllllllllll
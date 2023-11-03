# -*- coding: utf-8 -*-


{
    'name': 'library',
    'version': '1',
    'sequence': -100,
    'summary': 'library ',
    'description': """ .""",
    'author': 'alaa samy',
    'company': 'alaasamy',
    'maintainer': ' ',
    'category': 'Sales',
    'website': 'www.alaa.com',
    'depends': ['base', 'mail'],
    'data': [
        'reports/report_templet.xml',
        'views/Borrows.xml',
        'views/Book_copies.xml',
        'views/Books_data.xml',
        'views/Book_Category.xml',
        'views/Publisher.xml',
        'views/Author.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

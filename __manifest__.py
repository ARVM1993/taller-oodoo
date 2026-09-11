{
    'name': 'Gestion taller',
    'version': '1.0',
    'category': 'Fabricacion/reparacion',
    'summary': 'Modulo gestion taller fabricacion y reparacion',
    'description': 'Modulo para gestionar maquinaria y sus reparaciones',
    'author': 'Aitor Ruiz-Valdepenas Martin',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/maquinaria.views.xml',
    ],
    'installable': True,
    'application': True
}
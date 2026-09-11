from odoo import fields, models

class TallerReparacion(models.Model):
    _name = 'taller.reparacion'
    _description = 'Gestion de Reparaciones'
    _rec_name = 'referencia'

    name = fields.Char(string='Descripcion', required=True)
    referencia = fields.Char(
        string='Numero de reparacion',
        required=True,
        default='REP-NUEVO'
    )
    maquina = fields.Many2one(
        'taller.maquinaria',
        string='Maquina',
        required=True
    )
    fecha_inicio = fields.Date(
        string='Fecha de inicio',
        default=fields.Date.today
    )
    fecha_fin = fields.Date(string='Fecha de fin')
    responsable = fields.Many2one(
        'res.users',
        string='Tecnico responsable',
        domain="[('groups_id.name', 'in', ['Taller'])]",
        help='Tecnico responsable (solo usuarios del grupo Taller)'
    )
    descripcion = fields.Text(string='Descripcion de la reparacion')
    costo = fields.Float(string='Costo', digits=(10, 2))
    estado = fields.Selection([
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En proceso'),
        ('terminada', 'Terminada'),
        ('entregada', 'Entregada')
    ], string='Estado', default='pendiente')
    notas = fields.Text(string='Notas adicionales')
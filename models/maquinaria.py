from odoo import fields, models, api
from odoo.exceptions import ValidationError

class TallerMaquinaria(models.Model):
    _name = 'taller.maquinaria'
    _description = 'Gestion maquinas'
    _rec_name = 'modelo_referencia'
    _sql_constraints = [
        ('referencia_uniq', 'unique(referencia)', 'El numero de referencia debe ser unico.'),
    ]

    name = fields.Char(
        string='Maquina',
        compute='_compute_name',
        store=True,
        readonly=True
    )
    referencia = fields.Char(
        string='Numero de referencia',
        required=True
    )
    modelo_maquina = fields.Selection([
        ('modulite', 'ModuLite'),
        ('consola_c10', 'Consola C10'),
        ('validadora_v5', 'Validadora V5'),
        ('validadora_v7', 'Validadora V7'),
        ('velite', 'VéLite'),
        ('ecolite_emv', 'EcoLite EMV'),
        ('router_elite', 'Router éLite'),
    ], string='Modelo de maquina', required=True, default='modulite')

    modelo_referencia = fields.Char(
        string='Modelo y Referencia',
        compute='_compute_modelo_referencia',
        store=True
    )

    cliente_taller_id = fields.Many2one(
        'taller.cliente',
        string='Cliente',
        required=True,
        ondelete='cascade',
        help='Cliente propietario de la maquina'
    )
    cliente_id = fields.Many2one(
        'res.partner',
        string='Compania',
        related='cliente_taller_id.cliente_id',
        readonly=True,
        store=True
    )

    responsable = fields.Many2one(
        'res.users',
        string='Responsable',
        domain="[('groups_id.name', 'in', ['Taller'])]",
        help='Usuario responsable (solo usuarios del grupo Taller)'
    )

    estado = fields.Selection([
        ('fabricacion', 'En fabricacion'),
        ('terminada', 'Terminada'),
        ('reparacion', 'Reparacion')
    ], string='Estado de la maquinaria', required=True, default='fabricacion')

    telefono_cliente = fields.Char(
        string='Telefono del cliente',
        related='cliente_taller_id.telefono',
        readonly=True
    )
    email_cliente = fields.Char(
        string='Email del cliente',
        related='cliente_taller_id.email',
        readonly=True
    )

    @api.depends('cliente_taller_id')
    def _compute_name(self):
        for record in self:
            cliente = record.cliente_taller_id.name or 'Sin cliente'
            record.name = f"{cliente} ({record.id or 'Nuevo'})"

    @api.depends('modelo_maquina', 'referencia')
    def _compute_modelo_referencia(self):
        for record in self:
            modelo = dict(record._fields['modelo_maquina'].selection).get(record.modelo_maquina, '')
            referencia = record.referencia or ''
            record.modelo_referencia = f"{modelo} {referencia}".strip()

    @api.constrains('estado', 'responsable')
    def _check_responsable_reparacion(self):
        for record in self:
            if record.estado == 'reparacion' and not record.responsable:
                raise ValidationError(
                    'Debe seleccionar un Responsable cuando el estado es Reparacion.'
                )
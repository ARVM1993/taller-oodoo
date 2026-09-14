from odoo import fields, models, api
from odoo.exceptions import ValidationError


class TallerMaquinaria(models.Model):
    _name = 'taller.maquinaria'
    _description = 'Gestion maquinas'
    _rec_name = 'num_serie'
    _sql_constraints = [
        ('num_serie_uniq', 'unique(num_serie)', 'El numero de serie debe ser unico.'),
    ]

    cantidad = fields.Integer(
        string='Cantidad',
        required=True,
        default=1
    )
    puerto = fields.Char(
        string='Puerto',
        required=True
    )
    num_serie = fields.Char(
        string='N Serie',
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
    ], string='Modelo', required=True, default='modulite')

    cliente_taller_id = fields.Many2one(
        'taller.cliente',
        string='Cliente',
        required=True,
        ondelete='cascade'
    )
    cliente_id = fields.Many2one(
        'res.partner',
        string='Compania',
        related='cliente_taller_id.cliente_id',
        readonly=True,
        store=True
    )
    ns_cliente = fields.Char(
        string='N/S Cliente',
        help='Numero de serie del cliente'
    )

    fecha_envio = fields.Date(
        string='F. Envio',
        help='Fecha de envio'
    )

    observaciones = fields.Text(
        string='Observaciones'
    )

    conjunto = fields.Char(
        string='Conjunto',
        help='Conjunto al que pertenece (si procede)'
    )
    raspberry = fields.Char(
        string='Raspberry',
        help='Numero de Raspberry'
    )
    id_feig = fields.Char(
        string='ID FEIG',
        help='ID Feig'
    )
    version_pcb = fields.Char(
        string='Version PCB',
        help='Version de la PCB'
    )

    estado = fields.Selection([
        ('fabricacion', 'En fabricacion'),
        ('terminada', 'Terminada'),
        ('reparacion', 'Reparacion')
    ], string='Estado', required=True, default='fabricacion')

    responsable = fields.Many2one(
        'res.users',
        string='Responsable',
        domain="[('groups_id.name', 'in', ['Taller'])]"
    )

    @api.constrains('estado', 'responsable')
    def _check_responsable_reparacion(self):
        for record in self:
            if record.estado == 'reparacion' and not record.responsable:
                raise ValidationError(
                    'Debe seleccionar un Responsable cuando el estado es Reparacion.'
                )
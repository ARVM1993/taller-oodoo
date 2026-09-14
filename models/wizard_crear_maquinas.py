from odoo import fields, models, api
from odoo.exceptions import ValidationError
from datetime import datetime


class TallerCrearMaquinasWizard(models.TransientModel):

    _name = 'taller.crear.maquinas.wizard'
    _description = 'Asistente para crear multiples maquinas'

    cliente_taller_id = fields.Many2one(
        'taller.cliente',
        string='Cliente',
        required=True,
        readonly=True
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

    cantidad = fields.Integer(
        string='Cantidad',
        required=True,
        default=1
    )

    puerto = fields.Char(
        string='Puerto',
        required=True
    )

    num_serie_inicial = fields.Char(
        string='N Serie inicial',
        required=True,
        default='0',
        help='Numero inicial para los numeros de serie (ej: 1, 100, 500)'
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

    def action_crear_maquinas(self):
        self.ensure_one()

        if self.estado == 'reparacion' and not self.responsable:
            raise ValidationError(
                'Debe seleccionar un responsable cuando el estado es Reparacion.'
            )

        if self.cantidad <= 0:
            raise ValidationError(
                'La cantidad debe ser mayor que 0.'
            )

        codigos = {
            'modulite': 'ml',
            'consola_c10': 'c10',
            'validadora_v5': 'v5',
            'validadora_v7': 'v7',
            'velite': 'vl',
            'ecolite_emv': 'el',
            'router_elite': 're',
        }

        codigo_maquina = codigos.get(self.modelo_maquina)

        try:
            numero_inicial = int(self.num_serie_inicial)
        except ValueError:
            numero_inicial = 0

        maquinas_creadas = []

        for i in range(1, self.cantidad + 1):

            num_serie = (
                f"{datetime.now().year}"
                f"{codigo_maquina.upper()}"
                f"{(numero_inicial + i):05d}"
            )

            maquina = self.env['taller.maquinaria'].create({
                'cliente_taller_id': self.cliente_taller_id.id,
                'modelo_maquina': self.modelo_maquina,
                'cantidad': 1,
                'puerto': self.puerto,
                'num_serie': num_serie,
                'responsable': self.responsable.id if self.responsable else False,
                'estado': self.estado,
            })

            maquinas_creadas.append(maquina.id)

        return {
            'type': 'ir.actions.act_window',
            'name': 'Maquinas creadas',
            'res_model': 'taller.maquinaria',
            'view_mode': 'list,form',
            'domain': [('id', 'in', maquinas_creadas)],
            'target': 'current',
        }
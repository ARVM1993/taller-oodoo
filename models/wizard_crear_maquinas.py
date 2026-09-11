from odoo import fields, models, api
from odoo.exceptions import ValidationError

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
    ], string='Modelo de maquina', required=True, default='modulite')
    cantidad = fields.Integer(
        string='Cantidad',
        required=True,
        default=1
    )
    referencia_inicial = fields.Char(
        string='Referencia inicial',
        required=True
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
            raise ValidationError('Debe seleccionar un responsable cuando el estado es Reparacion.')

        if self.cantidad <= 0:
            raise ValidationError('La cantidad debe ser mayor que 0.')

        maquinas_creadas = []

        for i in range(1, self.cantidad + 1):
            if self.cantidad == 1:
                referencia = self.referencia_inicial
            else:
                referencia = f"{self.referencia_inicial}-{i:03d}"

            maquina = self.env['taller.maquinaria'].create({
                'cliente_taller_id': self.cliente_taller_id.id,
                'modelo_maquina': self.modelo_maquina,
                'referencia': referencia,
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
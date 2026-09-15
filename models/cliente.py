from odoo import fields, models, api


class TallerCliente(models.Model):
    _name = 'taller.cliente'
    _description = 'Cliente del taller'
    _rec_name = 'name'
    _sql_constraints = [
        ('cliente_id_uniq', 'unique(cliente_id)', 'Esta compania ya tiene un registro en el taller.'),
    ]

    name = fields.Char(
        string='Nombre',
        required=True,
        readonly=True
    )
    cliente_id = fields.Many2one(
        'res.partner',
        string='Compania',
        required=True,
        domain="[('is_company', '=', True)]",
        help='Solo se pueden seleccionar companias'
    )
    telefono = fields.Char(
        string='Telefono',
        related='cliente_id.phone',
        readonly=True
    )
    email = fields.Char(
        string='Email',
        related='cliente_id.email',
        readonly=True
    )
    direccion = fields.Char(
        string='Direccion',
        related='cliente_id.street',
        readonly=True
    )
    maquinas_ids = fields.One2many(
        'taller.maquinaria',
        'cliente_taller_id',
        string='Maquinas'
    )
    resumen_maquinas = fields.Char(
        string='Resumen de maquinas',
        compute='_compute_resumen_maquinas',
        store=True
    )
    num_reparaciones = fields.Integer(
        string='Total en reparacion',
        compute='_compute_num_reparaciones',
        store=True
    )
    resumen_reparaciones = fields.Char(
        string='Reparaciones por modelo',
        compute='_compute_num_reparaciones',
        store=True
    )

    @api.onchange('cliente_id')
    def _onchange_cliente_id(self):
        if self.cliente_id:
            self.name = self.cliente_id.name

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('cliente_id') and not vals.get('name'):
                cliente = self.env['res.partner'].browse(vals['cliente_id'])
                vals['name'] = cliente.name
        return super().create(vals_list)

    @api.depends('maquinas_ids', 'maquinas_ids.modelo_maquina')
    def _compute_resumen_maquinas(self):
        for record in self:
            total = len(record.maquinas_ids)
            if total == 0:
                record.resumen_maquinas = '0 maquinas'
                continue

            conteo = {}
            for maquina in record.maquinas_ids:
                modelo = dict(maquina._fields['modelo_maquina'].selection).get(
                    maquina.modelo_maquina, 'Desconocido'
                )
                conteo[modelo] = conteo.get(modelo, 0) + 1

            desglose = ', '.join([f"{cant} {mod}" for mod, cant in conteo.items()])
            record.resumen_maquinas = f"{total} maquinas: {desglose}"

    def name_get(self):
        result = []
        for record in self:
            name = record.name or (record.cliente_id.name if record.cliente_id else 'Sin nombre')
            result.append((record.id, name))
        return result

    @api.depends('name', 'cliente_id')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name or (record.cliente_id.name if record.cliente_id else 'Sin nombre')

    @api.depends('maquinas_ids', 'maquinas_ids.estado', 'maquinas_ids.modelo_maquina')
    def _compute_num_reparaciones(self):
        for record in self:
            reparaciones = record.maquinas_ids.filtered(lambda m: m.estado == 'reparacion')
            total = len(reparaciones)
            record.num_reparaciones = total

            if total == 0:
                record.resumen_reparaciones = 'Sin reparaciones'
                continue

            conteo = {}
            for maquina in reparaciones:
                modelo = dict(maquina._fields['modelo_maquina'].selection).get(
                    maquina.modelo_maquina, 'Desconocido'
                )
                conteo[modelo] = conteo.get(modelo, 0) + 1

            desglose = ', '.join([f"{cant} {mod}" for mod, cant in conteo.items()])
            record.resumen_reparaciones = f"{total} reparaciones: {desglose}"
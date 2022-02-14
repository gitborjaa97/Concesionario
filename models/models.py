# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class ConcesionarioMarca(models.Model):
    _name = 'ba.concesionario.marca'

    name = fields.Char(string="Marca",required=True)
    country_id = fields.Many2one("res.country",string="Pais")
    coche_ids = fields.One2many("ba.concesionario.coche","marca_id",string="Coches")
    
class ConcesionarioCoche(models.Model):
    _name = 'ba.concesionario.coche'

    name = fields.Char(string="Modelo",required=True)
    marca_id = fields.Many2one("ba.concesionario.marca",string="Marca",required=True)    
    factura_id = fields.Many2one("ba.concesionario.factura",string="Factura")
    anio = fields.Integer(string="Año")
    transmision = fields.Selection([('0','Manual'),('1','Automatico')],string="Transmision",default="0")
    combustible = fields.Selection([('0','Diesel'),('1','Gasolina'),('2','Electrico'),('3','Gas'),('4','Otros')],string="Combustible",default='0', required=True)
    n_plazas = fields.Integer(string='Numero de plazas')
    cilindrada = fields.Integer(string='Cilindrada')
    cvs = fields.Integer(string='Potencia')
    usado = fields.Boolean(string='Usado')
    kms = fields.Integer(string='Kms')
    n_puertas = fields.Integer(string='Numero de puertas')
    categoria_ids = fields.Many2many("ba.concesionario.categoria",string="Categorias")
    foto = fields.Image(string="Imagen",store=True,relation="res.partner")
    precio = fields.Float(string="Precio",required=True)
    disponibilidad = fields.Boolean(string="Disponible",default= True)

class ConcesionarioCategoria(models.Model):
    _name = 'ba.concesionario.categoria'

    name = fields.Char(string="Categoria",required=True)
    descripcion = fields.Text(string="Descripcion")

class ConcesionarioCliente(models.Model):
    _name = 'ba.concesionario.cliente'

    name = fields.Char(string="Nombre",required=True,help="Introduce el nombre del cliente.")
    foto = fields.Image(string="Imagen",store=True,relation="res.partner")
    calle = fields.Char(string="Calle",required=True)
    cp = fields.Integer(string="Codigo Postal",required=True)
    ciudad = fields.Char(string="Ciudad",required=True)
    email = fields.Char(string="Correo electronico", required=True)
    movil = fields.Char(string="Numero movil", required=True)
    fijo = fields.Char(string="Numero fijo",required=True)

class ConcesionarioFactura(models.Model):
    _name = 'ba.concesionario.factura'

    name = fields.Char(string="Secuencia", required=True, readonly=True, copy=False, default="Nuevo")
    vendedor = fields.Many2one("res.partner",string="Comercial",required=True)
    cliente = fields.Many2one("ba.concesionario.cliente", string="Cliente", required=True)
    coche_ids = fields.One2many("ba.concesionario.coche","factura_id",string="Coches")
    tipo_pago = fields.Selection([('0','Efectivo'),('1','Tarjeta')],string="Tipo de pago",default='1')
    financion = fields.Selection([('0','Al contado'),('1','Financiacion 4 años'),('2','Financiacion 10 años')],string='Financiacion',default='0')
    fecha_compra = fields.Date(string='Fecha de compra',readonly=True,default=datetime.now(),store=True)
    total = fields.Float(string="Total",compute="_importetotal",store=True)

   

    @api.depends('total','coche_ids')
    def _importetotal(self):
        sumatorio = 0
        for r in self:
            for coche in r.coche_ids:
                sumatorio += coche.precio
            r.total = sumatorio

    @api.constrains('coche_ids')
    def _check_something(self):
        for r in self:
            for c in r.coche_ids:
                c.disponibilidad = False



    #https://learnopenerp.blogspot.com/2020/08/generate-create-sequence-number-odoo.html
    #como generar una secuencia
    @api.model
    def create(self, vals):
        if vals.get('name', 'Nuevo') == 'Nuevo':
            vals['name'] = self.env['ir.sequence'].next_by_code('incremento.factura') or 'Nuevo'
        result = super(ConcesionarioFactura, self).create(vals)
            
        return result


    



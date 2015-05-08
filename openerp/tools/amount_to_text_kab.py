#-------------------------------------------------------------------------------
# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

#-------------------------------------------------------------
# Kabyle - DZ
#-------------------------------------------------------------

#To do : delete tens70_kab and tens90_kab dics. It's not necessary since kabyle conversion into letters doesn't have special cases
# si 0 ɣer 9
to_19_kab = ( u'ilem',  'yiwen',   'sin',  'kraḍ', 'kuz',   'sem',   'sed','sa', 'tam', 'tza','mraw','mraw yiwen','mraw sin','mraw Kraḍ','mraw kuz','mraw sem','mraw sed',
              'mraw sa', 'mraw tam','mraw tza')
# si 70 ɣer 79
tens70_kab=('Sat','Sat-yiwen','Sat-sin','Sat-kraḍ','Sat-kuz','Sat-sem','Sat-sed','Sat-sa','Sat-tam','Sat-tza')
# si 90  ɣer 99
tens90_kab=('Tzat','Tzat-yiwen','Tzat-sin','Tzat-kraḍ','Tzat-kuz','Tzat-sem','Tzat-sed','Tzat-sa','Tzat-tam','Tzat-tza')
# 20 30 40 50 60 70 80 90
tens_kab  = ( 'werrem', 'kraḍet', 'kuzet', 'Semmuset', 'Seddiset','Sat', 'Tamet','Tzat')
#100 1000 1000000 100000000 ......
denom_kab = ('Twines','Agim',     'Ifeḍ',         'Ifeḍgim',       'Sifeḍ',       'Agsifeḍ','Sifeḍgim',  'Sagim',      'Sisifeḍ',    'Tzagim',      'Smifeḍ',
              'Smifḍagim',    'Kifeḍgim' )

def _convert_nn_kab(val):
    """ convert a value < 100 to Kabyle
    """
    if(val>=70 and val <80):
        return tens70_kab[val-70]

    if(val>=90 and val <100):
        return tens70_kab[val-90]

    if val < 20:
        return to_19_kab[val]
    for (dcap, dval) in ((k, 20 + (10 * v)) for (v, k) in enumerate(tens_kab)):
        if dval + 10 > val:
            if val % 10:
                return dcap + '-' + to_19_kab[val % 10]
            return dcap

def _convert_nnn_kab(val):
    """ convert a value < 1000 to kabyle
    """
    word = ''
    (mod, rem) = (val % 100, val // 100)
    if rem > 0:
        word = to_19_kab[rem] + ' Twines'
        if mod > 0:
            word += ' '
    if mod > 0:
        word += _convert_nn_kab(mod)
    return word

def kabyle_number(val):
    if val < 100:
        return _convert_nn_kab(val)
    if val < 1000:
         return _convert_nnn_kab(val)
    for (didx, dval) in ((v - 1, 1000 ** v) for v in range(len(denom_kab))):
        if dval > val:
            mod = 1000 ** didx
            l = val // mod
            r = val - (l * mod)
            ret = _convert_nnn_kab(l) + ' ' + denom_kab[didx]
            if r > 0:
                ret = ret + ', ' + kabyle_number(r)
            return ret

def amount_to_text_kab(number, currency):
    number = '%.2f' % number
    units_name = currency
    list = str(number).split('.')
    start_word = kabyle_number(abs(int(list[0])))
    end_word = kabyle_number(int(list[1]))
    cents_number = int(list[1])
    cents_name = (cents_number > 1) and ' Isuntimen' or ' Usuntim'
    final_result = start_word +' '+units_name+' '+ end_word +' '+cents_name
    return final_result



# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 15:18:40 2017

@author: a.likhobabin
"""


def short_current_calc(R_1sum, X_1sum, U_sr_NN=400):
    return U_sr_NN / (3**0.5 * (R_1sum ** 2 + X_1sum ** 2)**0.5)
"""
U_sr_NN (Uср.НН) - среднее номинальное напряжение сети, в которой произошло
 короткое замыкание, В
R_1sum, X_1sum (R1, X1) - соответственно суммарное активное и суммарное
 индуктивное сопротивления прямой последовательности цепи КЗ, мОм.
 Эти сопротивления равны:
R1 = Rт + Rр + RтА + Rкв + Rш + Rк + R1кб + Rвл + Rд
X1 = Xс + Xт + Xр + XтА + Xкв + Xш + R1кб + Rвл
"""
#    return E_f_11 / (R_1sum ** 2 + X_1sum ** 2)**0.5
#    try:
#        a = float(self.ui.lineEdit_A.text())
#        b = float(self.ui.lineEdit_B.text())
#    except ValueError:
#        self.statusBar().showMessage('Введите число.')
#    else:
#        self.ui.lineEdit_C.setText(str(a + b))

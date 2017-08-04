# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 15:18:40 2017

@author: a.likhobabin
"""
import math


def calc_Xs(Xs):
    """
Xs (Хс) - эквивалентное индуктивное сопротивление системы до понижающего
трансформатора, мОм, приведенное к ступени низшего напряжения
    """
    return Xs


def calc_Rt(Pk_nom, U_NN_nom, St_nom):
    """
Rt (Rт) - активное сопротивления прямой последовательности понижающего
трансформатора, мОм, приведенное к ступени низшего напряжения сети

St_nom (Sт.ном) - номинальная мощность трансформатора, кВА
Pk_nom (Рк.ном) - потери короткого замыкания в трансформаторе, кВт
U_NN_nom (UННном) - номинальное напряжение обмотки низшего напряжения
 трансформатора, кВ
    """
    return Pk_nom * U_NN_nom**2 / St_nom**2 * 10**6


def calc_Xt(Pk_nom, U_NN_nom, St_nom, u_k):
    """
Xt (Хт) - индуктивное сопротивления прямой последовательности понижающего
трансформатора, мОм, приведенное к ступени низшего напряжения сети

St_nom (Sт.ном) - номинальная мощность трансформатора, кВА
Pk_nom (Рк.ном) - потери короткого замыкания в трансформаторе, кВт
U_NN_nom (UННном) - номинальное напряжение обмотки низшего напряжения
 трансформатора, кВ
u_k (uк) - напряжение короткого замыкания трансформатора, %
    """
    return (u_k**2 - (100*Pk_nom/St_nom)**2)**0.5 * U_NN_nom**2/St_nom * 10**4


def calc_RtA(RtA):
    """
RtA (RтА) - активное сопротивление первичных обмоток трансформаторов
тока, мОм, значения которых приведены в приложении 5 ГОСТ Р 50270-92
    """
    return RtA


def calc_XtA(XtA):
    """
XtA (ХтА) - индуктивное сопротивление первичных обмоток трансформаторов
тока, мОм, значения которых приведены в приложении 5 ГОСТ Р 50270-92
    """
    return XtA


def calc_Rr(Pr_nom_delta, Ir_nom):
    """
Rr (Rр) - активное сопротивления реактора, мОм

Pr_nom_delta (deltaРр.ном) - потери активной мощности в фазе реактора при
 номинальном токе, Вт
Ir_nom (Iр.ном) - номинальный ток реактора, А
    """
    return Pr_nom_delta / Ir_nom**2 * 10**3


def calc_Xr(f, L, M):
    """
Xr (Хр) - индуктивное сопротивления реактора, мОм

omega_s = 2*pi*f - угловая частота напряжения сети, рад/с
L - индуктивность катушки реактора, Гн
М - взаимная индуктивность между фазами реактора, Гн
    """
    omega_s = 2 * math.pi * f
    return omega_s * (L - M) * 10**3


def calc_R_1sum(Rt, Rr, RtA, Rkv, Rsh, Rk, R_1kb, Rvl, Rd):
    """
R_1sum (R1) - суммарное активное сопротивление прямой последовательности
 цепи КЗ, мОм
    R1 = Rт + Rр + RтА + Rкв + Rш + Rк + R1кб + Rвл + Rд
    """
    return Rt + Rr + RtA + Rkv + Rsh + Rk + R_1kb + Rvl + Rd


def calc_X_1sum(Xs, Xt, Xr, XtA, Xkv, Xsh, X_1kb, Xvl):
    """
X_1sum (X1) - суммарное индуктивное сопротивление прямой последовательности
 цепи КЗ, мОм
    X1 = Xс + Xт + Xр + XтА + Xкв + Xш + X1кб + Xвл
    """
    return Xs + Xt + Xr + XtA + Xkv + Xsh + X_1kb + Xvl


def calc_Ip0_3ph(R_1sum, X_1sum, U_sr_NN=400):
    """
Начальное действующее значение периодической составляющей тока трехфазного КЗ
(Iп0) в килоамперах без учета подпитки от электродвигателей
(при электроснабжении электроустановки от энергосистемы через понижающий
трансформатор)

U_sr_NN (Uср.НН) - среднее номинальное напряжение сети, в которой произошло
 короткое замыкание, В
    """
    return U_sr_NN / (3**0.5 * (R_1sum ** 2 + X_1sum ** 2)**0.5)


def calc_short_current(Xs,
                       Pk_nom, U_NN_nom, St_nom, u_k,
                       Pr_nom_delta, Ir_nom, f, L, M,
                       RtA, XtA,
                       Rkv, Xkv,
                       Rsh, Xsh,
                       Rk,
                       R_1kb, X_1kb,
                       Rvl, Xvl,
                       Rd,
                       U_sr_NN):
    Xs = calc_Xs(Xs)
    Rt = calc_Rt(Pk_nom, U_NN_nom, St_nom)
    Xt = calc_Xt(Pk_nom, U_NN_nom, St_nom, u_k)
    Rr = calc_Rr(Pr_nom_delta, Ir_nom)
    Xr = calc_Xr(f, L, M)
    RtA = RtA
    XtA = XtA
    Rkv = Rkv
    Xkv = Xkv
    Rsh = Rsh
    Xsh = Xsh
    Rk = Rk
    R_1kb = R_1kb
    X_1kb = X_1kb
    Rvl = Rvl
    Xvl = Xvl
    Rd = Rd
    R_1sum = calc_R_1sum(Rt, Rr, RtA, Rkv, Rsh, Rk, R_1kb, Rvl, Rd)
    X_1sum = calc_X_1sum(Xs, Xt, Xr, XtA, Xkv, Xsh, X_1kb, Xvl)
    Ip0_3ph = calc_Ip0_3ph(R_1sum, X_1sum, U_sr_NN)
    return Ip0_3ph

#    return E_f_11 / (R_1sum ** 2 + X_1sum ** 2)**0.5
#    try:
#        a = float(self.ui.lineEdit_A.text())
#        b = float(self.ui.lineEdit_B.text())
#    except ValueError:
#        self.statusBar().showMessage('Введите число.')
#    else:
#        self.ui.lineEdit_C.setText(str(a + b))

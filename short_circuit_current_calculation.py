# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 15:18:40 2017

@author: a.likhobabin
"""
import math


def calc_Xs(switch, Sk_IkVN_Xs_Iotklnom, U_sr_NN, U_sr_VN):
    """
Xs (Хс) - эквивалентное индуктивное сопротивление системы до понижающего
трансформатора, мОм, приведенное к ступени низшего напряжения
switch - переключатель расчёта параметра Xc:
    Sk - расчёт по величине Sк
    IkVN - расчёт по величине IкВН
    Xs - расчёт по величине Xс
    Iotklnom - расчёт по величине Iоткл.ном
U_sr_NN (Uср.НН) - среднее номинальное напряжение сети, подключенной к обмотке
    низшего напряжения трансформатора, В
U_sr_VN (Uср.ВН) - среднее номинальное напряжение сети, к которой подключена
    обмотка высшего напряжения трансформатора, В
Sк - условная мощность короткого замыкания у выводов обмотки высшего напряжения
    трансформатора, MBА
IкВН - действующее значение периодической составляющей тока при трехфазном
    КЗ у выводов обмотки высшего напряжения трансформатора, кА
Iоткл.ном - номинальный ток отключения выключателя, установленного на стороне
    высшего напряжения понижающего трансформатора
    """
    if switch == "IkVN" or switch == "Iotklnom":
        return U_sr_NN**2 / (3**0.5 * Sk_IkVN_Xs_Iotklnom * U_sr_VN)
    elif switch == "Sk":
        return U_sr_NN / Sk_IkVN_Xs_Iotklnom * 10**-3
    else:
        return Sk_IkVN_Xs_Iotklnom


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
#    R_1sum = calc_R_1sum(Rt=0,
#                         Rr=0,
#                         RtA=0,
#                         Rkv=0,
#                         Rsh=0,
#                         Rk=0,
#                         R_1kb=0,
#                         Rvl=0,
#                         Rd=0)
#    X_1sum = calc_X_1sum(Xs=0,
#                         Xt=0,
#                         Xr=0,
#                         XtA=0,
#                         Xkv=0,
#                         Xsh=0,
#                         X_1kb=0,
#                         Xvl=0)
    return U_sr_NN / (3**0.5 * (R_1sum ** 2 + X_1sum ** 2)**0.5)


def calc_short_current(switch="Xs", Sk_IkVN_Xs_Iotklnom=50, U_sr_NN=0.4,
                       U_sr_VN=10,
                       Pk_nom=0, U_NN_nom=0.4, St_nom=0, u_k=0,
                       Pr_nom_delta=0, Ir_nom=0, f=0, L=0, M=0,
                       RtA=0, XtA=0,
                       Rkv=0, Xkv=0,
                       Rsh=0, Xsh=0,
                       Rk=0,
                       R_1kb=0, X_1kb=0,
                       Rvl=0, Xvl=0,
                       Rd=0):
    Xs = calc_Xs(switch, Sk_IkVN_Xs_Iotklnom, U_sr_NN, U_sr_VN)
#    Rt = calc_Rt(Pk_nom, U_NN_nom, St_nom)
#    Xt = calc_Xt(Pk_nom, U_NN_nom, St_nom, u_k)
#    Rr = calc_Rr(Pr_nom_delta, Ir_nom)
#    Xr = calc_Xr(f, L, M)
#    RtA = RtA
#    XtA = XtA
#    Rkv = Rkv
#    Xkv = Xkv
#    Rsh = Rsh
#    Xsh = Xsh
#    Rk = Rk
#    R_1kb = R_1kb
#    X_1kb = X_1kb
#    Rvl = Rvl
#    Xvl = Xvl
#    Rd = Rd
    R_1sum = calc_R_1sum(Rt=0, Rr=0, RtA=0, Rkv=0, Rsh=0, Rk=0, R_1kb=0, Rvl=0, Rd=0)
    X_1sum = calc_X_1sum(Xs, Xt=0, Xr=0, XtA=0, Xkv=0, Xsh=0, X_1kb=0, Xvl=0)
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

# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 15:18:40 2017
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
        return U_sr_NN ** 2 / (3 ** 0.5 * Sk_IkVN_Xs_Iotklnom * U_sr_VN)
    elif switch == "Sk":
        return U_sr_NN ** 2 / Sk_IkVN_Xs_Iotklnom * 10 ** -3
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
    return Pk_nom * (U_NN_nom * 10 ** -3) ** 2 / St_nom ** 2 * 10 ** 6


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
    return (u_k ** 2 - (100 * Pk_nom / St_nom) ** 2) ** 0.5 * (U_NN_nom * 10 ** -3) ** 2 / St_nom * 10 ** 4


def calc_Rta(r_ta):
    """
r_ta (Rта) - активное сопротивление первичных обмоток трансформаторов
тока, мОм, значения которых приведены в приложении 5 ГОСТ Р 50270-92
    """
    return r_ta


def calc_Xta(x_ta):
    """
x_ta (Хта) - индуктивное сопротивление первичных обмоток трансформаторов
тока, мОм, значения которых приведены в приложении 5 ГОСТ Р 50270-92
    """
    return x_ta


def calc_Rr(Pr_nom_delta, Ir_nom):
    """
Rr (Rр) - активное сопротивления реактора, мОм

Pr_nom_delta (deltaРр.ном) - потери активной мощности в фазе реактора при
 номинальном токе, Вт
Ir_nom (Iр.ном) - номинальный ток реактора, А
    """
    return Pr_nom_delta / Ir_nom ** 2 * 10 ** 3


def calc_Xr(f, L, M):
    """
Xr (Хр) - индуктивное сопротивления реактора, мОм

omega_s = 2*pi*f - угловая частота напряжения сети, рад/с
L - индуктивность катушки реактора, Гн
М - взаимная индуктивность между фазами реактора, Гн
    """
    omega_s = 2 * math.pi * f
    return omega_s * (L - M) * 10 ** 3


# def calc_R_1sum(Rt, Rr, RtA, Rkv, Rsh, Rk, R_1kb, Rvl, Rd, Rpr):
def calc_r_sum(*args):
    """
R_1sum (R1) - суммарное активное сопротивление прямой последовательности
 цепи КЗ, мОм
    R1 = Rт + Rр + RтА + Rкв + Rш + Rк + R1кб + Rвл + Rд
    """
    # return Rt + Rr + RtA + Rkv + Rsh + Rk + R_1kb + Rvl + Rd + Rpr
    return sum(args)


# def calc_X_1sum(Xs, Xt, Xr, XtA, Xkv, Xsh, X_1kb, Xvl, Xpr):
def calc_x_sum(*args):
    """
X_1sum (X1) - суммарное индуктивное сопротивление прямой последовательности
 цепи КЗ, мОм
    X1 = Xс + Xт + Xр + XтА + Xкв + Xш + X1кб + Xвл
    """
    # return Xs + Xt + Xr + XtA + Xkv + Xsh + X_1kb + Xvl + Xpr
    return sum(args)


def calc_Kud(r_1sum, x_1sum):
    """
    Куд - ударный коэффициент
    """
    if not r_1sum:  # Если активное сопротивление цепи равно нулю
        return 1
    # Tа - постоянная времени затухания апериодической составляющей тока КЗ
    # ωс - синхронная угловая частота напряжения сети, рад/с
    f = 50  # Частота напряжения сети
    omega = 2 * math.pi * f
    Ta = x_1sum / (omega * r_1sum)
    # φк - угол сдвига по фазе напряжения и периодической составляющей тока КЗ
    fi_k = math.atan(x_1sum / r_1sum)
    # tуд - время от начала КЗ до появления ударного тока, с
    # tud = 0.01 * (math.pi/2 + fi_k) / math.pi
    # Kud = 1 + math.sin(fi_k * math.exp(-tud / Ta))
    tud = 0.01 * (math.pi / 2 + fi_k) / math.pi
    Kud = 1 + math.exp(-1 * tud / Ta)
    return Kud


def calc_Ip0_3ph(r_1sum, x_1sum, U_sr_NN=400.0):
    """
Начальное действующее значение периодической составляющей тока трехфазного КЗ
(Iп0) в килоамперах без учета подпитки от электродвигателей
(при электроснабжении электроустановки от энергосистемы через понижающий
трансформатор)

U_sr_NN (Uср.НН) - среднее номинальное напряжение сети, в которой произошло
 короткое замыкание, В
    """
    if not (r_1sum or x_1sum):
        return float('inf')

    return U_sr_NN / (math.sqrt(3) * math.sqrt(r_1sum ** 2 + x_1sum ** 2))


def calc_Ip0_1ph(r_1sum, x_1sum, r_0sum, x_0sum, U_sr_NN=400.0):
    """
Начальное действующее значение периодической составляющей тока однофазного КЗ
от системы (Iп0(1)) в килоамперах без учета подпитки от электродвигателей
(при электроснабжении электроустановки от энергосистемы через понижающий
трансформатор)

U_sr_NN (Uср.НН) - среднее номинальное напряжение сети, в которой произошло
 короткое замыкание, В
r1 и x1 определяют в соответствии с п. 3.2 настоящего стандарта;
r0 и x0 - суммарное активное и суммарное индуктивное сопротивления нулевой
последовательности расчетной схемы относительно точки КЗ, мОм.
Эти сопротивления равны:
r0 = rот + rр + rТА + rкв + rк + r0ш + r0кб + r0вл + rд
x0 = xот + xр + xТА + xкв + x0ш + x0кб + x0вл,
где r0т и x0т - активное и индуктивное сопротивления нулевой
последовательности понижающего трансформатора;
r0ш и x0ш - активное и индуктивное сопротивления нулевой
последовательности шинопровода;
r0кб и x0кб - активное и индуктивное сопротивления нулевой
последовательности кабеля;
r0вл и x0вл - активное и индуктивное сопротивления нулевой
последовательности воздушной линии (r 0вл = r 1вл , x 0вл
≈ 3x 1вл ).
    """
    if not (r_1sum or x_1sum or r_0sum or x_0sum):
        return float('inf')

    return math.sqrt(3) * U_sr_NN / (math.sqrt((2 * r_1sum + r_0sum) ** 2 + (2 * x_1sum + x_0sum) ** 2))


def calc_Ip0_2ph(r_1sum, x_1sum, U_sr_NN=400.0):
    """
Начальное действующее значение периодической составляющей тока трехфазного КЗ
(Iп0(2)) в килоамперах без учета подпитки от электродвигателей
(при электроснабжении электроустановки от энергосистемы через понижающий
трансформатор)

U_sr_NN (Uср.НН) - среднее номинальное напряжение сети, в которой произошло
 короткое замыкание, В
r1 = rт + rр + rТА + rкв + rш + rк + r1кб + r1вл + rд/2
x 1 = xс + xт + xр + xТА + xкв + xш + x1кб + x1вл
    """
    if not (r_1sum or x_1sum):
        return float('inf')

    return U_sr_NN / (2 * math.sqrt(r_1sum ** 2 + x_1sum ** 2))


def calc_short_current(switch="Xs", Sk_IkVN_Xs_Iotklnom=50, U_sr_NN=0.4,
                       U_sr_VN=10,
                       r_t=0, x_t=0, r_0t=0, x_0t=0,
                       r_pr=0, x_pr=0,
                       # Pr_nom_delta=0, Ir_nom=0, f=0, L=0, M=0,
                       r_r=0, x_r=0,
                       r_ta=0, x_ta=0,
                       r_kv=0, x_kv=0,
                       r_sh=0, x_sh=0, r_0sh=0, x_0sh=0,
                       r_k=0,
                       r_1kb=0, x_1kb=0, r_0kb=0, x_0kb=0,
                       r_vl=0, x_vl=0, r_0vl=0, x_0vl=0,
                       r_d=0):
    x_s = calc_Xs(switch, Sk_IkVN_Xs_Iotklnom, U_sr_NN, U_sr_VN)
    print("Хс = ", x_s)

    # r_t = calc_Rt(Pk_nom, U_NN_nom, St_nom)
    # x_t = calc_Xt(Pk_nom, U_NN_nom, St_nom, u_k)
    # print("Rт = ", r_t)
    # print("Xт = ", x_t)
    #
    # print("Rр = ", r_r)
    # print("Xр = ", x_r)
    #
    # print("Rта = ", r_ta)
    # print("Xта = ", x_ta)
    #
    # print("Rкв = ", r_kv)
    # print("Xкв = ", x_kv)
    #
    # print("Rш = ", r_sh)
    # print("Xш = ", x_sh)
    #
    # print("Rк = ", r_k)
    #
    # print("R1кб = ", r_1kb)
    # print("X1кб = ", x_1kb)
    #
    # print("Rвл = ", r_vl)
    # print("Xвл = ", x_vl)
    #
    # print("Rд = ", r_d)

    #    r_r = calc_Rr(Pr_nom_delta, Ir_nom)
    #    x_r = calc_Xr(f, L, M)

    #    r_ta = r_ta
    #    x_ta = x_ta

    #    r_kv = r_kv
    #    x_kv = x_kv

    #    r_sh = r_sh
    #    x_sh = x_sh

    #    r_k = r_k

    #    r_1kb = r_1kb
    #    x_1kb = x_1kb

    #    r_vl = r_vl
    #    x_vl = x_vl

    #    r_d = r_d

    # Расчёт тока трёхфазного КЗ
    r_1sum_3ph_max = calc_r_sum(r_t, r_pr, r_r, r_ta, r_kv, r_sh, r_k, r_1kb, r_vl)
    r_1sum_3ph_min = calc_r_sum(r_t, r_pr, r_r, r_ta, r_kv, r_sh, r_k, r_1kb, r_vl, r_d)
    x_1sum_3ph = calc_x_sum(x_s, x_t, x_pr, x_r, x_ta, x_kv, x_sh, x_1kb, x_vl)

    print("R1 3ф max = ", r_1sum_3ph_max)
    print("R1 3ф min = ", r_1sum_3ph_min)
    print("X1 3ф = ", x_1sum_3ph)
    # print("R1 max/X1 = ", R_1sum_max/X_1sum)
    # print("R1 min/X1 = ", R_1sum_min/X_1sum)
    # print("X1/R1 max = ", X_1sum/R_1sum_max)
    # print("X1/R1 min = ", X_1sum/R_1sum_min)

    Ip0_3ph_max = calc_Ip0_3ph(r_1sum_3ph_max, x_1sum_3ph, U_sr_NN)
    Ip0_3ph_min = calc_Ip0_3ph(r_1sum_3ph_min, x_1sum_3ph, U_sr_NN)

    i_a0_3ph_max = math.sqrt(2) * Ip0_3ph_max
    i_a0_3ph_min = math.sqrt(2) * Ip0_3ph_min

    Kud_3ph_max = calc_Kud(r_1sum_3ph_max, x_1sum_3ph)
    Kud_3ph_min = calc_Kud(r_1sum_3ph_min, x_1sum_3ph)
    i_ud_3ph_max = Kud_3ph_max * i_a0_3ph_max
    i_ud_3ph_min = Kud_3ph_min * i_a0_3ph_min

    # Расчёт тока однофазного КЗ
    r_1sum_1ph_max = r_1sum_3ph_max
    r_1sum_1ph_min = r_1sum_3ph_min
    x_1sum_1ph = x_1sum_3ph
    r_0sum_1ph = calc_r_sum(r_0t, r_pr, r_r, r_ta, r_kv, r_0sh, r_k, r_0kb, r_0vl, r_d)
    x_0sum_1ph = calc_x_sum(x_0t, x_pr, x_r, x_ta, x_kv, x_0sh, x_0kb, x_0vl)

    print("R0 1ф = ", r_0sum_1ph)
    print("X0 1ф= ", x_0sum_1ph)

    Ip0_1ph_max = calc_Ip0_1ph(r_1sum_1ph_max, x_1sum_1ph, r_0sum_1ph, x_0sum_1ph, U_sr_NN)
    Ip0_1ph_min = calc_Ip0_1ph(r_1sum_1ph_min, x_1sum_1ph, r_0sum_1ph, x_0sum_1ph, U_sr_NN)

    i_a0_1ph_max = math.sqrt(2) * Ip0_1ph_max
    i_a0_1ph_min = math.sqrt(2) * Ip0_1ph_min

    Kud_1ph_max = calc_Kud(2 * r_1sum_1ph_max + r_0sum_1ph, 2 * x_1sum_1ph + x_0sum_1ph)
    Kud_1ph_min = calc_Kud(2 * r_1sum_1ph_min + r_0sum_1ph, 2 * x_1sum_1ph + x_0sum_1ph)
    i_ud_1ph_max = Kud_1ph_max * i_a0_1ph_max
    i_ud_1ph_min = Kud_1ph_min * i_a0_1ph_min

    # Расчёт тока двухфазного КЗ
    R_1sum_2ph_max = calc_r_sum(r_t, r_pr, r_r, r_ta, r_kv, r_sh, r_k, r_1kb, r_vl)
    R_1sum_2ph_min = calc_r_sum(r_t, r_pr, r_r, r_ta, r_kv, r_sh, r_k, r_1kb, r_vl, r_d / 2)
    X_1sum_2ph = calc_x_sum(x_s, x_t, x_pr, x_r, x_ta, x_kv, x_sh, x_1kb, x_vl)

    print("R1 2ф min = ", r_1sum_3ph_min)

    Ip0_2ph_max = calc_Ip0_2ph(R_1sum_2ph_max, X_1sum_2ph, U_sr_NN)
    Ip0_2ph_min = calc_Ip0_2ph(R_1sum_2ph_min, X_1sum_2ph, U_sr_NN)

    i_a0_2ph_max = math.sqrt(2) * Ip0_2ph_max
    i_a0_2ph_min = math.sqrt(2) * Ip0_2ph_min

    Kud_2ph_max = calc_Kud(R_1sum_2ph_max, X_1sum_2ph)
    Kud_2ph_min = calc_Kud(R_1sum_2ph_min, X_1sum_2ph)
    i_ud_2ph_max = Kud_2ph_max * i_a0_2ph_max
    i_ud_2ph_min = Kud_2ph_min * i_a0_2ph_min

    return (Ip0_3ph_max, Ip0_3ph_min, i_a0_3ph_max, i_a0_3ph_min, i_ud_3ph_max, i_ud_3ph_min,
            Ip0_1ph_max, Ip0_1ph_min, i_a0_1ph_max, i_a0_1ph_min, i_ud_1ph_max, i_ud_1ph_min,
            Ip0_2ph_max, Ip0_2ph_min, i_a0_2ph_max, i_a0_2ph_min, i_ud_2ph_max, i_ud_2ph_min)

#    return E_f_11 / (R_1sum ** 2 + X_1sum ** 2)**0.5
#    try:
#        a = float(self.ui.lineEdit_A.text())
#        b = float(self.ui.lineEdit_B.text())
#    except ValueError:
#        self.statusBar().showMessage('Введите число.')
#    else:
#        self.ui.lineEdit_C.setText(str(a + b))

import pandas as pd
import numpy as np
from scipy.special import rel_entr
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score


def zero_norm(x):
    """Normalize array and zero values comprising less than 0.5% 
    of the sum of array.
    """
    s = sum(x)
    for i in range(0, len(x)):
        if x[i]/s < 0.05:
            x[i] = 0
    return x/x.sum()


def js(p, q):
    """Calculate Jensen-Shannon Distance between ground truth 
    array p and privatized array q.
    """
    m = (p + q) / 2.0
    left = rel_entr(p, m)
    right = rel_entr(q, m)
    js = np.sum(left, axis=0) + np.sum(right, axis=0)
    js /= np.log(2)
    return np.sqrt(js / 2.0)


def mpp(p, q):
    """Misleading Presence Penalty: Calculate number of false 
    positives in privatized array q with ground truth array p, 
    multiply outcome by 0.2.
    """
    mp = 0
    if not np.array_equal(np.nonzero(p)[0], np.nonzero(q)[0]):
        for i in range(0, len(q)):
            if p[i] == 0 and q[i] != 0:
                mp += 0.2
    return mp


def bp(p, q):
    """Bias Penalty: Add penalty of 0.25 if the total sum of values 
    in privatized array q exceeds the total sum of values in ground 
    truth array p by more than 500. When implementing in full metric, 
    do this before zero_norm.
    """
    bp = 0
    if np.abs(np.sum(p) - np.sum(q)) > 500:
        bp += 0.25
    return bp


def rcp(p, q):
    """Rank Change Penalty: Create 10 bins for p and q based on their 
    range of values and add penalty of 0.1 every time a value in the 
    privatized array q is in a different bin from its counterpart in 
    the ground truth array p.
    """
    p = np.asarray(p)
    q = np.asarray(q)
    t_bins = np.arange(0, max(p) + (max(p)/9) + 0.01, max(p)/9)
    t_inds = np.digitize(p, t_bins)
    p_bins = np.arange(0, max(q) + (max(q)/9) + 0.01, max(q)/9)
    p_inds = np.digitize(q, p_bins)
    penalty = (len(t_inds) - len(np.where(p_inds==t_inds)[0]))*0.1
    return penalty


def metric(p, q):
    """Calculate the full metric for a privatized array q and ground 
    truth array p.
    """
    p = np.asarray(p)
    q = np.asarray(q)
    bp = bp(p, q)
    if np.sum(p) != 0:
        p = zero_norm(p)
    if np.sum(q) != 0:
        q = zero_norm(q)
    jsd = js(p, q)
    mp = mpp(p, q)
    penalty = rcp(p, q)
    sm = jsd + mp + bp + penalty
    full_metric = 1 - min(sm, 1)
    return round(full_metric, 3)


def df_metric(p_df, q_df):
    """Calculate the metric for privatized dataframe q and ground truth 
    dataframe p.
    """
    m = 0
    for i in range(0, len(p_df)):
        m += metric(p_df[i], q_df[i])
    return m


def time_metric(p_df, q_df):
    """Calculate r_squared value between privatized dataframe q_df and ground
    truth dataframe p_df over the course of 12 months.
    """
    x_axis = np.arange(0, 12)
    t_sum = true.sum(axis=1)
    p_sum = pred.sum(axis=1)
    r_squared = r2_score(t_sum, p_sum)
    return r_squared





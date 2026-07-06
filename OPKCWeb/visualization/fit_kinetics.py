"""
Piecewise-linear MLE fit for viral kinetics data.

Model shape (4 segments):
    1. Horizontal at LOD before the growth phase
    2. Linear growth from LOD to a peak
    3. Linear decline from the peak back to LOD
    4. Horizontal at LOD after clearance

Free parameters: peak_time, peak_height, up_slope (>0), down_slope (>0),
sigma (>0). The peak time is estimated from data (not fixed at t=0).

Likelihood: Gaussian errors for detected values; left-censored (for orientation
'above') or right-censored (for orientation 'below') for BLOD observations.
"""
from __future__ import annotations

import numpy as np
from scipy import optimize
from scipy.stats import norm


def piecewise_predict(t, peak_time, peak_height, up_slope, down_slope, lod, orientation):
    """Evaluate the piecewise-linear model at times `t`.

    orientation='above': peak_height > lod. Segments rise then fall (log10VL scale).
    orientation='below': peak_height < lod. Segments fall then rise (Ct scale).
    """
    t = np.asarray(t, dtype=float)
    sign = 1.0 if orientation == "above" else -1.0
    amplitude = sign * (peak_height - lod)  # positive if params are consistent
    if amplitude <= 0 or up_slope <= 0 or down_slope <= 0:
        return np.full_like(t, lod, dtype=float)

    t_start = peak_time - amplitude / up_slope
    t_end = peak_time + amplitude / down_slope

    y = np.full_like(t, lod, dtype=float)
    up_mask = (t >= t_start) & (t < peak_time)
    down_mask = (t >= peak_time) & (t <= t_end)
    y[up_mask] = lod + sign * up_slope * (t[up_mask] - t_start)
    y[down_mask] = peak_height - sign * down_slope * (t[down_mask] - peak_time)
    return y


def _neg_log_likelihood(params, t, y, is_blod, lod, orientation):
    peak_time, peak_height, log_up, log_down, log_sigma = params
    up_slope = np.exp(log_up)
    down_slope = np.exp(log_down)
    sigma = np.exp(log_sigma)

    # Basic feasibility: peak on the correct side of the LOD
    if orientation == "above" and peak_height <= lod:
        return 1e12
    if orientation == "below" and peak_height >= lod:
        return 1e12

    mu = piecewise_predict(t, peak_time, peak_height, up_slope, down_slope, lod, orientation)

    detected = ~is_blod
    ll = 0.0

    # Gaussian log-density for detected observations
    if detected.any():
        resid = (y[detected] - mu[detected]) / sigma
        ll += np.sum(-0.5 * resid ** 2 - np.log(sigma) - 0.5 * np.log(2 * np.pi))

    # Left/right-censored contribution for BLOD observations
    if is_blod.any():
        if orientation == "above":
            # BLOD means y <= lod, so contribute P(y <= lod | model) = Phi((lod - mu)/sigma)
            z = (lod - mu[is_blod]) / sigma
        else:
            # BLOD means y >= lod (Ct), so contribute P(y >= lod) = 1 - Phi((lod - mu)/sigma)
            z = (mu[is_blod] - lod) / sigma
        # log Phi(z), guarded against underflow
        ll += np.sum(norm.logcdf(z))

    return -ll


def _initial_guess(t, y, is_blod, lod, orientation):
    """Reasonable starting parameters for the optimizer."""
    detected = ~is_blod
    if not detected.any():
        # Nothing detected — degenerate. Return a flat-at-LOD guess.
        return None
    yd = y[detected]
    td = t[detected]

    if orientation == "above":
        # Peak = observed max; if it's not above LOD, bump slightly
        peak_height = float(np.max(yd))
        if peak_height <= lod:
            peak_height = lod + 0.5
        peak_time = float(td[np.argmax(yd)])
    else:
        peak_height = float(np.min(yd))
        if peak_height >= lod:
            peak_height = lod - 0.5
        peak_time = float(td[np.argmin(yd)])

    # Slope initial guesses: rough (peak-LOD)/(observed span)
    amplitude = abs(peak_height - lod)
    span = max(1.0, float(np.max(td) - np.min(td)))
    up_slope = max(0.1, amplitude / span)
    down_slope = up_slope
    sigma = max(0.5, float(np.std(yd - np.mean(yd))))
    return np.array([peak_time, peak_height, np.log(up_slope), np.log(down_slope), np.log(sigma)])


def smoothed_binary(times, is_positive, window_days=2.0, step_days=0.5, min_n=3):
    """Sliding-window mean of positivity over time — the binary analog of the
    MLE fit. For each window centered on t, the y value is the fraction of
    samples in [t - window_days, t + window_days] that were positive.

    Returns the same shape of dict as `fit_kinetics` so the endpoint can hand it
    to the same frontend drawing code.
    """
    times = np.asarray(times, dtype=float)
    is_positive = np.asarray(is_positive, dtype=float)

    n_pos = int(is_positive.sum())
    n_neg = int(len(is_positive) - n_pos)

    if len(times) < min_n:
        return {"success": False, "reason": f"only {len(times)} sample(s), need >={min_n}",
                "n_detected": len(times), "n_blod": 0}

    t_min, t_max = float(np.min(times)), float(np.max(times))
    grid = np.arange(t_min, t_max + step_days, step_days)

    curve_t, curve_y = [], []
    for t in grid:
        mask = (times >= t - window_days) & (times <= t + window_days)
        if int(mask.sum()) < min_n:
            continue
        curve_t.append(float(t))
        curve_y.append(float(is_positive[mask].mean()))

    if len(curve_t) < 2:
        return {"success": False, "reason": "too sparse for smoothing",
                "n_detected": len(times), "n_blod": 0}

    return {
        "success": True,
        "curve": {"t": curve_t, "y": curve_y},
        "params": {"window_days": window_days, "step_days": step_days,
                   "n_pos": n_pos, "n_neg": n_neg},
        "n_detected": len(times),
        "n_blod": 0,
    }


def fit_kinetics(times, values, is_blod, lod, orientation, min_detected=8):
    """Fit the piecewise-linear model to one group's data.

    Returns dict with keys:
        success (bool)
        params: dict with peak_time, peak_height, up_slope, down_slope, sigma
        n_detected, n_blod
        curve: {'t': [...], 'y': [...]} — evaluated on a dense grid for plotting
        reason: str (if success is False)
    """
    times = np.asarray(times, dtype=float)
    values = np.asarray(values, dtype=float)
    is_blod = np.asarray(is_blod, dtype=bool)

    n_detected = int(np.sum(~is_blod))
    n_blod = int(np.sum(is_blod))

    if n_detected < min_detected:
        return {
            "success": False,
            "reason": f"only {n_detected} detected point(s), need >={min_detected}",
            "n_detected": n_detected,
            "n_blod": n_blod,
        }

    x0 = _initial_guess(times, values, is_blod, lod, orientation)
    if x0 is None:
        return {"success": False, "reason": "no detected data", "n_detected": 0, "n_blod": n_blod}

    result = optimize.minimize(
        _neg_log_likelihood,
        x0,
        args=(times, values, is_blod, lod, orientation),
        method="Nelder-Mead",
        options={"xatol": 1e-4, "fatol": 1e-4, "maxiter": 5000},
    )
    if not result.success and result.fun >= 1e11:
        return {"success": False, "reason": "optimizer failed to find feasible fit",
                "n_detected": n_detected, "n_blod": n_blod}

    peak_time, peak_height, log_up, log_down, log_sigma = result.x
    up_slope, down_slope, sigma = float(np.exp(log_up)), float(np.exp(log_down)), float(np.exp(log_sigma))

    # Build a plotting grid spanning the data + a bit of the flat tails
    t_min, t_max = float(np.min(times)), float(np.max(times))
    span = t_max - t_min
    grid_t = np.linspace(t_min - 0.1 * span, t_max + 0.1 * span, 200)
    grid_y = piecewise_predict(grid_t, peak_time, peak_height, up_slope, down_slope, lod, orientation)

    return {
        "success": True,
        "params": {
            "peak_time": float(peak_time),
            "peak_height": float(peak_height),
            "up_slope": up_slope,
            "down_slope": down_slope,
            "sigma": sigma,
            "lod": float(lod),
        },
        "n_detected": n_detected,
        "n_blod": n_blod,
        "curve": {"t": grid_t.tolist(), "y": grid_y.tolist()},
    }

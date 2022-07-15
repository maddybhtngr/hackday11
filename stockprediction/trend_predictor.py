import math

import yfinance as yf

def get_prediction(stock_val):
    dataframe = yf.download(
        tickers=str(stock_val) + ".NS",
        period="ytd",
        interval="5d"
    )

    dataframe = dataframe.dropna()

    slope_positive_threshold = 0.20
    slope_negative_threshold = -0.20

    normalised_open_close_delta = []
    normalised_high_low_delta = []
    normalised_open_adj_close = []
    normalised_close_adj_close = []
    volume = []
    open_value = []
    close_value = []
    high_value = []
    low_value = []
    adj_close = []

    for index, row in dataframe.iterrows():
        open_value.append(row['Open'])
        close_value.append(row['Close'])
        high_value.append(row['High'])
        low_value.append(row['Low'])
        volume.append(row['Volume'])
        adj_close.append(row['Adj Close'])
        normalised_open_close_delta.append((row['Close'] - row['Open']) / (row['Close'] + row['Open']))
        normalised_open_adj_close.append((row['Adj Close'] - row['Open']) / (row['Adj Close'] + row['Open']))
        normalised_close_adj_close.append((row['Close'] - row['Open']) / (row['Close'] + row['Open']))
        normalised_high_low_delta.append((row['High'] - row['Low']) / (row['High'] + row['Low']))

    open_slopes = []
    close_slopes = []
    volume_slopes = []
    high_slopes = []
    low_slopes = []
    adj_close_slopes = []
    n_oc_slopes = []
    n_hl_slopes = []
    n_oac_slopes = []
    n_cac_slopes = []

    def get_slopes(input_list, slope_list: list, start_idx, end_idx, vis: set):
        if start_idx == end_idx or (start_idx, end_idx) in vis:
            return
        start_val = input_list[start_idx]
        end_val = input_list[end_idx]
        slope = (end_val - start_val) / (end_val + 0.1)
        if slope > slope_positive_threshold:
            slope_list.append(1)
        elif slope < slope_negative_threshold:
            slope_list.append(-1)
        vis.add((start_idx, end_idx))
        mid = int((start_idx + end_idx) / 2)
        get_slopes(input_list, slope_list, start_idx, mid, vis)
        get_slopes(input_list, slope_list, mid, end_idx, vis)

    get_slopes(open_value, open_slopes, 0, len(open_value) - 1, set())
    get_slopes(close_value, close_slopes, 0, len(open_value) - 1, set())
    get_slopes(adj_close, adj_close_slopes, 0, len(open_value) - 1, set())
    get_slopes(high_value, high_slopes, 0, len(open_value) - 1, set())
    get_slopes(low_value, low_slopes, 0, len(open_value) - 1, set())
    get_slopes(volume, volume_slopes, 0, len(open_value) - 1, set())
    get_slopes(normalised_open_close_delta, n_oc_slopes, 0, len(open_value) - 1, set())
    get_slopes(normalised_close_adj_close, n_cac_slopes, 0, len(open_value) - 1, set())
    get_slopes(normalised_high_low_delta, n_hl_slopes, 0, len(open_value) - 1, set())
    get_slopes(normalised_open_adj_close, n_oac_slopes, 0, len(open_value) - 1, set())


    def sum_of_slopes(slopes: list):
        return sum(slopes)

    sum_open_slopes = sum_of_slopes(open_slopes)
    sum_close_slopes = sum_of_slopes(close_slopes)
    sum_high_slopes = sum_of_slopes(high_slopes)
    sum_low_slopes = sum_of_slopes(low_slopes)
    sum_volume_slopes = sum_of_slopes(volume_slopes)
    sum_adj_close_slopes = sum_of_slopes(adj_close_slopes)
    sum_n_oc_slopes = sum_of_slopes(n_oc_slopes)
    sum_n_cac_slopes = sum_of_slopes(n_cac_slopes)
    sum_n_hl_slopes = sum_of_slopes(n_hl_slopes)
    sum_oac_slopes = sum_of_slopes(n_oac_slopes)

    max_indicators = sum_open_slopes + sum_close_slopes + sum_high_slopes + sum_low_slopes + sum_volume_slopes
    biased_indicators = (sum_n_oc_slopes + sum_n_cac_slopes + sum_n_hl_slopes + sum_oac_slopes + sum_adj_close_slopes) * 0.6

    return (max_indicators + biased_indicators) / abs(math.ceil((max_indicators + biased_indicators + 0.0001)))

import pandas as pd

def json_timeseries_to_df(data):
    """Converts json timeseries data structure to csv
    Expected input format:
        [
            {
                'data': [
                    [1500681600, 4.61],
                    [1500768000, 4.85]
                ],
                'name': 'throughput'
            }
        ]
    """
    df = (
            pd
            .DataFrame(columns=['timestamp'])
            .set_index('timestamp')
        )

    for node in data:
        node_df = pd.DataFrame.from_records(
                                    node['data'],
                                    columns=['timestamp', node['name']],
                                    index='timestamp')

        # Combine partial data frame with global one
        df = df.combine_first(node_df)

    return df.reset_index()

def df_to_json_timeseries(df):
    """Converts data frame to json with the following
    format:
        [
            {
                'data': [
                    [1500681600, 4.61],
                    [1500768000, 4.85]
                ],
                'name': 'throughput'
            }
        ]
    """
    data = []
    if not df.empty:
        for column in df:
            if column != 'timestamp':
                data.append({
                    'name': column,
                    'data': list(zip(df.timestamp.tolist(), df[column].tolist()))
                    })

    return data
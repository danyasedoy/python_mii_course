from pandas import DataFrame


def summer_analysis(df: DataFrame) -> (float, float, float):
    summer_data = df[(df['Date'].dt.month > 5) & (df['Date'].dt.month < 9)]

    min_price = summer_data['Open'].min()
    max_price = summer_data['Open'].max()
    avg_price = summer_data['Open'].mean()

    return min_price, max_price, avg_price

def winter_analysis(df: DataFrame) -> dict:
    winter_data = df[df['Date'].dt.month.isin([12, 1, 2])].groupby(df['Date'].dt.year)
 
    result = {}

    for year, group in winter_data:
        result[year] = {}
        result[year]['min'] = group['Open'].min()
        result[year]['max'] = group['Open'].max()
        result[year]['avg'] = group['Open'].mean()

    return result

def all_years_analysis(df: DataFrame) -> dict:
    years_data = df.groupby(df['Date'].dt.year)

    result = {}

    for year, group in years_data:
        result[year] = {
            'min': group['Open'].min(),
            'max': group['Open'].max(),
            'avg': group['Open'].mean()
        }

    return result

def year_analysis(df: DataFrame, year: int) -> dict:
    year_data = df[df['Date'].dt.year == year]

    return {
        'min': year_data['Open'].min(),
        'max': year_data['Open'].max(),
        'avg': year_data['Open'].mean()
    }
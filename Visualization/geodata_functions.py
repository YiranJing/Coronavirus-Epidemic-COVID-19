import geopandas
import pandas as pd
import math


def build_ncov_geodf(day_df):
    world_lines = geopandas.read_file('zip://./shapefiles/ne_50m_admin_0_countries.zip')
    world = world_lines[(world_lines['POP_EST'] > 0) & (world_lines['ADMIN'] != 'Antarctica')]
    world = world.rename(columns={'ADMIN': 'name'})

    china = world_lines[world_lines['ADMIN'] == 'China']
    # layers: ['gadm36_CHN_0', 'gadm36_CHN_1', 'gadm36_CHN_2', 'gadm36_CHN_3']
    china_provinces = geopandas.read_file('./shapefiles/gadm36_CHN.gpkg', layer='gadm36_CHN_1')
    china_provinces = china_provinces.rename(columns={'NAME_1': 'name'})

    china_cities = geopandas.read_file('./shapefiles/gadm36_CHN.gpkg', layer='gadm36_CHN_2')
    china_cities = china_cities.rename(columns={'NAME_2': 'name'})

    # set to same projection
    china_provinces.crs = china.crs
    china_cities.crs = china.crs

    state_lines = geopandas.read_file('zip://./shapefiles/ne_50m_admin_1_states_provinces.zip')
    us_state_lines = state_lines[state_lines['iso_a2'].isin(['US','CA','AU'])]

    # merge with coronavirus data
    us_state_ncov = us_state_lines.merge(day_df, left_on='name', right_on='Province/State')

    # merge with coronavirus data
    china_provinces_ncov = china_provinces.merge(day_df, left_on='name', right_on='Province/State')
    china_cities_ncov = china_cities.merge(day_df, left_on='name', right_on='Province/State')

    # add Hong Konng data to Guangdong province data
    g_idx = china_provinces['name'] == 'Guangdong'
    hk_idx = day_df['Province/State'] == 'Hong Kong'
    if g_idx.any() and hk_idx.any():
        hk_confirmed = day_df.loc[hk_idx, 'Confirmed'].values[0]
        china_provinces_ncov.loc[g_idx, 'Confirmed'] += hk_confirmed

    # deselect countries we already dealt with
    rest_of_world = world[~world['name'].isin(['China','United States of America','Australia','Canada'])]
    # merge with coronavirus data
    world_ncov = rest_of_world.merge(day_df, left_on='name', right_on='Country/Region')

    cols = ['name', 'Confirmed', 'geometry']
    ncov = pd.concat([world_ncov[cols], us_state_ncov[cols], china_provinces_ncov[cols], china_cities_ncov[cols]],
                     ignore_index=True)

    ncov['log_confirmed'] = ncov.apply(lambda x: math.log10(x['Confirmed']), axis=1)

    return ncov


def create_location(row):
    if pd.isna(row['Province/State']):
        return row['Country/Region']
    else:
        return row['Province/State'] + ', ' + row['Country/Region']


states_abbr_to_full = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'UM': 'Minor Outlying Islands',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

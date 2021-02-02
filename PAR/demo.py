from sdv.demo import load_timeseries_demo
data = load_timeseries_demo()
entity_columns = ['Symbol']
context_columns = ['MarketCap', 'Sector', 'Industry']
sequence_index = 'Date'

from sdv.timeseries import PAR
model = PAR(entity_columns=entity_columns, context_columns=context_columns, 
            sequence_index=sequence_index)
model.fit(data)


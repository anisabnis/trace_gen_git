import pandas as pd
data = pd.read_csv("trace_small.csv")
entity_columns=['obj_id'] 
context_columns=['obj_sz']  
#sequence_index=['timestamp'] 

from sdv.timeseries import PAR
model=PAR(entity_columns=entity_columns, context_columns=context_columns)  
model.fit(data)
model.save('my_model.pkl')

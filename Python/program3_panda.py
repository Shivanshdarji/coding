import pandas as pd
import numpy as np

data=pd.read_csv("C:/Users/SHIVANSH/Downloads/data.csv")
df=pd.DataFrame(data)
print(df)

import pandas as pd
import numpy as np
data=pd.read_csv("C:/Users/SHIVANSH/Downloads/data.csv")
df=pd.DataFrame(data)
df.describe()

import pandas as pd
import numpy as np
data=pd.read_csv("C:/Users/SHIVANSH/Downloads/data.csv")
df=pd.DataFrame(data)
df.head

import pandas as pd
import numpy as np
data=pd.read_csv("C:/Users/SHIVANSH/Downloads/data.csv")
df=pd.DataFrame(data)
df.info

import pandas as pd
import numpy as np
data=pd.read_csv("C:/Users/SHIVANSH/Downloads/data.csv")
df=pd.DataFrame(data)
df['Duration']
df.iloc[0]
print(df)

import pandas as pd
import numpy as np
data=pd.read_csv("C:/Users/SHIVANSH/Downloads/data.csv")
df=pd.DataFrame(data)
filtered_df = df[df['Duration']>75]
df['pulse']=df['Duration'+25]
grouped=df.groupby("Name").mean()
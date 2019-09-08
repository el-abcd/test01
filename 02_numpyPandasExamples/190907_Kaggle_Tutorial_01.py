import pandas as pd

# Dataframe
df = pd.DataFrame({'Bob': ['I liked it.', 'It was awful.'],
                   'Sue': ['Pretty good.', 'Bland.']},
                  index=['Product A', 'Product B']
                  )
df.head()
print(df)

# Series
ser = pd.Series([1, 2, 3, 6, 5, 4], index=['a', 'b', 3, 4, 5, 'end'],
                name='series_name!'
                )

ser.head()
print(ser)

##
#https://www.kaggle.com/eleeabcd/kernel2c0cebe9b7/edit

fruit_sales = pd.DataFrame(data=[[35,21],[41,34]],
                           columns=['Apples', 'Bananas'], index=['2017 Sales','2018 Sales'])

ingredients = pd.Series(['4 cups','1 cup', '2 large', '1 can'],
                        index=['Flour','Milk','Eggs','Spam'], name='Dinner')

reviews = pd.read_csv('../input/wine-reviews/winemag-data_first150k.csv', index_col=0)
#NOTE: read_csv, NOT from_csv.
#NOTE: index_col, NOT index!

#print(dir(animals))
animals.to_csv('cows_and_goats.csv')
#NOTE: to_csv is on the  data frame!

####
import sqlite3
conn = sqlite3.connect('../input/pitchfork-data/database.sqlite')
#print(dir(sqlite3))
music_reviews = pd.read_sql_query('select * from artists', conn)

###
# second lesson.  https://www.kaggle.com/eleeabcd/exercise-indexing-selecting-assigning/edit
# reference: https://www.kaggle.com/residentmario/indexing-selecting-assigning

#Types
# series type, pandas.core.series.Series

# can access by dot notation (attribute).  Or by indexing.  reviews['country']
# Can use spaces with [].
# getting element of a series, use []
# loc and iloc.
# ROW then column.  ROMan empire, ruled by pandas?  Opposite of normal python.
# column: reviews[:,0]



first_description = reviews.description.iloc[0]
#NOTE: iloc is preferred?

# loc operator: label-based selection. In this paradigm it's the data index value,
# If you have the default integer index column they seem like the same thing?
# But if have a timestamp, etc. for index column, then they are different.

# iloc uses the Python stdlib indexing scheme, where the first element of the range is included and the last one excluded. So 0:10 will select entries 0,...,9. loc, meanwhile, indexes inclusively. So 0:10 will select entries 0,...,10.
# NOTE: iloc uses 'STANDARD' indexing.  loc is INCLUSIVE!!! Nice for alphabetical!
# REMEMBER THIS QUIRK!!!
# iloc = integer location.  loc = 'locate'/search/find.

# set_index()
# Can do LOTS of filtering using .loc!  Can feed in a:b types of filters, &, |, or boolean conditions,
# results.country == 'Italy', reviews.points >= 90, etc.

# isin matching filter...
# isnull notnull

# Can assign a value (to all rows).  Or, an iterable.




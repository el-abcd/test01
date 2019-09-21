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

#reviews = pd.read_csv('../input/wine-reviews/winemag-data_first150k.csv', index_col=0)
#NOTE: read_csv, NOT from_csv.
#NOTE: index_col, NOT index!

#print(dir(animals))
# animals.to_csv('cows_and_goats.csv')
#NOTE: to_csv is on the  data frame!

fruit_sales.iloc[0]

####
import sqlite3
conn = sqlite3.connect('../input/pitchfork-data/database.sqlite')
#print(dir(sqlite3))
music_reviews = pd.read_sql_query('select * from artists', conn)

music_reviews.iloc[0]
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

# NOTE: iloc takes a bracket format!!! How?
#  https://stackoverflow.com/questions/46176656/why-how-does-pandas-use-square-brackets-with-loc-and-iloc
# The square brackets are syntactic sugar for the special method __getitem__. All objects can implement this method in their class definition and then subsequently work with the square brackets.

# Note: This one took me some time.
# sample_reviews = reviews.loc[[1,2,3,5,8]]
# brackets, then syntax hiccups, forgot loc, etc!

# tricky again...
# iloc, MUST BE INTS!  No names...
# but loc can use names!
# remember offset by 1!
# df = reviews.loc[0:99, ['country','variety']]
# OR cols_idx = [0, 11]
# df = reviews.iloc[:100, cols_idx]

# Got it right away.  Seems surprising (but easy) that filter can be first parameter passed in.
# Even simpler than iloc.
# italian_wines = reviews[reviews.country == 'Italy']

# top_oceania_wines = reviews[ (reviews.country.isin(['Australia','New Zealand'])) & (reviews.points >= 95) ]
# NOTE: needed the paren around the filter conditions!!! Else was evaluated wrong!

## read pandas docs a bit.
# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html#indexing-view-versus-copy
# These both yield the same results, so which should you use? It is instructive to understand the order of operations on these and why method 2 (.loc) is much preferred over method 1 (chained []).
# Summary: avoid [][].

####
# Part 3, Summary Functions and Maps!
##
# https://www.kaggle.com/eleeabcd/exercise-summary-functions-and-maps/edit

# NOTE describe
# NOTE: mean(), unique(), value_counts (count, by how common?)
# Series.map() functions...
# DataFrame.apply(), can call a custom method per ROW.  Looks like might do 'in place'?

# pandas will handle a series and a single value (apply to all).
# Faster than map or apply, use internal optimizations!
# map and apply can do more complex things, though.

# countries = reviews.country.unique()
# print(reviews.country.value_counts())

# centered_price = reviews.price - reviews.price.mean()
# Nice!  simple!


# bargain wine.  Am suspicious of using a 80-100 scale, 2x more costly but 1 more point?  Hard to get 2x more points...
# print((reviews.points / reviews.price).idxmax())
# bargain_wine = reviews.iloc[(reviews.points / reviews.price).idxmax()].title
# NOTE: Series.idxmax() method.

# Counts of a string occurring...
    # num_tropical = reviews.description.str.contains('tropical').sum()
    # num_fruity = reviews.description.str.contains('fruity').sum()
    #
    # descriptor_counts = pd.Series([num_tropical, num_fruity], index=['tropical','fruity'])
    # print(descriptor_counts)
# NOTE: NEED to use str in it, CAN'T just use contains on a string object (it seems).

# Try their way ALSO.  Use Series.map.

# nice little apply example...
    # def stars(row):
    #     if row.country == 'Canada':
    #         return 3
    #     else:
    #         if row.points >= 95:
    #             return 3
    #         elif row.points >= 85:
    #             return 2
    #         else:
    #             return 1
    #
    # star_ratings = reviews.apply(stars, axis = 'columns')

######################
# https://www.kaggle.com/eleeabcd/exercise-grouping-and-sorting/edit

#Read the cheatsheet.
#expanding window, basically cumsum!  Each step increase window size!

# reference:  https://www.kaggle.com/residentmario/grouping-and-sorting
# This DataFrame is accessible to us directly using the apply method
#  So, it sounds like they create many "sub dataframmes" for each grouping.
# the "apply" lets you access each of those?

# Use 'series.values.argmax' to get the position of the maximum now.
# argmax!!!!

# .agg([len, min, max])
# Can do several agg's in parallel!!!'
# multi-index.
# groupby(['country','province']).
# pandas.core.indexes.multi.MultiIndex

# They also require two levels of labels to retrieve a value, an operation that looks something like this
# reset_index will reset back to normal index.

# <pandas.core.groupby.generic.DataFrameGroupBy object at 0x7f2ba75b6588>
# So a groupby does NOT produce a dataFrame directly, but a groupby object.
# You need to do some further operation to get a series, it seems!  A size,








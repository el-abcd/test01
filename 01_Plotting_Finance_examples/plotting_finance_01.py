
import altair as alt

#cars = alt.load_dataset('cars')

from vega_datasets import data

cars = data.cars()


chart = alt.Chart(cars).mark_point().encode(
    x='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
    column = 'Cylinders:Q'
).interactive() # interactive needed for plotting?

chart.serve() # Start a browser window with a chart!
print("DONE 001 !!!!")


chart = alt.Chart(cars).mark_bar(opacity=0.1).encode(
    x=alt.value(0),
    x2='Horsepower',
    y='Miles_per_Gallon',
    color='Origin',
) # .interactive()

chart.serve()
print("DONE 002 !!!!")

alt.X

a = 1


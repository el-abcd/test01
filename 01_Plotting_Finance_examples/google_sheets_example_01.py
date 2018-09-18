
import gspread

# https://github.com/burnash/gspread

# follow the example in colabs:

#from google.colab import auth
#auth.authenticate_user()


# https://medium.com/@ashokyogi5/a-beginners-guide-to-google-oauth-and-google-apis-450f36389184
##############################
import httplib2

from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

#CLIENT_SECRET = 'client_secret.json'
CLIENT_SECRET = '/Users/elee/01_git/test01/01_Plotting_Finance_examples/client_secret_769836808193-22bslqejj79j1hgoosdj0ohiuiaf7frf.apps.googleusercontent.com.json'
SCOPE = [
    'https://www.googleapis.com/auth/spreadsheets.readonly',
    'https://www.googleapis.com/auth/drive' #gspread.client.Client.create needs this.
    ]
# HMM, WHY doesn't it detect I changed the scope above, and automatically invalidate/re-authenticate when
# I re-run?  it can detect it is invalid based on time, why not invalid based on scope?
# Would simplify a bit/be less confusing for a beginner.
STORAGE = Storage('credentials.storage')
#STORAGE = Storage('token.json')


# Start the OAuth flow to retrieve credentials
def authorize_credentials():
# Fetch credentials from storage
    credentials = STORAGE.get()
# If the credentials doesn't exist in the storage location then run the flow
    if credentials is None or credentials.invalid:
        flow = flow_from_clientsecrets(CLIENT_SECRET, scope=SCOPE)
        http = httplib2.Http()
        credentials = run_flow(flow, STORAGE, http=http)
    return credentials
credentials = authorize_credentials()

###################################




# ok, oath2client has been deprecated?
# pip install --upgrade google-auth

# I THINK this is doing the "server to server" auth, i.e. the co-labs servers might already be setup for
# access I guess.
#from google.colab import auth
#auth.authenticate_user()


# https://medium.com/@ashokyogi5/a-beginners-guide-to-google-oauth-and-google-apis-450f36389184
# console.cloud.google.com

import gspread
from oauth2client.client import GoogleCredentials

gc = gspread.authorize(credentials ) # GoogleCredentials.get_application_default())


#task = 'read_existing_sheet'
task = 'write_a_new_sheet'

if task == 'read_existing_sheet':
    worksheet = gc.open('180916 test spreadsheet created from api').sheet1

    # get_all_values gives a list of rows.
    rows = worksheet.get_all_values()
    print(rows)

    # Convert to a DataFrame and render.
    import pandas as pd
    pd.DataFrame.from_records(rows)

elif task == 'write_a_new_sheet':
    # Writing to a spreadsheet:

    sheet_name = 'A new spreadsheet'
    sh = gc.create(sheet_name)

    # Open our new sheet and add some data.
    worksheet = gc.open('A new spreadsheet').sheet1

    cell_list = worksheet.range('A1:C2')

    import random
    for cell in cell_list:
      cell.value = random.randint(1, 100)

    worksheet.update_cells(cell_list)
    print("Go to https://sheets.google.com to see your new spreadsheet (named '{}').".format(sheet_name))
    print("Worksheet id is: {}".format(sh.id))

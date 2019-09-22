
from intuitlib.client import AuthClient
from quickbooks_id_encrypted import client_id, client_secret, redirect_uri, environment, realm_id, oauth2_token_from_auth

# Store credentials in here (not sure which are secret, but just assume they are).
# Try using git-crypt to store these in the repo.
# https://github.com/AGWA/git-crypt
#  brew install git-crypt
#  brew install gpg
# follow some of the gpg getting started info here:  https://github.com/StackExchange/blackbox#how-to-indoctrinate-a-new-user-into-the-system
#  gpg --gen-key
#  Real name: E Lee
# Email address: el_abcd@yahoo.com
# Give up for now, too many steps, how to backup the PGP keys also......
# Just leave out some things when backing them up...


# Go from the "prod app keys" page to the Playground link... https://developer.intuit.com/app/developer/appdetail/prod/keys?appId=djQuMTo6OGQzYmJlYTI3Yg:061f8ffe-afc2-4713-a58c-ca76af289a88
# Select the "production" app at the top...


##################################
# Try this one:
# https://github.com/sidecars/python-quickbooks/blob/master/README.md
from quickbooks import QuickBooks

auth_client = AuthClient( client_id, client_secret, redirect_uri, environment )
# url = auth_client.get_authorization_url([Scopes.ACCOUNTING])

# Hmm, WHERE to get the refresh token from?  I think that requires the "sign in"
# flow, etc.
# https://stackoverflow.com/questions/30605128/python-with-quickbooks-online-api-v3

# Or, see this guide.
# https://developer.intuit.com/app/developer/qbo/docs/develop/authentication-and-authorization/oauth-2.0
# OAuth 2.0 for server-side web apps
# Your app needs an OAuth 2.0 Access Token to access QuickBooks Online data. The OAuth 2.0 playground is the easiest way to get your access token.
#  https://developer.intuit.com/app/developer/playground
# CAN GET THE AUTH TOKEN FOR EITHER SANDBOX OR PRODUCTION APP!!!

# ALSO, this test API page lets you try things out...
# https://developer.intuit.com/app/developer/qbo/docs/api/accounting/all-entities/account


# https://developer.intuit.com/app/developer/qbo/docs/get-started

#  By now, you have your Client ID, Client Secret, and OAuth access token. Next, you can try making an API call. In the snippet below:
from quickbooks import QuickBooks
client = QuickBooks(
        auth_client=auth_client,
        refresh_token=oauth2_token_from_auth['refreshToken'], #'REFRESH_TOKEN',
        company_id= realm_id,  #'COMPANY_ID',
        # minorversion=4
    )


from quickbooks.objects.customer import Customer
customers = Customer.all(qb=client)
# Note: The maximum number of entities that can be returned in a response is 1000. If the result size is not specified, the default number is 100. (See Intuit developer guide for details)
print("####################\nShow CUSTOMER NAMES\n####################")
for (cnt, a) in enumerate(customers):
    print(cnt, a.DisplayName)


from quickbooks.objects.account import Account
accounts = Account.all(qb=client)
print("####################\nShow ACCOUNT NAMES\n####################")
for (cnt, a) in enumerate(accounts):
    print(cnt, a.Name)



import sys

import pandas as pd
import numpy as np
from Code.config import get_path

pd.set_option('display.width', 500)


def main():
    path = get_path()

    dels = pd.DataFrame(pd.read_csv(path + '/Footfall/Data/Cleaned/Final/delegates.csv', encoding='utf-8'))
    seg = pd.DataFrame(pd.read_csv(path + '/Footfall/Data/Cleaned/Final/segmentation.csv', encoding='latin1'))
    revenue = pd.DataFrame(pd.read_csv(path + '/Footfall/Data/Cleaned/Final/revenue.csv', encoding='latin1'))
    sessions = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/works.csv', encoding='latin1'))
    bookings = pd.DataFrame(pd.read_csv(path + '/Footfall/Data/Cleaned/Final/bookings.csv', encoding='latin1'))
    speakers = pd.DataFrame(pd.read_csv(path + '/Footfall/Data/Cleaned/Final/speakers.csv', encoding='latin1'))
    seminars = pd.DataFrame(pd.read_csv(path + '/Footfall/Data/Cleaned/Final/seminars.csv', encoding='latin1'))





    sys.exit()
    a = sessions.merge(seminars, on='Seminar', how='inner').reset_index()
    a.rename(columns={'index': 'Session ID'}, inplace=True)
    b = a.merge(speakers, on='Seminar', how='inner')

    c = dels.merge(b, on='Name', how='left')

    d = c.merge(revenue, on='Name', how='left')

    e = d.merge(seg, left_on='Account', right_on='Account Name', how='left')

    e = e.replace('n/a', np.NaN)

    e.fillna(value=np.nan, inplace=True)



    e.to_csv('/Users/JackShipway/Desktop/data.csv', index=None, encoding='utf-8-sig')

    sys.exit()





    a = seminars.merge(speakers, on='Seminar', how='inner')
    b = sessions.merge(a, on='Seminar', how='left')

    c = seg.merge(bookings, left_on='Account Name', right_on='Account', how='inner')
    d = dels.merge(revenue, on='Name', how='left').merge(c, left_on='Account', right_on='Account Name', how='left')

    e = pd.DataFrame(d.merge(b, on='Name', how='left'))

    e.to_csv(
        '/Users/JackShipway/Desktop/Ascential/Projects/M2020/Europe/Copenhagen/Footfall/Data/Cleaned/Final/data.csv',
        index=None, encoding='utf-8-sig')

    sys.exit()

    dels = dels[dels['Type'] == 'Delegate']
    revenue = revenue[revenue['Revenue'] > 0]

    a = sessions.merge(dels, on='Name', how='left').dropna(subset=['Type'])

    b = a.merge(seminars, on='Seminar', how='left')

    c = b.merge(speakers, on='Seminar', how='left')

    d = c.merge(revenue, on='Name', how='left')

    f = seg.merge(bookings, left_on='Account Name', right_on='Account', how='inner')

    e = pd.DataFrame(d.merge(f, left_on='Account', right_on='Account Name', how='left'))

    g = e.groupby('Name')['Revenue'].mean().reset_index().dropna()

    g['Revenue'] = g['Revenue'].astype(float)

    sys.exit()

    sys.exit()
    # d = c.merge(revenue, on=)











    sys.exit()

    c = b.dropna(subset=['Account Name'])

    d = c.merge(bookings, left_on='Account Name', right_on='Account', how='left')

    print d

    sys.exit()

    # a = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/arrivals.csv'))
    #
    # print len(pd.unique(a['clientReference']))
    #
    #
    #
    #
    #
    # sys.exit()
    #
    #
    #
    #
    attendee_list = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/AttendeeList.csv').drop(
        ['Phone', 'External Link', 'Date Created', 'Registration Reference'], axis=1))
    group_map = {'Wristband to collect': 1, None: 0}
    attendee_list['Group'] = attendee_list['Group'].replace(group_map)
    attendee_list.columns = ['First Name', 'Last Name', 'Company', 'DelegateType', 'Wristband', 'Country',
                             'Email Address', 'ClientRef', 'FirstSeen', 'Job']
    attendee_list['ID'] = attendee_list['First Name'] + ' ' + attendee_list['Last Name'] + ' ' + attendee_list[
        'Email Address']
    for col in ['Company', 'DelegateType', 'Country', 'Job']:
        attendee_list[col] = attendee_list[col].str.title()

    sessions = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/sessions.csv').drop(
        ['dateCreated', 'registrationReference.1', 'company', 'categoryName',
         'groupName', 'country', 'jobTitle', 'registrationReference'], axis=1))
    sessions.columns = ['ScanIn', 'ScanOut', 'Name', 'Surname', 'Seminar', 'Start', 'Finish', 'Location', 'ClientRef',
                        'Email']
    sessions['ID'] = sessions['Name'] + ' ' + sessions['Surname'] + sessions['Email']
    for col in ['Seminar', 'Location']:
        sessions[col] = sessions[col].str.title()
    sessions = sessions.drop_duplicates().reset_index()
    sessions = pd.DataFrame(sessions.drop(['Name', 'Surname', 'Email'], axis=1))

    sessions = sessions.dropna(subset=['ClientRef'])
    print sessions

    b = sessions.merge(attendee_list, on='ClientRef', how='inner')
    print len(pd.unique(b['ClientRef']))

    sys.exit()

    b = sessions.merge(a, left_on='ClientRef', right_on='clientReference', how='inner')

    revenue = pd.DataFrame(pd.read_csv('/Users/JackShipway/Desktop/revenue.csv')).reset_index(drop=True)
    revenue['ID'] = revenue['Contact: Full Name'] + revenue['Contact Email']

    c = revenue.merge(b, on='ID', how='inner')

    d = c.drop_duplicates(subset=['clientReference'], keep='first')

    sys.exit()





    # path = get_path()  # File path to data store
    #








    # # Clean Pre-prints List
    # print_map = {None: 0}
    # attendee_list['Wristband'] = attendee_list['Wristband'].replace(print_map)
    #
    # # Clean Arrivals
    # arrivals = pd.DataFrame(pd.read_csv(path+'/arrivals.csv'))
    # arrivals.columns = ['ClientRef', 'Arrived']
    # arrivals = arrivals.drop_duplicates()
    # b = attendee_list.merge(arrivals, on='ClientRef', how='outer')
    # b['Arrived'] = b['Arrived'].replace(print_map)
    #
    # # Clean Sessions
    # sessions = pd.DataFrame(pd.read_csv(path+'/Joined/sessions.csv').drop(['dateCreated', 'registrationReference.1', 'company',
    #                                                                        'categoryName', 'groupName','country', 'jobTitle',
    #                                                                        'registrationReference'], axis=1))
    # sessions.columns=['ScanIn', 'ScanOut', 'Name', 'Surname', 'Seminar', 'Start', 'Finish', 'Location', 'ClientRef', 'Email']
    # for col in ['Seminar', 'Location']:
    #     sessions[col] = sessions[col].str.title()
    # sessions['ID'] = sessions['Name']+' '+sessions['Surname']+' '+sessions['Email']
    # sessions = pd.DataFrame(sessions.drop(['Email'], axis=1))
    # c = sessions.dropna(subset=['ClientRef'])
    # c = c.drop_duplicates()
    #
    # # Join sessions on ClientRef
    # merged = c.merge(b, on='ClientRef', how='outer')
    #
    # # Clean Delegates
    # dels = pd.DataFrame(pd.read_csv(path+'/Joined/delegates17.csv').drop('JobTitle', axis=1))
    #
    # for col in ['FullName']:
    #     dels[col] = dels[col].str.title()
    # dels['ID'] = dels['FullName'] + ' ' + dels['Email']
    # dels = pd.DataFrame(dels.drop(['FullName', 'Email'], axis=1))
    # dels = dels.drop_duplicates()
    #
    # # Merge tables
    # e = pd.DataFrame(merged.merge(dels, on='ID', how='outer'))
    #
    # pre_prints = pd.DataFrame(pd.read_csv(path + '/pre_prints.csv').drop(['ClientRef'], axis=1))
    # pre_prints['Pre-Print'] = pre_prints['Pre-Print'].replace(print_map)
    # pre_prints.columns = ['Name', 'Surname', 'PrePrinted']
    # g = e.merge(pre_prints, on=['Name', 'Surname'], how='outer')
    # g['PrePrinted'] = g['PrePrinted'].replace(print_map)
    # g = pd.DataFrame(g.drop_duplicates())
    #
    # g = pd.DataFrame(g.drop(['Name', 'Surname'], axis=1))
    #
    # g = g.dropna(subset=['Revenue'])
    #
    # # g.to_csv(path+'/Joined/final.csv', index=None)
    #
    # g = g.drop_duplicates(subset=['ID'])
    # print g[(g['Country'] == 'Norway') & (g['Revenue'] > 0)]
    #
    # 45000000/




    # e.to_csv(path+'/Joined/DelJoin.csv', index=None, encoding='utf-8-sig')





    # a.to_csv(path+'/Joined/joined.csv', index=None, encoding='utf-8-sig')


if __name__ == '__main__':
    main()

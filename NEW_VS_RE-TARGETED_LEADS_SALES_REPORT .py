#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#LIBRARY IMPORTS
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().magic(u'matplotlib inline')
sns.set_style('darkgrid')


#DATA IMPORT
retargeted_lead = pd.read_csv('rt_leads.csv')
new_lead = pd.read_csv('n_leads.csv')
sale = pd.read_excel('sale.xlsx', skiprows=[0])

#SOURCE DICTONARY
source = {'google' : 'Google Search Ad','google-search-ad' : 'Google Search Ad','google-paid-search': 'Google Search Ad',
          'google-ad': 'Google Search Ad','Pivot-cmo-google-search-ad': 'Google Search Ad',
          'google-search-ad,pivot-cmo-google-search-ad': 'Google Search Ad','pivot-cmo-google-search-ad': 'Google Search Ad',
          'google-search-ads':'Google Search Ad','googleindia':'Google Search Ad','google-ad-extension':'Google Search Ad',
          'googleforeign':'Google Search Ad',
          
         'Organic Search':'Organic Search',
         
         'Direct Traffic':'Direct Traffic',
         
         'Skill-lync-blog':'Skill-lync-blog',
         
         'Outbound Phone call':'Outbound Phone call',
        
         'Inbound Phone call':'Inbound Phone call',
         
         'Workshop':'Workshop','Everwebinar':'Workshop','Workshop Leads':'Workshop',
         
         'youtube':'YouTube Videos','youtube-workshop-videos':'YouTube Videos','youtube-videos':'YouTube Videos',
         'youtube-science-videos':'YouTube Videos','youtube-testimonial-video':'YouTube Videos',
         'youtube-daily-post':'YouTube Videos','youtube-workshop-video':'YouTube Videos', 'skill-lync-youtube':'YouTube Videos',
         'youtube-workshop-video':'YouTube Videos','career-videos':'YouTube Videos',
         'skill-lync-youtube-science-video':'YouTube Videos',
         
         'facebook-homepage-button':'Facebook Posts/Videos','facebook-daily-video':'Facebook Posts/Videos',
         'facebook-daily-post':'Facebook Posts/Videos',
         
         'insta-bio':'Instagram Bio','insta-story':'Instagram Bio',
         
         'Facebook Lead Ad':'Facebook Ad','Facebook conversion ad':'Facebook Ad','Facebook-traffic-ad':'Facebook Ad',
         'fb':'Facebook Ad','social media':'Facebook Ad','Facebook':'Facebook Ad',
         'pivot cmo facebook lead ad':'Facebook Ad','pivot cmo facebook ad':'Facebook Ad',
         'Facebook ads':'Facebook Ad','DM_CFD':'Facebook Ad','DM_Design':'Facebook Ad','FBConversionAds':'Facebook Ad',
         'DM_MHEVD':'Facebook Ad','facebook-conversion-ad':'Facebook Ad','pivot-facebook-traffic-ad':'Facebook Ad',
         'Pivot Facebook Lead Ad':'Facebook Ad','Social Media':'Facebook Ad','facebook-traffic-ad':'Facebook Ad',
         'DM_FBAds':'Facebook Ad','Facebook Messages':'Facebook Ad',
         
         'LinkedIn Ads':'LinkedIn Ads','LInikedIn Lead Ads':'LinkedIn Ads','LinkedIn Lead Ad':'LinkedIn Ads','linkedin-traffic-ad':'LinkedIn Ads',
         
         'LinkedIn Report':'LinkedIn Report',
         
         'linkedin-daily-post':'LinkedIn Posts','linkedin-daily-video':'LinkedIn Posts','linkedin-homepage-button':'LinkedIn Posts',
         'linkedin-post':'LinkedIn Posts',
          
         'Collect Chat':'Collect Chat',
         
         'Quora Ads':'Quora Ads','Quora%20Ads':'Quora Ads','quora-traffic-ad':'Quora Ads',
          
         'skill-lync-quora':'Quora','quora':'Quora','quora-answer':'Quora',
          
         'Google Display Ad':'Google Display Ad','Pay per Click Ads':'Google Display Ad','Google%20Display%20Ad':'Google Display Ad',
         'Google Display Ad,google':'Google Display Ad','Google Display Ad,google':'Google Display Ad',
          
         'Kaleyra Inbound Call':'Kaleyra Inbound Call','Kaleyra Voice':'Kaleyra Inbound Call',
         
         'FreshWorld':'FreshWorld',
         
         'Monster Jobs':'Monster Jobs',
         
         'Times Jobs':'Times Jobs',
         
         'JustDial':'JustDial', 'Justdial':'JustDial',
         
         'Unknown':'Unknown','Baja Team Email':'Unknown','Referral Sites':'Unknown','Upviral':'Unknown','Test Button Website':'Unknown',
         'Employability Test':'Unknown','Tawk Live Chat':'Unknown','watsapp':'Unknown',
          
         'Newspaper Ad':'Newspapaer Ad','Newspaper':'Newspapaer Ad','Newspaper+Ad':'Newspapaer Ad','Newspaper%20Ad':'Newspapaer Ad',
          
         'Customer Referral':'Customer Referral',
          
         'skill-lync-blog':'Blog',
          
         'Taboola':'Taboola',
          
         'Wisdom jobs':'Wisdom jobs',
         }


#RETARGETED DATA MANUPILATION
retargeted_lead['Source'] = retargeted_lead['Lead Source'].map(source) 
retargeted_lead['Source'].fillna('UN-NAMED',inplace = True)
r_lead = retargeted_lead.pivot_table(index='Source',values='Email',aggfunc='count')
r_lead=r_lead.rename(columns={'Email':'No of Leads'})

#NEW DATA MANUPILATION
new_lead['Source'] = new_lead['Lead Source'].map(source)
new_lead['Source'].fillna('UN-NAMED',inplace = True)
n_lead = new_lead.pivot_table(index='Source',values='Email',aggfunc='count')
n_lead=n_lead.rename(columns={'Email':'No of Leads'})


#SALE DATA MANUPILATION
sale['Lead Created Date']= pd.to_datetime(sale['Lead Created Date'])
sale['Lead Source'].fillna('Unknown',inplace = True)
sale['Source'] = sale['Lead Source'].map(source)
sale['Source'].fillna('UN-NAMED',inplace = True)
sale.sort_values(by='Lead Created Date')


#NEW SALE DATA MANUPILATION
new_lead_sale = sale.loc[sale['Lead Created Date'] > pd.datetime(2020,02,01)]
N_sale = new_lead_sale.pivot_table(index='Source',values=['Email','Course cost'],aggfunc={'Email':'count',
                                                                        'Course cost' : 'sum'})
N_sale = N_sale.rename(columns={'Email':'No of sales'})
N_sale = N_sale[['No of sales','Course cost']]


#RETARGETTED SALE DATA MANUPILATION
retargeted_lead_sale = sale.loc[sale['Lead Created Date'] < pd.datetime(2020,02,01)]
RT_sale = retargeted_lead_sale.pivot_table(index='Source',values=['Email','Course cost'],aggfunc={'Email':'count',
                                                                        'Course cost' : 'sum'})
RT_sale = RT_sale.rename(columns={'Email':'No of sales'})
RT_sale = RT_sale[['No of sales','Course cost']]


#NEW LEAD SALE REPORT
new_lead_sale_report = pd.merge(n_lead,N_sale,on='Source',how='left')
new_lead_sale_report['Lead Conversion %'] = (new_lead_sale_report['No of sales']/new_lead_sale_report['No of Leads'])*100 
new_lead_sale_report.fillna(0, inplace=True)
new_lead_sale_report.round(2)

#RETARGETED LEAD SALE REPORT
retargeted_sale_report = pd.merge(r_lead,RT_sale,on='Source',how='left')
retargeted_sale_report['Lead Conversion %'] = (retargeted_sale_report['No of sales']/retargeted_sale_report['No of Leads'])*100 
retargeted_sale_report.fillna(0, inplace=True)
retargeted_sale_report.round(2)

#SALE VISUALIZATION
retargeted_sale_report['month'] = 'other months'
new_lead_sale_report['month'] = 'last month'
report = (pd.concat((retargeted_sale_report,new_lead_sale_report)))
report.sort_values(by='month')
report.round(2)

fig_dims = (15, 15)
fig, ax = plt.subplots(figsize=fig_dims)
chart = sns.barplot(x='Lead Conversion %', y = 'Source', data= report.reset_index(),hue='month',ax=ax)
chart.set(xticks=np.arange(0,55,2))

#CSV DOCUMENT
report.to_csv(r'C:\Users\Skill-lync user\Desktop\Monthly_retargeted_vs_new_lead_sales_report.csv')


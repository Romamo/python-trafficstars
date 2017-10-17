from trafficstars import Trafficstars

TRAFFICSTARS_ID = '`1234'
TRAFFICSTARS_SECRET = 'qwert'
TRAFFICSTARS_USERNAME = 'email'
TRAFFICSTARS_PASSWORD = 'passwd'

ts = Trafficstars(TRAFFICSTARS_ID, TRAFFICSTARS_SECRET, TRAFFICSTARS_USERNAME, TRAFFICSTARS_PASSWORD)

print "Your campaigns"
data = ts.campaign_list()
for r in data['response']:
    print r['id'], r['status'], r['clicks']

print "Your banners"
campaign = 0
if campaign:
    banners = dict()
    data = ts.banner_list(campaign_id=campaign)
    for r in data['response']:
        banners[r['id']] = r

    stats = dict(total=dict(impressions=0, clicks=0, price=0))
    page = 1
    while True:
        data = ts.stats_advertiser('creative', campaign_id=47729, date_from='2017-05-20', page=page)

        for r in data['response']:
            if not stats.get(r['banner_id']):
                stats[r['banner_id']] = r
            else:
                stats[r['banner_id']]['impressions'] += r['impressions']
                stats[r['banner_id']]['price'] += r['price']
                stats[r['banner_id']]['clicks'] += r['clicks']

            if r.get('banner_url') and not stats[r['banner_id']].get('color'):
                import re
                m = re.search(r'c5=(\d+)&c6=(\w+)', r['banner_url'])
                # print m.group(1), m.group(2)
                stats[r['banner_id']]['color'] = m.group(2)
                stats[r['banner_id']]['angle'] = m.group(1)

            stats['total']['impressions'] += r['impressions']
            stats['total']['price'] += r['price']
            stats['total']['clicks'] += r['clicks']

        page += 1
        if data['page_count'] < page:
            break

    # print stats
    for k, r in stats.items():
        if r['clicks']:
            cpc = float(r['price']) / r['clicks']
        else:
            cpc = r['price']

        ctr = float(r['clicks']) / r['impressions'] * 100

        if r.get('banner_id'):
            k = r['banner_id']

            print u'{} {} {:6} {:6} {:.2f} {:.3f} {}'.format(k, r['angle'], r['color'], r['impressions'], ctr, cpc, banners[r['banner_id']]['status'])

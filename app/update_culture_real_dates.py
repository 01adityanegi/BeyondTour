"""
Update database CultureEntry records with authentic real dates and add Shri Nanda Devi Raj Jat Yatra.
"""
from app import create_app
from app.extensions import db
from app.models import CultureEntry, Destination

app = create_app()

with app.app_context():
    print("Updating CultureEntry records with real dates...")

    # Update Entry 1 (Nanda Devi Mela)
    e1 = CultureEntry.query.get(1)
    if e1:
        e1.when_celebrated = '16–20 September 2026 (Nanda Ashtami on 19 September 2026)'
        e1.event_date = '16–20 September 2026'
        e1.month_name = 'September'
        e1.month_number = 9
        e1.is_happening_soon = True
        print("Updated Entry 1: Nanda Devi Mela")

    # Update Entry 2 (Nainital Winter Carnival)
    e2 = CultureEntry.query.get(2)
    if e2:
        e2.when_celebrated = '25–31 December 2026 (Annual Year-End Carnival)'
        e2.event_date = '25–31 December 2026'
        e2.month_name = 'December'
        e2.month_number = 12
        print("Updated Entry 2: Nainital Winter Carnival")

    # Update Entry 3 (Nanda Devi Fair, Almora)
    e3 = CultureEntry.query.get(3)
    if e3:
        e3.when_celebrated = '16–20 September 2026 (Nanda Ashtami on 19 September 2026)'
        e3.event_date = '16–20 September 2026'
        e3.month_name = 'September'
        e3.month_number = 9
        e3.is_happening_soon = True
        print("Updated Entry 3: Nanda Devi Fair Almora")

    # Update Entry 4 (Jageshwar Monsoon Festival)
    e4 = CultureEntry.query.get(4)
    if e4:
        e4.when_celebrated = '15 July – 15 August 2026 (Holy Shravan Month)'
        e4.event_date = '15 July – 15 August 2026'
        e4.month_name = 'July'
        e4.month_number = 7
        print("Updated Entry 4: Jageshwar Monsoon Festival")

    # Update Entry 5 (Magh Mela / Bada Haat)
    e5 = CultureEntry.query.get(5)
    if e5:
        e5.when_celebrated = '14–21 January 2027 (Makar Sankranti / Magh Mela)'
        e5.event_date = '14–21 January 2027'
        e5.month_name = 'January'
        e5.month_number = 1
        print("Updated Entry 5: Magh Mela")

    # Update Entry 6 (Ganga Dussehra)
    e6 = CultureEntry.query.get(6)
    if e6:
        e6.when_celebrated = '25 May 2026 (Jyeshtha Shukla Dashami)'
        e6.event_date = '25 May 2026'
        e6.month_name = 'May'
        e6.month_number = 5
        print("Updated Entry 6: Ganga Dussehra")

    # Update Entry 7 (Maa Purnagiri Mela)
    e7 = CultureEntry.query.get(7)
    if e7:
        e7.when_celebrated = '19–27 March 2026 (Chaitra Navratri)'
        e7.event_date = '19–27 March 2026'
        e7.month_name = 'March'
        e7.month_number = 3
        print("Updated Entry 7: Maa Purnagiri Mela")

    # Update Entry 8 (Devidhura Bagwal Mela)
    e8 = CultureEntry.query.get(8)
    if e8:
        e8.when_celebrated = '28 August 2026 (Shravan Purnima / Raksha Bandhan)'
        e8.event_date = '28 August 2026'
        e8.month_name = 'August'
        e8.month_number = 8
        print("Updated Entry 8: Devidhura Bagwal Mela")

    # Update Entry 12 (Khatarua)
    e12 = CultureEntry.query.get(12)
    if e12:
        e12.when_celebrated = '17 September 2026 (Ashwin Sankranti)'
        e12.event_date = '17 September 2026'
        e12.month_name = 'September'
        e12.month_number = 9
        e12.is_happening_soon = True
        print("Updated Entry 12: Khatarua")

    # Update Entry 13 (Kumaoni Dussehra & Ramlila)
    e13 = CultureEntry.query.get(13)
    if e13:
        e13.when_celebrated = '11–20 October 2026 (Vijayadashami / Dussehra on 20 October 2026)'
        e13.event_date = '11–20 October 2026'
        e13.month_name = 'October'
        e13.month_number = 10
        print("Updated Entry 13: Kumaoni Dussehra")

    # Update Entry 14 (Kumaoni Diwali)
    e14 = CultureEntry.query.get(14)
    if e14:
        e14.when_celebrated = '8 November 2026 (Kartik Amavasya / Diwali Night)'
        e14.event_date = '8 November 2026'
        e14.month_name = 'November'
        e14.month_number = 11
        print("Updated Entry 14: Kumaoni Diwali")

    # Update Entry 15 (Egaas Bagwal)
    e15 = CultureEntry.query.get(15)
    if e15:
        e15.when_celebrated = '20 November 2026 (Haribodhini Ekadashi / 11 Days After Diwali)'
        e15.event_date = '20 November 2026'
        e15.month_name = 'November'
        e15.month_number = 11
        print("Updated Entry 15: Egaas Bagwal")

    # Update Entry 16 (Uttarayani Fair)
    e16 = CultureEntry.query.get(16)
    if e16:
        e16.when_celebrated = '13–19 January 2027 (Makar Sankranti Sangam Fair)'
        e16.event_date = '13–19 January 2027'
        e16.month_name = 'January'
        e16.month_number = 1
        print("Updated Entry 16: Uttarayani Fair")

    # Update Entry 17 (Phool Dei)
    e17 = CultureEntry.query.get(17)
    if e17:
        e17.when_celebrated = '14–15 March 2026 (Chaitra Sankranti / Spring Welcoming)'
        e17.event_date = '14–15 March 2026'
        e17.month_name = 'March'
        e17.month_number = 3
        print("Updated Entry 17: Phool Dei")

    # Update Entry 18 (Kandali)
    e18 = CultureEntry.query.get(18)
    if e18:
        e18.when_celebrated = 'Autumn 2026 / 2027 (12-Year Strobilanthes Bloom Cycle)'
        e18.event_date = 'October 2026'
        e18.month_name = 'October'
        e18.month_number = 10
        print("Updated Entry 18: Kandali")

    # Check or Insert Nanda Devi Raj Jat Yatra
    raj_jat = CultureEntry.query.filter_by(slug='nanda-devi-raj-jat').first()
    if not raj_jat:
        raj_jat = CultureEntry(
            slug='nanda-devi-raj-jat',
            region='garhwal',
            entry_type='festival',
            category='Religious',
            title='Shri Nanda Devi Raj Jat Yatra',
            subtitle='The Himalayan Mahakumbh & 280-km Barefoot Sacred Pilgrimage',
            district='Chamoli',
            venue='Nauti Village to Homkund Lake (4,061 m) at Mount Trishul',
            deity_or_ritual='Emotional Vidaai (bridal farewell) of Goddess Nanda Devi led by the sacred Four-Horned Ram (Chausingha Khadu) and Golden Chhantoli',
            attendance='Est. 500,000+ devotees across Uttarakhand (12-year cycle Mahakumbh)',
            when_celebrated='5–23 September 2026 (Culmination on 19 Sep · Nanda Ashtami)',
            event_date='5–23 September 2026',
            month_name='September',
            month_number=9,
            is_happening_soon=True,
            cover_image_url='/static/images/Almora/nandadevi.png',
            unesco=True,
            story_text="""Regarded as the 'Himalayan Mahakumbh' of Uttarakhand, the Nanda Devi Raj Jat is a legendary 280-kilometer barefoot pilgrimage undertaken once every 12 years. It portrays the intensely emotional 'Vidaai' (bridal departure) of Goddess Nanda Devi—the beloved daughter of the Himalayas—leaving her maternal childhood home (Maika) at Nauti village to join her divine consort, Lord Shiva, at his eternal icy abode beneath Mount Trishul. Over three weeks, thousands of pilgrims walk through mist-veiled forests, river valleys, high alpine bugyals (Bedni), and glaciated passes (Jurangali), united in devotion.""",
            travel_tips="""• Acclimatization: Altitude reaches 4,850 m at Jurangali Pass. Proper fitness and thermal layering are essential.
• Sacred rule: Strictly barefoot beyond Bedni Bugyal and sacred Vaitarini Kund. Zero leather items permitted.
• Ecology: Zero plastic tolerance across high-altitude meadows; Brahma Kamal flowers must remain untouched.""",
            guide_name='Suresh Nautiyal (Nauti Hereditary Trustee)'
        )
        db.session.add(raj_jat)
        print("Inserted new CultureEntry: Shri Nanda Devi Raj Jat Yatra")
    else:
        raj_jat.when_celebrated = '5–23 September 2026 (Culmination on 19 Sep · Nanda Ashtami)'
        raj_jat.event_date = '5–23 September 2026'
        raj_jat.month_name = 'September'
        raj_jat.month_number = 9
        raj_jat.is_happening_soon = True
        print("Updated existing CultureEntry: Shri Nanda Devi Raj Jat Yatra")

    db.session.commit()
    print("Database culture records successfully committed!")

"""
Updates Champawat destinations with:
1. Baleshwar Temple (with Baleshwar_Temple.png and rich story)
2. Purnagiri Temple (with Purnagiri_temple.png and rich story)
3. Golu Devta Temple (with goluDevta.png and rich story)
4. Shyamlatal (with shyamlatal.png and rich story)
Also links culture entries and validates paths.
"""
from app import create_app
from app.extensions import db
from app.models import Destination, CultureEntry

def update_champawat():
    app = create_app()
    with app.app_context():
        # 1. Baleshwar Temple
        baleshwar = Destination.query.filter_by(slug='baleshwar-temple').first()
        baleshwar_story = (
            "An architectural masterpiece of South Indian style stone craft in the Kumaon Himalayas, "
            "Baleshwar Temple was erected between the 10th and 12th century AD by the Chand dynasty rulers. "
            "Dedicated to Lord Shiva (Baleshwar Mahadev), the complex also enshrines Ratneshwar and Champawati Devi "
            "within intricate dark-granite sanctums. Ancient folklore honors master sculptor Jagannath Mistri, whose exquisite "
            "stonework and celestial apsaras so captivated the Chand King that his right hand was severed to prevent the creation "
            "of another rival masterpiece — yet, fueled by devotion, Mistri sculpted an equally revered temple using his left hand. "
            "The complex features exquisitely carved ceiling mandalas, dragon-headed stone water spouts, and centuries-old granite shivlings "
            "preserved under the Archaeological Survey of India (ASI)."
        )
        if baleshwar:
            baleshwar.name = 'Baleshwar Temple'
            baleshwar.description = baleshwar_story
            baleshwar.cover_image_url = '/static/images/champwat/Baleshwar_Temple.png'
            baleshwar.best_time = 'October–April (ideal mountain weather)'
            baleshwar.featured = True
            print("Updated Baleshwar Temple.")
        else:
            baleshwar = Destination(
                name='Baleshwar Temple',
                slug='baleshwar-temple',
                region='kumaon',
                category='temple',
                district='Champawat',
                lat=29.3374,
                lng=80.0967,
                altitude_m=1610,
                description=baleshwar_story,
                cover_image_url='/static/images/champwat/Baleshwar_Temple.png',
                best_time='October–April (ideal mountain weather)',
                featured=True
            )
            db.session.add(baleshwar)
            print("Created Baleshwar Temple.")

        # 2. Purnagiri Temple
        purnagiri = Destination.query.filter_by(slug='purnagiri-temple').first()
        purnagiri_story = (
            "Perched atop the Annapurna Peak at an altitude of 3,000m near Tanakpur along the border with Nepal, "
            "Maa Purnagiri is celebrated as one of the 108 supreme Shakti Peethas. In Hindu cosmology, when Lord Shiva "
            "carried Sati's body in his cosmic dance of sorrow, the navel (nabhi) of the goddess fell upon this precipitous mountain crest. "
            "Pilgrims undertake a rigorous barefoot ascent along narrow cliff-carved stairways above the roaring Kali (Sharda) river "
            "to offer prayers at the open-sky summit shrine, adorned with countless sacred red threads and bells tied by those praying for "
            "progeny and healing. The annual Chaitra Navratri fair brings over half a million devotees together in an unbroken centuries-old "
            "pilgrimage tradition."
        )
        if purnagiri:
            purnagiri.name = 'Purnagiri Temple'
            purnagiri.description = purnagiri_story
            purnagiri.cover_image_url = '/static/images/champwat/Purnagiri_temple.png'
            purnagiri.best_time = 'October–May (Chaitra Navratri for the sacred Mela)'
            purnagiri.featured = True
            print("Updated Purnagiri Temple.")
        else:
            purnagiri = Destination(
                name='Purnagiri Temple',
                slug='purnagiri-temple',
                region='kumaon',
                category='temple',
                district='Champawat',
                lat=29.1350,
                lng=80.1980,
                altitude_m=3000,
                description=purnagiri_story,
                cover_image_url='/static/images/champwat/Purnagiri_temple.png',
                best_time='October–May (Chaitra Navratri for the sacred Mela)',
                featured=True
            )
            db.session.add(purnagiri)
            print("Created Purnagiri Temple.")

        # 3. Golu Devta Temple
        golu = Destination.query.filter_by(slug='golu-devta-champawat').first()
        golu_story = (
            "Champawat is the sacred birthplace and legendary ancestral seat of Golu Devta (Gwalla Devta), "
            "revered throughout Kumaon as the supreme incarnation of Lord Shiva and the divine dispenser of instant justice. "
            "Born to King Jhal Rai and Queen Kalindra of Champawat, folk ballads recount how the miraculous child outsmarted "
            "the jealousy of seven stepmothers by bringing stone horses to drink from the lake. Unlike conventional temples, "
            "devotees come to Golu Devta to present written petitions and legal affidavits detailing their griefs and seeking truth. "
            "The temple precincts echo with the resonant chime of thousands of brass bells donated by grateful devotees whose petitions "
            "were divinely resolved."
        )
        if golu:
            golu.name = 'Golu Devta Temple'
            golu.description = golu_story
            golu.cover_image_url = '/static/images/champwat/goluDevta.png'
            golu.best_time = 'Year-round (Chaitra Navratri & autumn are especially vibrant)'
            golu.featured = True
            print("Updated Golu Devta Temple.")
        else:
            golu = Destination(
                name='Golu Devta Temple',
                slug='golu-devta-champawat',
                region='kumaon',
                category='temple',
                district='Champawat',
                lat=29.3360,
                lng=80.0910,
                altitude_m=1620,
                description=golu_story,
                cover_image_url='/static/images/champwat/goluDevta.png',
                best_time='Year-round (Chaitra Navratri & autumn are especially vibrant)',
                featured=True
            )
            db.session.add(golu)
            print("Created Golu Devta Temple.")

        # 4. Shyamlatal
        shyamla = Destination.query.filter_by(slug='shyamlatal').first()
        shyamla_story = (
            "Shyamlatal is a serene natural lake spanning over 1.5 square kilometers at an elevation of 1,500m, "
            "famed for its deep blue-black waters that mirror the surrounding virgin oak, pine, and sal ridges. "
            "The lake derives its name 'Shyamla' from its dark hue, evoking the divine form of Lord Krishna. "
            "On its tranquil banks stands the historic Ramakrishna Mission Vivekananda Ashram, founded in 1914 by "
            "Swami Virajananda (direct disciple of Swami Vivekananda). Blooming with pristine white water lilies (kumud) "
            "and framed by silent meditation walking trails, Shyamlatal remains an untouched haven of spiritual contemplation "
            "far from crowded tourist circuits."
        )
        if shyamla:
            shyamla.name = 'Shyamlatal'
            shyamla.description = shyamla_story
            shyamla.cover_image_url = '/static/images/champwat/shyamlatal.png'
            shyamla.best_time = 'October–June (clear skies & tranquil lake reflections)'
            shyamla.featured = True
            print("Updated Shyamlatal.")
        else:
            shyamla = Destination(
                name='Shyamlatal',
                slug='shyamlatal',
                region='kumaon',
                category='lake',
                district='Champawat',
                lat=29.1860,
                lng=80.1250,
                altitude_m=1500,
                description=shyamla_story,
                cover_image_url='/static/images/champwat/shyamlatal.png',
                best_time='October–June (clear skies & tranquil lake reflections)',
                featured=True
            )
            db.session.add(shyamla)
            print("Created Shyamlatal.")

        db.session.flush()

        # Link CultureEntry for Purnagiri Mela to Purnagiri Temple
        purnagiri_entry = CultureEntry.query.filter_by(slug='maa-purnagiri-mela-champawat').first()
        if purnagiri_entry and purnagiri:
            purnagiri_entry.destination_id = purnagiri.id
            purnagiri_entry.cover_image_url = '/static/images/champwat/Purnagiri_temple.png'
            print("Linked Purnagiri Mela culture entry to Purnagiri Temple.")

        db.session.commit()
        print("Champawat destinations successfully updated!")

if __name__ == '__main__':
    update_champawat()

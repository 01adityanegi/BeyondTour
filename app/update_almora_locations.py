"""
Updates Almora destinations and culture entries with user-provided images:
1. Almora Heritage Town (almora.png)
2. Jageshwar Dham (jagwasher.png)
3. Kasar Devi Temple (kashardevi.png)
4. Chitai Golu Devta Temple (goludevtachatai.png)
5. Nanda Devi Temple Almora (nandadevi.png)
6. Vriddha Jageshwar Temple (virdhjageshwar.png)
7. Dandeshwar Temple (dhadeshwar.png)
8. Kalbisht Devta Temple (kalbistgoludevta.png)
Also updates Culture entries: Nanda Devi Fair Almora and Jageshwar Monsoon Festival.
"""
from app import create_app
from app.extensions import db
from app.models import Destination, CultureEntry

def update_almora():
    app = create_app()
    with app.app_context():
        # 1. Almora Heritage Town (id=2, slug='almora')
        almora_town = Destination.query.filter_by(slug='almora').first()
        almora_story = (
            "The cultural capital of Kumaon, founded in 1563 by King Kalyan Chand of the Chand dynasty on a "
            "horse-saddle shaped ridge between the Kosi and Suyal rivers. Almora is famed for its 200-year-old "
            "cobblestone pedestrian Lala Bazaar, its unbroken legacy of ritual Aipan art, the famed golden Bal Mithai "
            "made with roasted khoya and sugar beads, and its deep spiritual aura where Swami Vivekananda, Rabindranath "
            "Tagore, and Uday Shankar established their artistic and philosophical sanctuaries overlooking the Himalayan peaks."
        )
        if almora_town:
            almora_town.name = 'Almora Heritage Town'
            almora_town.description = almora_story
            almora_town.cover_image_url = '/static/images/Almora/almora.png'
            almora_town.best_time = 'Year-round (March–May for blooms, Sep–Nov for clear mountain views)'
            almora_town.featured = True
            print("Updated Almora Heritage Town.")
        else:
            almora_town = Destination(
                name='Almora Heritage Town',
                slug='almora',
                region='kumaon',
                category='heritage',
                district='Almora',
                lat=29.5969,
                lng=79.6538,
                altitude_m=1604,
                description=almora_story,
                cover_image_url='/static/images/Almora/almora.png',
                best_time='Year-round (March–May for blooms, Sep–Nov for clear mountain views)',
                featured=True
            )
            db.session.add(almora_town)
            print("Created Almora Heritage Town.")

        # 2. Jageshwar Dham (id=4, slug='jageshwar')
        jageshwar = Destination.query.filter_by(slug='jageshwar').first()
        jageshwar_story = (
            "Cradled in a mystical valley along the sacred Jata Ganga river amidst a protected forest of towering "
            "deodar cedars, Jageshwar Dham is a cluster of 124 stone temples dating from the 7th to the 14th century CE, "
            "built by the Katyuri and Chand kings. Revered as one of the twelve sacred Jyotirlingas (Nagesh Darukavane), "
            "the sanctum houses the self-manifested Shiva lingam. At dawn, as mountain mist weaves through the ancient "
            "deodars and temple bells echo through stone mandapas, Jageshwar radiates an aura of primordial sanctity."
        )
        if jageshwar:
            jageshwar.name = 'Jageshwar Dham'
            jageshwar.description = jageshwar_story
            jageshwar.cover_image_url = '/static/images/Almora/jagwasher.png'
            jageshwar.best_time = 'March–June, September–November (Shravan month for Monsoon Festival)'
            jageshwar.featured = True
            print("Updated Jageshwar Dham.")
        else:
            jageshwar = Destination(
                name='Jageshwar Dham',
                slug='jageshwar',
                region='kumaon',
                category='temple',
                district='Almora',
                lat=29.6381,
                lng=79.8536,
                altitude_m=1870,
                description=jageshwar_story,
                cover_image_url='/static/images/Almora/jagwasher.png',
                best_time='March–June, September–November (Shravan month for Monsoon Festival)',
                featured=True
            )
            db.session.add(jageshwar)
            print("Created Jageshwar Dham.")

        # 3. Kasar Devi Temple
        kasar_devi = Destination.query.filter_by(slug='kasar-devi-temple').first()
        kasar_story = (
            "Perched atop Crank's Ridge with sweeping vistas of Trishul, Nanda Devi, and Panchachuli, the 2nd-century CE "
            "Kasar Devi Temple is situated on the Earth's Van Allen radiation belt, possessing a rare geomagnetic field "
            "similar to Stonehenge and Machu Picchu that fosters profound meditative calm. The temple became a global beacon "
            "of transcendental consciousness when Swami Vivekananda meditated here in 1890, followed by Lama Anagarika Govinda, "
            "Walter Evans-Wentz, Beat poet Allen Ginsberg, and music legends Bob Dylan and George Harrison."
        )
        if kasar_devi:
            kasar_devi.name = 'Kasar Devi Temple'
            kasar_devi.description = kasar_story
            kasar_devi.cover_image_url = '/static/images/Almora/kashardevi.png'
            kasar_devi.best_time = 'Year-round (Kartik Poornima for Kasar Devi Mela; clear winter sunsets)'
            kasar_devi.featured = True
            print("Updated Kasar Devi Temple.")
        else:
            kasar_devi = Destination(
                name='Kasar Devi Temple',
                slug='kasar-devi-temple',
                region='kumaon',
                category='temple',
                district='Almora',
                lat=29.6384,
                lng=79.6738,
                altitude_m=2116,
                description=kasar_story,
                cover_image_url='/static/images/Almora/kashardevi.png',
                best_time='Year-round (Kartik Poornima for Kasar Devi Mela; clear winter sunsets)',
                featured=True
            )
            db.session.add(kasar_devi)
            print("Created Kasar Devi Temple.")

        # 4. Chitai Golu Devta Temple
        chitai_golu = Destination.query.filter_by(slug='chitai-golu-devta-temple').first()
        chitai_story = (
            "Located 8 km from Almora, Chitai is the foremost temple of Golu Devta, venerated across Kumaon as the God of "
            "Justice (Nyay ke Devta) and an incarnation of Lord Shiva. The temple grounds are an extraordinary spectacle, "
            "draped with tens of thousands of ringing brass bells hung by devotees whose prayers were granted. Pilgrims travel "
            "from across the Himalayas to submit handwritten petitions on stamp papers and postcards, seeking divine justice "
            "before the beloved deity who rides a white horse brandishing a bow and arrow."
        )
        if chitai_golu:
            chitai_golu.name = 'Chitai Golu Devta Temple'
            chitai_golu.description = chitai_story
            chitai_golu.cover_image_url = '/static/images/Almora/goludevtachatai.png'
            chitai_golu.best_time = 'Year-round (festive mornings and Navratri)'
            chitai_golu.featured = True
            print("Updated Chitai Golu Devta Temple.")
        else:
            chitai_golu = Destination(
                name='Chitai Golu Devta Temple',
                slug='chitai-golu-devta-temple',
                region='kumaon',
                category='temple',
                district='Almora',
                lat=29.6056,
                lng=79.6978,
                altitude_m=1800,
                description=chitai_story,
                cover_image_url='/static/images/Almora/goludevtachatai.png',
                best_time='Year-round (festive mornings and Navratri)',
                featured=True
            )
            db.session.add(chitai_golu)
            print("Created Chitai Golu Devta Temple.")

        # 5. Nanda Devi Temple, Almora
        nanda_devi = Destination.query.filter_by(slug='nanda-devi-temple-almora').first()
        nanda_story = (
            "Enshrined in the heart of Almora within the historic stone complex of Lala Bazaar, this revered shrine is dedicated "
            "to Goddess Nanda Devi, the guardian deity of the Chand dynasty and Kumaon. King Kalyan Chand originally established her "
            "worship in the royal palace at Malla Mahal in the 16th century. Every September during Bhadrapad Ashtami, the temple hosts "
            "the historic Almora Nanda Devi Fair, where twin murtis of Nanda and Sunanda are sculpted from banana trunks and paraded "
            "through ancient stone-paved lanes amid celebratory Jhora and Chanchari folk dances."
        )
        if nanda_devi:
            nanda_devi.name = 'Nanda Devi Temple, Almora'
            nanda_devi.description = nanda_story
            nanda_devi.cover_image_url = '/static/images/Almora/nandadevi.png'
            nanda_devi.best_time = 'Year-round (Bhadrapad Ashtami in September for Nanda Devi Fair)'
            nanda_devi.featured = True
            print("Updated Nanda Devi Temple, Almora.")
        else:
            nanda_devi = Destination(
                name='Nanda Devi Temple, Almora',
                slug='nanda-devi-temple-almora',
                region='kumaon',
                category='temple',
                district='Almora',
                lat=29.5985,
                lng=79.6590,
                altitude_m=1640,
                description=nanda_story,
                cover_image_url='/static/images/Almora/nandadevi.png',
                best_time='Year-round (Bhadrapad Ashtami in September for Nanda Devi Fair)',
                featured=True
            )
            db.session.add(nanda_devi)
            print("Created Nanda Devi Temple, Almora.")

        # 6. Vriddha Jageshwar Temple
        vridh_jageshwar = Destination.query.filter_by(slug='vriddha-jageshwar').first()
        vridh_story = (
            "Perched on a high Himalayan ridge 3 km above Jageshwar Dham at an altitude of 2,200 meters, Vriddha Jageshwar "
            "('Old Jageshwar') is believed to be the original site where Lord Shiva meditated as an ascetic sage before descending "
            "into the valley. Reached via a picturesque road or a walking trail through dense oak, pine, and rhododendron forests, "
            "this peaceful hilltop shrine provides an unhindered, spellbinding panoramic view of the Great Himalayan range—including "
            "Trishul, Nanda Devi, Nanda Kot, and the Panchachuli peaks."
        )
        if vridh_jageshwar:
            vridh_jageshwar.name = 'Vriddha Jageshwar Temple'
            vridh_jageshwar.description = vridh_story
            vridh_jageshwar.cover_image_url = '/static/images/Almora/virdhjageshwar.png'
            vridh_jageshwar.best_time = 'October–June (sunrise hours for crystalline Himalayan panorama)'
            vridh_jageshwar.featured = True
            print("Updated Vriddha Jageshwar Temple.")
        else:
            vridh_jageshwar = Destination(
                name='Vriddha Jageshwar Temple',
                slug='vriddha-jageshwar',
                region='kumaon',
                category='temple',
                district='Almora',
                lat=29.6450,
                lng=79.8600,
                altitude_m=2200,
                description=vridh_story,
                cover_image_url='/static/images/Almora/virdhjageshwar.png',
                best_time='October–June (sunrise hours for crystalline Himalayan panorama)',
                featured=True
            )
            db.session.add(vridh_jageshwar)
            print("Created Vriddha Jageshwar Temple.")

        # 7. Dandeshwar Temple (Dhadeshwar)
        dandeshwar = Destination.query.filter_by(slug='dandeshwar-temple').first()
        dandeshwar_story = (
            "Situated just one kilometer upstream of Jageshwar Dham along the banks of the Jata Ganga, Dandeshwar Temple is the "
            "largest and most architecturally imposing stone temple in the entire Jageshwar valley. Erected during the Katyuri era, "
            "the sanctum features an enormous natural rock boulder venerated as Lord Shiva carrying a staff (Danda). Surrounded by "
            "eighteen smaller satellite shrines standing serenely among whispering deodar trees, Dandeshwar is protected by the "
            "Archaeological Survey of India as a masterpiece of ancient northern Indian stone masonry."
        )
        if dandeshwar:
            dandeshwar.name = 'Dandeshwar Temple (Dhadeshwar)'
            dandeshwar.description = dandeshwar_story
            dandeshwar.cover_image_url = '/static/images/Almora/dhadeshwar.png'
            dandeshwar.best_time = 'March–June, September–November'
            dandeshwar.featured = True
            print("Updated Dandeshwar Temple.")
        else:
            dandeshwar = Destination(
                name='Dandeshwar Temple (Dhadeshwar)',
                slug='dandeshwar-temple',
                region='kumaon',
                category='temple',
                district='Almora',
                lat=29.6330,
                lng=79.8450,
                altitude_m=1800,
                description=dandeshwar_story,
                cover_image_url='/static/images/Almora/dhadeshwar.png',
                best_time='March–June, September–November',
                featured=True
            )
            db.session.add(dandeshwar)
            print("Created Dandeshwar Temple.")

        # 8. Kalbisht Devta Temple
        kalbisht = Destination.query.filter_by(slug='kalbisht-devta-temple').first()
        kalbisht_story = (
            "Revered with profound devotion across the hills of Kumaon, Kalbisht Devta is an ancient pastoral protector and folk deity "
            "celebrated alongside Golu Devta as a defender of the helpless. In Kumaoni folk folklore, Kalbisht Baba was a flute-playing "
            "protector of cows, farmers, and mountain pastures who healed afflicted livestock. Following his betrayal by feudal landlords, "
            "his spirit became an eternal guardian of mountain livestock and village justice. Devotees visit this pine-sheltered shrine to "
            "offer fresh milk, copper bells, and iron tridents, seeking blessings for their livestock and peace in their homes."
        )
        if kalbisht:
            kalbisht.name = 'Kalbisht Devta Temple'
            kalbisht.description = kalbisht_story
            kalbisht.cover_image_url = '/static/images/Almora/kalbistgoludevta.png'
            kalbisht.best_time = 'Year-round (mornings and annual community bhandaras)'
            kalbisht.featured = True
            print("Updated Kalbisht Devta Temple.")
        else:
            kalbisht = Destination(
                name='Kalbisht Devta Temple',
                slug='kalbisht-devta-temple',
                region='kumaon',
                category='temple',
                district='Almora',
                lat=29.6800,
                lng=79.7200,
                altitude_m=1950,
                description=kalbisht_story,
                cover_image_url='/static/images/Almora/kalbistgoludevta.png',
                best_time='Year-round (mornings and annual community bhandaras)',
                featured=True
            )
            db.session.add(kalbisht)
            print("Created Kalbisht Devta Temple.")

        db.session.flush()

        # Update Culture Entries for Almora
        nanda_fair = CultureEntry.query.filter_by(slug='nanda-devi-fair-almora').first()
        if nanda_fair:
            nanda_fair.cover_image_url = '/static/images/Almora/nandadevi.png'
            if nanda_devi:
                nanda_fair.destination_id = nanda_devi.id
            print("Updated Nanda Devi Fair Almora culture entry image and destination link.")

        jageshwar_fest = CultureEntry.query.filter_by(slug='jageshwar-monsoon-festival').first()
        if jageshwar_fest:
            jageshwar_fest.cover_image_url = '/static/images/Almora/jagwasher.png'
            if jageshwar:
                jageshwar_fest.destination_id = jageshwar.id
            print("Updated Jageshwar Monsoon Festival culture entry image and destination link.")

        db.session.commit()
        print("Almora destinations and culture entries successfully updated!")

if __name__ == '__main__':
    update_almora()

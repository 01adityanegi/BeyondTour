"""
Seed script — populates the Beyond Tour database with authentic Uttarakhand data.
Run with: python -m app.seed_data  (from the project root)
"""
import sys
import os
import json
from datetime import date, datetime

sys.path.insert(0, os.path.abspath(os.path.dirname(os.path.dirname(__file__))))

from app import create_app
from app.extensions import db
from app.models import (
    User, Destination, CultureEntry, FoodItem, Hotel, Guide,
    Trip, Review, Wishlist, CommunityPost, Comment, Booking
)


def seed():
    app = create_app()
    with app.app_context():
        # Cleanly recreate database schema
        db.drop_all()
        db.create_all()

        # -----------------------------------------------------------
        # Users
        # -----------------------------------------------------------
        admin = User(
            name='Beyond Tour Admin',
            email='admin@beyondtour.in',
            role='admin',
            auth_provider='local',
            email_verified=True,
            home_city='Dehradun',
            bio='Overseeing the Beyond Tour cultural preservation platform.',
            interests='["heritage", "culture", "wildlife"]'
        )
        admin.set_password('admin@123')

        traveler = User(
            name='Priya Sharma',
            email='priya@example.com',
            role='tourist',
            auth_provider='local',
            email_verified=True,
            home_city='New Delhi',
            bio='Slow traveler, photographer, and lover of mountain stories.',
            interests='["trekking", "food", "photography", "culture"]'
        )
        traveler.set_password('password123')

        traveler2 = User(
            name='Arjun Mehta',
            email='arjun.mehta@example.com',
            role='tourist',
            auth_provider='local',
            email_verified=True,
            home_city='Bengaluru',
            bio='Alpine trekker, wilderness camper, and high-altitude photography enthusiast.',
            interests='["trekking", "wildlife", "photography"]'
        )
        traveler2.set_password('password123')

        traveler3 = User(
            name='Sneha Rawat',
            email='sneha.rawat@example.com',
            role='tourist',
            auth_provider='local',
            email_verified=True,
            home_city='Dehradun',
            bio='Cultural researcher and Kumaoni traditional cuisine chronicler.',
            interests='["culture", "food", "homestays"]'
        )
        traveler3.set_password('password123')

        traveler4 = User(
            name='Dr. Rajesh Mukhopadhyay',
            email='rajesh.m@example.com',
            role='tourist',
            auth_provider='local',
            email_verified=True,
            home_city='Kolkata',
            bio='Botanist, avid birdwatcher, and Himalayan heritage traveler.',
            interests='["temples", "culture", "wildlife"]'
        )
        traveler4.set_password('password123')

        traveler5 = User(
            name='Ananya Nair',
            email='ananya.nair@example.com',
            role='tourist',
            auth_provider='local',
            email_verified=True,
            home_city='Mumbai',
            bio='Solo traveler seeking quiet Himalayan villages and meditation trails.',
            interests='["spiritual", "homestays", "culture"]'
        )
        traveler5.set_password('password123')

        host = User(
            name='Gopal Bhandari',
            email='gopal@example.com',
            role='business',
            auth_provider='local',
            email_verified=True,
            home_city='Almora',
            bio='Kumaoni farmer and homestay host preserving authentic Aipan art and regional recipes.',
            interests='["culture", "food", "homestays"]'
        )
        host.set_password('password123')

        db.session.add_all([admin, traveler, traveler2, traveler3, traveler4, traveler5, host])
        db.session.flush()

        # -----------------------------------------------------------
        # Destinations — Kumaon & Garhwal
        # -----------------------------------------------------------
        destinations = [
            Destination(
                name='Naini Lake', slug='nainital', region='kumaon', category='lake',
                district='Nainital', lat=29.3919, lng=79.4542, altitude_m=2084,
                description='The jewel of Kumaon and the sacred heart of the hill station, Naini Lake is a natural crescent-shaped freshwater lake cradled at 2,084m by seven majestic peaks (Sapta-Shring). In sacred Hindu mythology recorded in the Skanda Purana, the waterbody was known as \'Tririshi Sarovar\'—carved by the great sages Atri, Pulastya, and Pulaha, who channeled sacred waters from Mount Kailash\'s holy Lake Mansarovar. It is also celebrated as the divine spot where Goddess Sati\'s left eye (Naina) fell as Lord Shiva danced in cosmic grief. Divided into Mallital (northern head) and Tallital (southern foot), the emerald waters mirror the floating silhouettes of heritage yachts, colorful wooden paddleboats, and mist-veiled cedar ridges.',
                cover_image_url='/static/images/Nanital/lakenanital.png',
                best_time='March–June, September–November', featured=True
            ),
            Destination(
                name='Naina Devi Temple', slug='naina-devi-temple', region='kumaon', category='temple',
                district='Nainital', lat=29.3950, lng=79.4510, altitude_m=2088,
                description='Standing venerated on the northern edge of Naini Lake at the Flatts, the sacred Naina Devi Temple is one of the revered Shakti Peethas of northern India. The sanctum sanctorum houses two divine eyes representing Goddess Naina Devi (Maa Durga), flanked by the fierce form of Maa Kali and Lord Ganesha. Following a tragic landslide in 1880 that swept away the ancient shrine, devout townspeople and hill communities rebuilt the present temple structure in 1883 with deep reverence. Every autumn during Bhadrapad Ashtami, the temple hosts the historic Nanda Devi Mela, where towering banana-trunk idols are paraded through lakeside lanes accompanied by the rhythmic clatter of Chholiya swords and conch shells before sacred ritual immersion into the lake.',
                cover_image_url='/static/images/Nanital/NainaDeviTemple.png',
                best_time='Year-round (Bhadrapad Ashtami for Nanda Devi Mela)', featured=True
            ),
            Destination(
                name='Mall Road Nainital', slug='mall-road-nainital', region='kumaon', category='heritage',
                district='Nainital', lat=29.3900, lng=79.4580, altitude_m=2080,
                description='Constructed during British colonial rule in the mid-19th century, Mall Road—officially named Govind Ballabh Pant Marg—is the vibrant pedestrian artery connecting Tallital and Mallital along the tranquil shoreline of Naini Lake. Flanked by colonial-era lampposts, ornate wooden eaves, and lakefront benches, the promenade buzzes with mountain life. Visitors stroll past heritage bakeries like Sakley\'s, local wool markets offering hand-woven Pashminas, artisanal candle workshops renowned for aromatic hand-carved pillars, and traditional dhabas serving hot Pahadi Aloo ke Gutke. In the evening, traffic is halted to allow pedestrians to watch the twilight reflections of lakeside cottages glimmering over the darkening lake.',
                cover_image_url='/static/images/Nanital/Mallroad.png',
                best_time='Year-round (evenings for leisurely lakeside strolls)', featured=True
            ),
            Destination(
                name='Naini Peak (China Peak)', slug='naini-peak', region='kumaon', category='trek',
                district='Nainital', lat=29.4167, lng=79.4500, altitude_m=2615,
                description='Perched at a commanding elevation of 2,615 meters (8,579 ft), Naini Peak—historically known as Cheena Peak—is the highest summit in the Nainital hills. The rewarding 6-kilometer trail winds through canopies of Himalayan cypress, oak, deodar cedar, and blooming red rhododendrons, alive with the calls of kalij pheasants and Himalayan black-throated jays. At the summit, hikers are greeted with a panoramic 360-degree vista: looking north across a 300-kilometer horizon of snowcapped Himalayan giants from Bandarpoonch to Nanda Devi and Trishul, and looking south onto the entire jewel-like emerald basin of Naini Lake nestled far below in the valley.',
                cover_image_url='/static/images/Nanital/Naini_Peak.png',
                best_time='October–June (morning hours for crystalline Himalayan views)', featured=True
            ),
            Destination(
                name='Tiffin Top (Dorothy\'s Seat)', slug='tiffin-top', region='kumaon', category='trek',
                district='Nainital', lat=29.3833, lng=79.4417, altitude_m=2292,
                description='Located atop the Ayarpatta hill at an altitude of 2,292 meters (7,520 ft), Tiffin Top is celebrated as one of Nainital\'s most scenic picnic knolls and tranquil forest viewpoints. At its summit stands \'Dorothy\'s Seat\'—a stone memorial masonry bench erected by British officer Col. J.P. Kellett in memory of his artist wife Dorothy Kellett, who spent days painting the mountain landscapes from this cliffside knoll. The 4 km trek from the town center winds through moss-draped deodar woods and terraced farmland, opening up onto majestic panoramic vistas of the Kumaon countryside, Nainital valley, and distant snow peaks glistening under the mountain sun.',
                cover_image_url='/static/images/Nanital/Tiffin_Top.png',
                best_time='March–June, September–November', featured=True
            ),
            Destination(
                name='Almora Heritage Town', slug='almora', region='kumaon', category='heritage',
                district='Almora', lat=29.5969, lng=79.6538, altitude_m=1604,
                description='The cultural capital of Kumaon, founded in 1563 by King Kalyan Chand of the Chand dynasty on a horse-saddle shaped ridge between the Kosi and Suyal rivers. Almora is famed for its 200-year-old cobblestone pedestrian Lala Bazaar, its unbroken legacy of ritual Aipan art, the famed golden Bal Mithai made with roasted khoya and sugar beads, and its deep spiritual aura where Swami Vivekananda, Rabindranath Tagore, and Uday Shankar established their artistic and philosophical sanctuaries overlooking the Himalayan peaks.',
                cover_image_url='/static/images/Almora/almora.png',
                best_time='Year-round (March–May for blooms, Sep–Nov for clear mountain views)', featured=True
            ),
            Destination(
                name='Jageshwar Dham', slug='jageshwar', region='kumaon', category='temple',
                district='Almora', lat=29.6381, lng=79.8536, altitude_m=1870,
                description='Cradled in a mystical valley along the sacred Jata Ganga river amidst a protected forest of towering deodar cedars, Jageshwar Dham is a cluster of 124 stone temples dating from the 7th to the 14th century CE, built by the Katyuri and Chand kings. Revered as one of the twelve sacred Jyotirlingas (Nagesh Darukavane), the sanctum houses the self-manifested Shiva lingam. At dawn, as mountain mist weaves through the ancient deodars and temple bells echo through stone mandapas, Jageshwar radiates an aura of primordial sanctity.',
                cover_image_url='/static/images/Almora/jagwasher.png',
                best_time='March–June, September–November (Shravan month for Monsoon Festival)', featured=True
            ),
            Destination(
                name='Kasar Devi Temple', slug='kasar-devi-temple', region='kumaon', category='temple',
                district='Almora', lat=29.6384, lng=79.6738, altitude_m=2116,
                description='Perched atop Crank\'s Ridge with sweeping vistas of Trishul, Nanda Devi, and Panchachuli, the 2nd-century CE Kasar Devi Temple is situated on the Earth\'s Van Allen radiation belt, possessing a rare geomagnetic field similar to Stonehenge and Machu Picchu that fosters profound meditative calm. The temple became a global beacon of transcendental consciousness when Swami Vivekananda meditated here in 1890, followed by Lama Anagarika Govinda, Walter Evans-Wentz, Beat poet Allen Ginsberg, and music legends Bob Dylan and George Harrison.',
                cover_image_url='/static/images/Almora/kashardevi.png',
                best_time='Year-round (Kartik Poornima for Kasar Devi Mela; clear winter sunsets)', featured=True
            ),
            Destination(
                name='Chitai Golu Devta Temple', slug='chitai-golu-devta-temple', region='kumaon', category='temple',
                district='Almora', lat=29.6056, lng=79.6978, altitude_m=1800,
                description='Located 8 km from Almora, Chitai is the foremost temple of Golu Devta, venerated across Kumaon as the God of Justice (Nyay ke Devta) and an incarnation of Lord Shiva. The temple grounds are an extraordinary spectacle, draped with tens of thousands of ringing brass bells hung by devotees whose prayers were granted. Pilgrims travel from across the Himalayas to submit handwritten petitions on stamp papers and postcards, seeking divine justice before the beloved deity who rides a white horse brandishing a bow and arrow.',
                cover_image_url='/static/images/Almora/goludevtachatai.png',
                best_time='Year-round (festive mornings and Navratri)', featured=True
            ),
            Destination(
                name='Nanda Devi Temple, Almora', slug='nanda-devi-temple-almora', region='kumaon', category='temple',
                district='Almora', lat=29.5985, lng=79.6590, altitude_m=1640,
                description='Enshrined in the heart of Almora within the historic stone complex of Lala Bazaar, this revered shrine is dedicated to Goddess Nanda Devi, the guardian deity of the Chand dynasty and Kumaon. King Kalyan Chand originally established her worship in the royal palace at Malla Mahal in the 16th century. Every September during Bhadrapad Ashtami, the temple hosts the historic Almora Nanda Devi Fair, where twin murtis of Nanda and Sunanda are sculpted from banana trunks and paraded through ancient stone-paved lanes amid celebratory Jhora and Chanchari folk dances.',
                cover_image_url='/static/images/Almora/nandadevi.png',
                best_time='Year-round (Bhadrapad Ashtami in September for Nanda Devi Fair)', featured=True
            ),
            Destination(
                name='Vriddha Jageshwar Temple', slug='vriddha-jageshwar', region='kumaon', category='temple',
                district='Almora', lat=29.6450, lng=79.8600, altitude_m=2200,
                description='Perched on a high Himalayan ridge 3 km above Jageshwar Dham at an altitude of 2,200 meters, Vriddha Jageshwar (\'Old Jageshwar\') is believed to be the original site where Lord Shiva meditated as an ascetic sage before descending into the valley. Reached via a picturesque road or a walking trail through dense oak, pine, and rhododendron forests, this peaceful hilltop shrine provides an unhindered, spellbinding panoramic view of the Great Himalayan range—including Trishul, Nanda Devi, Nanda Kot, and the Panchachuli peaks.',
                cover_image_url='/static/images/Almora/virdhjageshwar.png',
                best_time='October–June (sunrise hours for crystalline Himalayan panorama)', featured=True
            ),
            Destination(
                name='Dandeshwar Temple (Dhadeshwar)', slug='dandeshwar-temple', region='kumaon', category='temple',
                district='Almora', lat=29.6330, lng=79.8450, altitude_m=1800,
                description='Situated just one kilometer upstream of Jageshwar Dham along the banks of the Jata Ganga, Dandeshwar Temple is the largest and most architecturally imposing stone temple in the entire Jageshwar valley. Erected during the Katyuri era, the sanctum features an enormous natural rock boulder venerated as Lord Shiva carrying a staff (Danda). Surrounded by eighteen smaller satellite shrines standing serenely among whispering deodar trees, Dandeshwar is protected by the Archaeological Survey of India as a masterpiece of ancient northern Indian stone masonry.',
                cover_image_url='/static/images/Almora/dhadeshwar.png',
                best_time='March–June, September–November', featured=True
            ),
            Destination(
                name='Kalbisht Devta Temple', slug='kalbisht-devta-temple', region='kumaon', category='temple',
                district='Almora', lat=29.6800, lng=79.7200, altitude_m=1950,
                description='Revered with profound devotion across the hills of Kumaon, Kalbisht Devta is an ancient pastoral protector and folk deity celebrated alongside Golu Devta as a defender of the helpless. In Kumaoni folk folklore, Kalbisht Baba was a flute-playing protector of cows, farmers, and mountain pastures who healed afflicted livestock. Following his betrayal by feudal landlords, his spirit became an eternal guardian of mountain livestock and village justice. Devotees visit this pine-sheltered shrine to offer fresh milk, copper bells, and iron tridents, seeking blessings for their livestock and peace in their homes.',
                cover_image_url='/static/images/Almora/kalbistgoludevta.png',
                best_time='Year-round (mornings and annual community bhandaras)', featured=True
            ),
            Destination(
                name='Munsiyari', slug='munsiyari', region='kumaon', category='trek',
                district='Pithoragarh', lat=30.0668, lng=80.2369, altitude_m=2200,
                description='The "little Kashmir" of Kumaon — a remote frontier town where the Panchachuli glacier peaks fill every window like a painted backdrop. Gateway to the Milam, Ralam, and Namik glaciers, and home to the Bhotia tribal community whose woolen shawls and oral epics are a civilisation in themselves.',
                cover_image_url='/static/images/destinations/munsiyari.jpg',
                best_time='May–June, September–October', featured=True
            ),
            Destination(
                name='Kausani', slug='kausani', region='kumaon', category='heritage',
                district='Almora', lat=29.8378, lng=79.5960, altitude_m=1890,
                description='A ridgeline village where Gandhi described watching the sunrise over Nanda Devi peak as "the most beautiful sunrise I have ever seen." Kausani\'s Anasakti Ashram preserves his handwritten notes. The Himalayan panorama — Trishul, Nanda Devi, Panchachuli — stretches 300km from this single viewpoint, framed by Kausani\'s famous organic tea gardens.',
                cover_image_url='/static/images/destinations/kausani.jpg',
                best_time='October–June (clear skies for mountain views)', featured=True
            ),
            Destination(
                name='Binsar Wildlife Sanctuary', slug='binsar', region='kumaon', category='wildlife',
                district='Almora', lat=29.7092, lng=79.7411, altitude_m=2412,
                description='A 47 sq km forest reserve at 2,412m housing over 200 species of birds including the rare cheer pheasant, koklass pheasant, and kalij. The Zero Point ridge offers an unobstructed 300km Himalayan panorama from Kedarnath to Nanda Devi. The brown oak-rhododendron forest is spectacular in spring.',
                cover_image_url='/static/images/destinations/binsar.jpg',
                best_time='March–June for birding, October–November for mountain views', featured=False
            ),
            Destination(
                name='Baleshwar Temple', slug='baleshwar-temple', region='kumaon', category='temple',
                district='Pithoragarh', lat=29.3374, lng=80.0967, altitude_m=1610,
                description='An architectural masterpiece of South Indian style stone craft in the Kumaon Himalayas, Baleshwar Temple was erected between the 10th and 12th century AD by the Chand dynasty rulers. Dedicated to Lord Shiva (Baleshwar Mahadev), the complex also enshrines Ratneshwar and Champawati Devi within intricate dark-granite sanctums. Ancient folklore honors master sculptor Jagannath Mistri, whose exquisite stonework and celestial apsaras so captivated the Chand King that his right hand was severed to prevent the creation of another rival masterpiece — yet, fueled by devotion, Mistri sculpted an equally revered temple using his left hand. The complex features exquisitely carved ceiling mandalas, dragon-headed stone water spouts, and centuries-old granite shivlings preserved under the Archaeological Survey of India (ASI).',
                cover_image_url='/static/images/champwat/Baleshwar_Temple.png',
                best_time='October–April', featured=True
            ),
            Destination(
                name='Purnagiri Temple', slug='purnagiri-temple', region='kumaon', category='temple',
                district='Pithoragarh', lat=29.1350, lng=80.1980, altitude_m=3000,
                description='Perched atop the Annapurna Peak at an altitude of 3,000m near Tanakpur along the border with Nepal, Maa Purnagiri is celebrated as one of the 108 supreme Shakti Peethas. In Hindu cosmology, when Lord Shiva carried Sati\'s body in his cosmic dance of sorrow, the navel (nabhi) of the goddess fell upon this precipitous mountain crest. Pilgrims undertake a rigorous barefoot ascent along narrow cliff-carved stairways above the roaring Kali (Sharda) river to offer prayers at the open-sky summit shrine, adorned with countless sacred red threads and bells tied by those praying for progeny and healing. The annual Chaitra Navratri fair brings over half a million devotees together in an unbroken centuries-old pilgrimage tradition.',
                cover_image_url='/static/images/champwat/Purnagiri_temple.png',
                best_time='October–May (Chaitra Navratri for the sacred Mela)', featured=True
            ),
            Destination(
                name='Golu Devta Temple', slug='golu-devta-champawat', region='kumaon', category='temple',
                district='Pithoragarh', lat=29.3360, lng=80.0910, altitude_m=1620,
                description='Champawat is the sacred birthplace and legendary ancestral seat of Golu Devta (Gwalla Devta), revered throughout Kumaon as the supreme incarnation of Lord Shiva and the divine dispenser of instant justice. Born to King Jhal Rai and Queen Kalindra of Champawat, folk ballads recount how the miraculous child outsmarted the jealousy of seven stepmothers by bringing stone horses to drink from the lake. Unlike conventional temples, devotees come to Golu Devta to present written petitions and legal affidavits detailing their griefs and seeking truth. The temple precincts echo with the resonant chime of thousands of brass bells donated by grateful devotees whose petitions were divinely resolved.',
                cover_image_url='/static/images/champwat/goluDevta.png',
                best_time='Year-round', featured=True
            ),
            Destination(
                name='Shyamlatal', slug='shyamlatal', region='kumaon', category='lake',
                district='Pithoragarh', lat=29.1860, lng=80.1250, altitude_m=1500,
                description='Shyamlatal is a serene natural lake spanning over 1.5 square kilometers at an elevation of 1,500m, famed for its deep blue-black waters that mirror the surrounding virgin oak, pine, and sal ridges. The lake derives its name \'Shyamla\' from its dark hue, evoking the divine form of Lord Krishna. On its tranquil banks stands the historic Ramakrishna Mission Vivekananda Ashram, founded in 1914 by Swami Virajananda (direct disciple of Swami Vivekananda). Blooming with pristine white water lilies (kumud) and framed by silent meditation walking trails, Shyamlatal remains an untouched haven of spiritual contemplation far from crowded tourist circuits.',
                cover_image_url='/static/images/champwat/shyamlatal.png',
                best_time='October–June', featured=True
            ),
            Destination(
                name='Abbott Mount', slug='abbott-mount', region='kumaon', category='heritage',
                district='Pithoragarh', lat=29.4187, lng=80.1205, altitude_m=1981,
                description='A secluded colonial hill retreat perched on a ridge at nearly 2,000m, looking directly onto Trishul, Maiktoli, and Nanda Kot peaks. Established in 1914 by John Harold Abbott, its 13 scattered stone cottages amidst oak and deodar woods offer an untouched sanctuary far from crowded hill stations.',
                cover_image_url='/static/images/destinations/abbott_mount.jpg',
                best_time='March–June, September–November', featured=True
            ),
            Destination(
                name='Pithoragarh Fort and Soar Valley', slug='pithoragarh-fort', region='kumaon', category='heritage',
                district='Pithoragarh', lat=29.5828, lng=80.2182, altitude_m=1645,
                description='Known as the Mini Kashmir of Kumaon, the Soar Valley is an amphitheatre of terraced farmland ringed by snowcapped Himalayan peaks. The historic Chand-dynasty Pithoragarh Fort stands guard on a prominent hilltop overlooking the entire valley.',
                cover_image_url='/static/images/destinations/pithoragarh_fort.jpg',
                best_time='September–May', featured=True
            ),
            # Garhwal — Uttarkashi
            Destination(
                name='Rishikesh', slug='rishikesh', region='garhwal', category='heritage',
                district='Uttarkashi', lat=30.0869, lng=78.2676, altitude_m=356,
                description='Where the Ganges leaves the Himalayas for the plains — Rishikesh is simultaneously the yoga capital of the world and a frontier town with rapid river crossings, ashrams on every bank, and a Beatles-era retreat (Maharishi Mahesh Yogi\'s ashram) now reclaimed by jungle. The Laxman Jhula suspension bridge connects two worlds of the city.',
                cover_image_url='/static/images/destinations/rishikesh.jpg',
                best_time='September–March (avoid monsoon for river sports)', featured=True
            ),
            Destination(
                name='Valley of Flowers', slug='valley-of-flowers', region='garhwal', category='trek',
                district='Uttarkashi', lat=30.7278, lng=79.6097, altitude_m=3352,
                description='A UNESCO World Heritage Site — a high-altitude valley in the Zanskar range where over 500 species of wildflowers bloom in concentric bands of color during the monsoon (July–September). The trek from Govindghat passes through Ghangaria. The valley itself — 87.5 sq km, closed in winter — feels like a living painting.',
                cover_image_url='/static/images/destinations/valley_of_flowers.jpg',
                best_time='July–September (peak bloom)', featured=True
            ),
            Destination(
                name='Haridwar', slug='haridwar', region='garhwal', category='temple',
                district='Uttarkashi', lat=29.9457, lng=78.1642, altitude_m=314,
                description='The gateway to the gods — where the Ganges fully enters the plains, marked by the Har Ki Pauri ghat where the evening Ganga Aarti turns the river surface into a floating temple of fire and flowers. Haridwar is one of the four Kumbh Mela sites and receives millions of pilgrims annually, yet retains its ancient rhythm.',
                cover_image_url='/static/images/destinations/haridwar.jpg',
                best_time='October–March (cooler for pilgrimage)', featured=True
            ),
            Destination(
                name='Auli', slug='auli', region='garhwal', category='trek',
                district='Uttarkashi', lat=30.5256, lng=79.5622, altitude_m=2519,
                description='India\'s premier ski destination — a bowl of meadows at 2,519m with Asia\'s longest gondola (4km) and views of Nanda Devi dominating the skyline. In summer, Auli transforms into a meadow carpeted with wildflowers, making it equally spectacular for trekking toward Kuari Pass.',
                cover_image_url='/static/images/destinations/auli.jpg',
                best_time='Dec–Feb for skiing; May–Jun for trekking', featured=False
            ),
            Destination(
                name='Uttarkashi', slug='uttarkashi', region='garhwal', category='temple',
                district='Uttarkashi', lat=30.7268, lng=78.4354, altitude_m=1158,
                description='Gateway to the Gangotri glacier and Yamunotri shrines, nestled along the sacred Bhagirathi River with ancient temples and vibrant mountain culture.',
                cover_image_url='/static/images/destinations/uttarkashi.jpg',
                best_time='March–June, September–November', featured=True
            ),
            Destination(
                name='Chopta & Tungnath', slug='chopta-tungnath', region='garhwal', category='trek',
                district='Uttarkashi', lat=30.4878, lng=79.2185, altitude_m=2680,
                description='Known as the Mini Switzerland of Uttarakhand, Chopta is an untouched alpine meadow bugyal framed by evergreen deodar and oak forests. It serves as the base for the trek to Tungnath, the highest Shiva temple in the world at 3,680m, and the summit ridge of Chandrashila with a 360-degree Himalayan panorama.',
                cover_image_url='/static/images/destinations/chopta_tungnath.jpg',
                best_time='April–June, September–November (snow trekking Dec–Feb)', featured=True
            ),
            Destination(
                name='Tehri Lake & Dam', slug='tehri-lake', region='garhwal', category='lake',
                district='Uttarkashi', lat=30.3787, lng=78.4803, altitude_m=1750,
                description='A massive turquoise alpine reservoir created by Asia\'s highest dam across the Bhagirathi River. Tehri Lake has emerged as Uttarakhand\'s premier watersports destination, offering jet-skiing, speed-boating, kayaking, and floating eco-cottages surrounded by green Shivalik hills.',
                cover_image_url='/static/images/destinations/tehri_lake.jpg',
                best_time='March–June, September–December', featured=True
            ),
        ]
        db.session.add_all(destinations)
        db.session.flush()

        # Map destinations by slug for reliable, explicit referencing
        dest_map = {d.slug: d for d in destinations}
        nainital = dest_map['nainital']
        almora = dest_map['almora']
        munsiyari = dest_map['munsiyari']
        jageshwar = dest_map['jageshwar']
        kausani = dest_map['kausani']
        binsar = dest_map['binsar']
        baleshwar = dest_map['baleshwar-temple']
        abbott_mount = dest_map['abbott-mount']
        pithoragarh_fort = dest_map['pithoragarh-fort']
        rishikesh = dest_map['rishikesh']
        valley_of_flowers = dest_map['valley-of-flowers']
        haridwar = dest_map['haridwar']
        auli = dest_map['auli']
        uttarkashi = dest_map['uttarkashi']
        purnagiri = dest_map['purnagiri-temple']
        golu = dest_map['golu-devta-champawat']
        shyamlatal = dest_map['shyamlatal']
        naina_devi = dest_map['naina-devi-temple']


        # -----------------------------------------------------------
        # Culture Entries — Festivals (Filterable Directory: 9 across 5 Districts)
        # -----------------------------------------------------------
        festivals = [
            # 1. NAINITAL — Nanda Devi Mela
            CultureEntry(
                slug='nanda-devi-mela-nainital',
                region='kumaon',
                entry_type='festival',
                category='Religious',
                title='Nanda Devi Mela',
                subtitle='Goddess Procession and Kumaoni Sacred Gathering',
                district='Nainital',
                venue='Naina Devi Temple, Flats Ground',
                deity_or_ritual='Procession of Goddess Nanda Devi with ceremonial banana-trunk murtis, traditional Chholiya sword dance, and ancient Kumaoni benediction hymns',
                attendance='Est. 80,000+ devotees (illustrative estimate — verify with state tourism board)',
                when_celebrated='16 – 20 September 2026 (Nanda Ashtami on 19 September)',
                month_name='September',
                month_number=9,
                is_happening_soon=True,
                cover_image_url='/static/images/Nanital/NainaDeviTemple.png',
                story_text="""Nanda Devi is not merely a deity in Kumaon; she is considered the elder daughter of the mountains, married to Lord Shiva in high Kailash. Every autumn during Bhadrapad Ashtami, she returns home to visit her maternal kin in the valleys.

In Nainital, the Mela centers around the sacred Naina Devi temple by the lake's northern edge. Two towering ceremonial idols of Nanda and her sister Sunanda are meticulously sculpted from the living trunks of sacred plantain (banana) trees by hereditary artisans following strict Vedic and Tantric canons. No iron tools may touch the wood.

When the idols are carried in a grand procession through the narrow bazaar to the Flats ground, thousands of women dressed in traditional saffron and red Pichhora join in songs of farewell and gratitude. The fair culminates with the ritual immersion of the deities into the emerald waters of Naini Lake, accompanied by the clatter of brass cymbals and the rhythmic thunder of Hurka drums.""",
                travel_tips="""• Best viewing: Arrive at the Flats Ground by 9:00 AM on Bhadrapad Ashtami for the morning idol unveiling.
• Dress code: Modest ethnic attire is recommended; traditional yellow/saffron shawls are worn by devotees.
• Logistics: Vehicles are barred from Mall Road during peak procession hours; use the designated shuttle from Tallital.""",
                destination_id=naina_devi.id
            ),

            # 2. NAINITAL — Nainital Winter Carnival
            CultureEntry(
                slug='nainital-winter-carnival',
                region='kumaon',
                entry_type='festival',
                category='Cultural',
                title='Nainital Winter Carnival',
                subtitle='Year-End Cultural Parades and Lake Festivities',
                district='Nainital',
                venue='Mall Road and Naini Lake',
                deity_or_ritual='Lakeside winter parades, Pahari acoustic music concerts, heritage walks, illuminated midnight yacht flotillas, and local mountain culinary competitions',
                attendance='Est. 45,000+ visitors (illustrative estimate — verify with state tourism board)',
                when_celebrated='25 – 31 December 2026',
                month_name='December',
                month_number=12,
                is_happening_soon=False,
                cover_image_url='/static/images/Nanital/Mallroad.png',
                story_text="""As December frost settles over the Kumaon hills, Nainital transforms into a vibrant amphitheatre of mountain folklore, sound, and light. Originating as a celebration of the Himalayan winter, the festival marks the final week of the year with colorful pageantry that bridges heritage and modern celebration.

The festival kicks off with an energetic carnival parade down the historic Mall Road, featuring Chholiya dancers in gleaming brass armor, school bands, and masked folk performers representing each valley of Kumaon.

By twilight, illuminated traditional yachts and rowboats glide across Naini Lake, their lantern reflections dancing across the dark mirror of water. Stalls along the promenade serve steaming cups of pahadi chai, Singodi sweets wrapped in Malu leaves, and organic millet preparations while local indie folk bands perform beneath cedar canopies.""",
                travel_tips="""• Weather note: Temperatures frequently hover near 2°C to 7°C; carry windproof thermal layers and woolens.
• Photography: The best angles for the evening lake flotilla are from the higher vantage point along Ayarpatta ridge.
• Accommodation: Book heritage lakeside homestays at least 4 weeks in advance for Christmas and New Year's week.""",
                destination_id=nainital.id
            ),

            # 3. ALMORA — Nanda Devi Fair, Almora
            CultureEntry(
                slug='nanda-devi-fair-almora',
                region='kumaon',
                entry_type='festival',
                category='Fair',
                title='Nanda Devi Fair, Almora',
                subtitle='Chand Dynasty Heritage and Royal Idol Procession',
                district='Almora',
                venue='Nanda Devi Temple, Almora Bazaar',
                deity_or_ritual='Royal court procession of ceremonial plantain murtis, hereditary temple offerings, and classical Jhora-Chanchari community circles through the old cobblestone alleys',
                attendance='Est. 100,000+ pilgrims (illustrative estimate — verify with state tourism board)',
                when_celebrated='16 – 20 September 2026 (Nanda Ashtami Procession on 19 September)',
                month_name='September',
                month_number=9,
                is_happening_soon=True,
                cover_image_url='/static/images/Almora/nandadevi.png',
                story_text="""The historic royal seat of Almora celebrates Nanda Devi with an unbroken lineage of courtly ritual tracing back to the 16th-century Chand kings. King Kalyan Chand originally established the royal Nanda Devi temple inside the Malla Mahal fort, dedicating his crown and realm to the mountain goddess.

During Bhadrapad Ashtami, the twin murtis of Nanda and Sunanda are crafted from freshly felled banana trunks brought from a chosen village forest. The facial features of the goddess are painted with natural mineral pigments by hereditary priests inside the temple sanctum behind closed doors.

When the temple doors swing open, a sacred bell peal resounds across Almora's ridges. The fair is renowned for its all-night Jhora singing: circles of up to fifty men and women holding hands, swaying in synchrony while chanting centuries-old verse narrating the history of Kumaon's mountain kings and the benevolence of the goddess.""",
                travel_tips="""• Cultural courtesy: Photography is permitted in the outer temple square, but cameras must be turned off inside the inner sanctum.
• Footwear: The cobblestone streets of Lala Bazaar are steep and pedestrian-only; sturdy walking shoes are essential.
• Local sweet: Don't leave without tasting genuine Bal Mithai roasted with khoya and sugar balls from the bazaar stalls.""",
                destination_id=almora.id
            ),

            # 4. ALMORA — Jageshwar Monsoon Festival
            CultureEntry(
                slug='jageshwar-monsoon-festival',
                region='kumaon',
                entry_type='festival',
                category='Religious',
                title='Jageshwar Monsoon Festival',
                subtitle='Ancient Cedar Forest Shiva Pilgrimage',
                district='Almora',
                venue='Jageshwar Temple Cluster (Mahamrityunjaya Temple)',
                deity_or_ritual='Continuous Vedic chanting, Mahamrityunjaya jaap, holy water abhishek from the Jata Ganga, and twilight earthen butter lamp aartis under sacred Deodars',
                attendance='Est. 60,000+ devotees (illustrative estimate — verify with state tourism board)',
                when_celebrated='16 July – 15 August 2026 (Holy Shravan Month)',
                month_name='August',
                month_number=8,
                is_happening_soon=False,
                cover_image_url='/static/images/Almora/jagwasher.png',
                story_text="""Deep within a mist-shrouded valley 36km from Almora stands Jageshwar — an extraordinary complex of 124 ancient stone temples built between the 7th and 12th centuries by Katyuri and Chand dynasty master stonemasons. Here, enveloped by giant Himalayan cedar trees (Deodars), Lord Shiva is venerated as the cosmic healer.

During the monsoon month of Shravan, thousands of devotees walk barefoot through damp cedar groves to offer mountain wildflowers, bael leaves, and fresh glacial stream water to the Mahamrityunjaya Lingam.

The atmosphere is defined by silence and the reverberation of bronze bells against ancient stone. As evening falls, hundreds of handmade brass lamps are lit across the stone courtyards. The monsoon rain falling through the cedar canopy creates a natural music that merges with Vedic hymns in one of the most serene sacred spaces on earth.""",
                travel_tips="""• Best hour: Early morning between 5:30 AM and 7:00 AM before pilgrim tour buses arrive from Haldwani.
• Packing tip: The valley stays humid and rainy during monsoon; carry waterproof footwear and a dependable umbrella.
• Heritage note: Visit the ASI Archaeological Museum on-site to inspect the famed 9th-century bronze sculpture of Pona Raja.""",
                destination_id=jageshwar.id
            ),

            # 5. UTTARKASHI — Magh Mela (Duldul)
            CultureEntry(
                slug='magh-mela-uttarkashi',
                region='garhwal',
                entry_type='festival',
                category='Fair',
                title='Magh Mela (Duldul)',
                subtitle='Ancient Winter Trade and Cultural Sangam of Garhwal',
                district='Uttarkashi',
                venue='Kashi Vishwanath Temple, Ramlila Ground',
                deity_or_ritual='Arrival of local valley deities on palanquins (dolis) heralded by copper Ransingha horns, ceremonial Makar Sankranti river bath, and trans-Himalayan woolen trade',
                attendance='Est. 75,000+ traders and pilgrims (illustrative estimate — verify with state tourism board)',
                when_celebrated='14 – 21 January 2027 (Makar Sankranti)',
                month_name='January',
                month_number=1,
                is_happening_soon=False,
                cover_image_url='https://images.unsplash.com/photo-1548365328-8c6db3220e4c?w=700&q=80',
                story_text="""Magh Mela is one of the oldest cultural trade fairs of the Garhwal Himalayas. Historically, when high passes were blanketed under winter snow, shepherds and artisans from the upper Rawain, Bhotia, and Jaunsar valleys would trek down to Uttarkashi with woolens, herbs, hand-beaten copper vessels, and dried mountain apples.

The fair begins at dawn on Makar Sankranti with the ritual arrival of village deities carried upon high wooden palanquins (dolis). The bearers sway rhythmically as if possessed by the spirit of the gods, moving to the low drone of long copper Ransinghas and the double-headed Dhol-Damau.

Pilgrims take a ritual cleansing bath in the frigid Bhagirathi River before praying at the 1,200-year-old Kashi Vishwanath temple. For the next seven days, the town becomes a bustling mountain bazaar where traditional weavers, blacksmiths, and folk troupes celebrate the sun's northward turn.""",
                travel_tips="""• Cold gear: January in Uttarkashi has freezing nights (-1°C); pack heavy thermal innerwear, woolen socks, and down jackets.
• Shopping: Exceptional place to purchase genuine hand-spun sheep wool blankets (Pankhi), Ringal baskets, and raw pine honey.
• Timing: Deity palanquin greetings take place on the inaugural morning around 8:00 AM at the Ramlila Ground.""",
                destination_id=rishikesh.id
            ),

            # 6. UTTARKASHI — Ganga Dussehra
            CultureEntry(
                slug='ganga-dussehra-uttarkashi',
                region='garhwal',
                entry_type='festival',
                category='Religious',
                title='Ganga Dussehra',
                subtitle='Sacred Descent of the Holy River Bhagirathi',
                district='Uttarkashi',
                venue='Bhagirathi Ghats, Uttarkashi Town',
                deity_or_ritual='Commemorates the celestial descent of Mother Ganga (Avatarana) with ten-fold river purification snan, floating earthen dipa lamps, and twilight Bhagirathi Aarti',
                attendance='Est. 90,000+ devotees (illustrative estimate — verify with state tourism board)',
                when_celebrated='15 – 24 May 2026 (Shukla Dashami of Jyeshtha on 24 May)',
                month_name='June',
                month_number=6,
                is_happening_soon=False,
                cover_image_url='https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80',
                story_text="""In Hindu sacred cosmology, the river Ganga did not simply flow on earth — she descended from the heavens through the ascetic austerities of King Bhagiratha to liberate his ancestors. Ganga Dussehra celebrates the exact tenth day (Dashami) of the waxing moon in Jyeshtha when the river first touched the peaks of Uttarakhand.

In Uttarkashi, where the river still retains her primal name 'Bhagirathi', the festival is observed with immense devotion. Pilgrims gather on the ghats to take ten sacred dips, each immersion believed to wash away one of ten specific moral offenses (three physical, four vocal, and three mental).

In the evening, priests perform the grand Bhagirathi Aarti with multi-tiered brass oil lamps. Thousands of earthen leaf-boats (dona) bearing marigold blossoms and flickering camphor are gently released onto the rushing river, turning the emerald torrent into a moving constellation of light.""",
                travel_tips="""• River safety: The Bhagirathi flows with torrential glacial speed in June; only bathe within designated iron chain enclosures.
• Best viewpoint: The pedestrian suspension bridge over the Bhagirathi gives a breathtaking view of the evening lamp flotilla.
• Temple visit: Combine with morning prayers at the historic Shakti Temple to view the 26-foot heavy bronze trident.""",
                destination_id=rishikesh.id
            ),

            # 7. PITHORAGARH — Maa Purnagiri Mela
            CultureEntry(
                slug='maa-purnagiri-mela-champawat',
                region='kumaon',
                entry_type='festival',
                category='Religious',
                title='Maa Purnagiri Mela',
                subtitle='Shakti Peeth Pilgrimage on the Kali River Border',
                district='Pithoragarh',
                venue='Purnagiri Temple (Annapurna Peak) above Kali River',
                deity_or_ritual='Veneration of the sacred navel of Goddess Sati; strenuous barefoot cliff ascent along winding ridge trails, bell donations, and tying sacred red threads',
                attendance='Est. 500,000+ pilgrims (illustrative estimate — verify with state tourism board)',
                when_celebrated='19 March – 27 March 2026 (Chaitra Navratri)',
                month_name='April',
                month_number=4,
                is_happening_soon=False,
                cover_image_url='/static/images/champwat/Purnagiri_temple.png',
                story_text="""Perched at an elevation of 3,000 meters atop the Annapurna Peak near the Indo-Nepal border, Purnagiri is one of the 108 venerated Shakti Peethas. According to the Shiva Purana, when Lord Shiva performed the cosmic dance of grief carrying Sati's remains, the navel (nabhi) of the goddess fell upon this precipitous mountain crest.

The annual Purnagiri Mela during Chaitra Navratri is one of Uttarakhand's largest religious congregations, drawing pilgrims from across northern India, the Terai plains, and western Nepal.

Devotees walk the final 3-kilometer steep mountain climb barefoot along precipitous stone staircases carved into rock faces above the roaring Kali River. At the summit shrine, no idols are housed — only a sacred rock face smeared with vermilion and surrounded by tens of thousands of brass bells, where pilgrims tie red threads promising to return when their prayers are answered.""",
                travel_tips="""• Fitness requirement: The uphill stone stairway climb from Thulligad is physically demanding; start early at 4:30 AM to beat the heat.
• Border note: Carry valid government photo ID as the area lies close to the international border with Nepal.
• Return trail: Follow the traditional custom of visiting the Siddha Baba temple across the Sharda barrage after completing the ascent.""",
                destination_id=purnagiri.id
            ),

            # 8. PITHORAGARH — Devidhura Bagwal Mela
            CultureEntry(
                slug='devidhura-bagwal-mela',
                region='kumaon',
                entry_type='festival',
                category='Harvest',
                title='Devidhura Bagwal Mela',
                subtitle='The Ancient Four-Clan Ceremonial Fair of Varahi Devi',
                district='Pithoragarh',
                venue='Maa Varahi Devi Temple, Devidhura',
                deity_or_ritual='Centuries-old ceremonial duel where four warrior clans (Walik, Chamyal, Lamgaria, Gaherwal) armed with wicker shields pelt fruit to honor Varahi Devi without human sacrifice',
                attendance='Est. 120,000+ spectators (illustrative estimate — verify with state tourism board)',
                when_celebrated='28 August 2026 (Raksha Bandhan / Shravan Purnima)',
                month_name='August',
                month_number=8,
                is_happening_soon=False,
                cover_image_url='https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=800&q=80',
                story_text="""In the high forested ridge of Devidhura, Raksha Bandhan brings a spectacle found nowhere else on earth: the Bagwal, or ritual stone-pelting tournament of Varahi Devi.

Folklore recounts that centuries ago, the ferocious goddess demanded an annual human sacrifice (narbuli) from the four warrior clans (Kham) of the region: the Walik, Chamyal, Lamgaria, and Gaherwal. When an elderly grandmother was faced with surrendering her only grandson, she wept and prayed intensely for mercy. Varahi Devi relented on one condition: the four clans must battle each other openly until blood equivalent to one human life was spilt upon the sacred earth.

For hundreds of years, warriors with large woven bamboo shields (Chhatoli) hurled stones at each other for exactly ten to fifteen minutes until the head priest blew the conch shell. In recent years, following a historic court directive, stones have been replaced with hard mountain pears and flowers, preserving the sacred valor and martial pride of the four clans without severe injury.""",
                travel_tips="""• Spectator safety: Stand on the elevated concrete spectator galleries or temple terraces; do not enter the central battle arena.
• Traffic: Devidhura is a remote mountain ridge; arrive a day early or before 7:00 AM on Raksha Bandhan morning.
• Local cuisine: Taste the regional Singodi and roasted hemp seed chutney (Bhang ki Chutney) prepared in village homes during the fair.""",
                destination_id=baleshwar.id
            ),

            # 9. CHAMOLI — Shri Nanda Devi Raj Jat Yatra
            CultureEntry(
                slug='nanda-devi-raj-jat',
                region='garhwal',
                entry_type='festival',
                category='Pilgrimage',
                title='Shri Nanda Devi Raj Jat Yatra',
                subtitle='The Royal 12-Year Himalayan Pilgrimage of the Four-Horned Ram',
                district='Chamoli',
                venue='Nauti Village to Homkund (280 km Alpine Foot Pilgrimage)',
                deity_or_ritual='12-year Himalayan sacred foot yatra led by the mythical four-horned ram (Chausingha Khadu) and the royal golden umbrella (Chhatoli) of the Kansuwa Kunwars across 18 alpine stages',
                attendance='Est. 250,000+ pilgrims across 19–22 days (illustrative estimate — verify with state tourism board)',
                when_celebrated='5 – 23 September 2026 (Homkund Culmination: 19 September 2026 · Nanda Ashtami)',
                month_name='September',
                month_number=9,
                is_happening_soon=True,
                cover_image_url='/static/images/hero/nanda-devi-banner.jpg',
                story_text="""The Shri Nanda Devi Raj Jat Yatra is the most sacred, challenging, and celebrated pilgrimage in the Central Himalayas. Organized once every twelve years, it traces the ceremonial farewell journey (vidaee) of Goddess Nanda Devi as she departs her maternal mountain home (maika) in the valleys to reunite with her divine consort Lord Shiva in his high glacial abode at Mount Trishul.

Spanning over 280 kilometers on foot across 19 to 22 arduous days, the yatra negotiates lush terraced villages, roaring river sangams, virgin oak and rhododendron canopies, and high-altitude alpine meadows (bugyals) before ascending beyond the snowline through Roopkund (5,029 m) and the treacherous Junargali Pass (5,122 m) to Homkund (4,061 m).

The pilgrimage is uniquely guided by the Chausingha Khadu — a miraculously born four-horned ram bearing sacred offerings, jewel ornaments, and the royal golden umbrella (Chhatoli) presented by the Kunwars of Kansuwa. At Nandkeshari, the Garhwal procession conjoins with the sacred silver Doli from Kumaon, uniting the twin cultural souls of Uttarakhand.

Beyond the village of Wan, all leather items, modern musical horns, and worldly ostentation are strictly prohibited. At Homkund, amidst the glacial amphitheatre of Trishul and Nanda Ghunti, the four-horned ram is consecrated and released towards the eternal snowfields, carrying the collective prayers of Uttarakhand into the divine heavens.""",
                travel_tips="""• 2026 Dates: 5 – 23 September 2026 (Homkund culmination on Nanda Ashtami: 19 September 2026).
• Physical fitness: High-altitude endurance trekking through 5,000+ m passes; acclimatization and medical fitness certificate are mandatory.
• Gear checklist: Sub-zero sleeping bags, waterproof mountaineering boots, rain protection, thermal layers, and trekking poles.
• Cultural sanctity: Strictly adhere to local mountain norms — no leather articles, liquor, or non-biodegradable waste beyond Wan village.""",
                destination_id=valley_of_flowers.id
            ),
        ]
        db.session.add_all(festivals)

        # -----------------------------------------------------------
        # Culture Entries — Art
        # -----------------------------------------------------------
        arts = [
            CultureEntry(
                region='kumaon', entry_type='art',
                title='Aipan',
                subtitle='Sacred Geometric Ritual Art of Kumaon',
                district='Almora',
                cover_image_url='https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=700&q=80',
                gi_tag=True,
                story_text="""Aipan is drawn exclusively with the ring finger — the "anaamica" in Sanskrit, the finger believed to have a direct nerve connection to the heart. No brush, no stencil, no ruler. The artist begins with a red-ochre (geru) base coat on the floor or wall, then draws white rice-paste (biswar) lines over it in an unbroken gesture that begins and ends with a central dot — the "bindu" — representing the undivided universe from which all pattern emerges.

The motifs are not decorative choices. Each has specific ritual function: the "Shri Yantra" pattern is for Lakshmi's arrival; the swastika (in its original Vedic meaning, svastika: "that which is associated with well-being") marks auspicious beginnings; the lotus indicates purity; footprints mark the passage of deities through space.

Aipan is drawn only by women, and the knowledge passes from mother to daughter in an unbroken chain. The patterns vary by district — Almora's Aipan favors fine geometric precision; Pithoragarh's work is larger and bolder. The GI tag (2023) recognizes this tradition as specifically and exclusively Kumaoni, protecting it from imitation and commercial dilution.""",
                destination_id=almora.id
            ),
            CultureEntry(
                region='kumaon', entry_type='art',
                title='Ringal Craft',
                subtitle='Himalayan Bamboo Weaving',
                district='Pithoragarh',
                cover_image_url='https://images.unsplash.com/photo-1578301978693-85fa9c0320b9?w=700&q=80',
                story_text="""Ringal is the name for a species of Himalayan bamboo (Himalayacalamus falconeri) that grows at 2,000–3,500m in Kumaon's forests — thin, flexible, and extraordinarily strong for its weight. Kumaoni craftspeople have woven it for generations into baskets (tokri), mats (pat), storage containers, sieves, and decorative objects of remarkable complexity.

The craft requires harvesting the ringal at the right stage of maturity (neither too young nor old), splitting it into strips of controlled width, and then weaving those strips into patterns using techniques passed down without written instruction. The quality of Ringal craft from Pithoragarh is particularly valued — the weave is so tight that the baskets are waterproof without any coating.

Ringal craft is now under economic pressure from plastic alternatives, but several self-help groups and artisan cooperatives in Pithoragarh are preserving the tradition and creating contemporary products — laptop sleeves, home accessories, wall art — that carry the craft into new markets while keeping the makers in their mountain villages.""",
                destination_id=pithoragarh_fort.id
            ),
            CultureEntry(
                region='garhwal', entry_type='art',
                title='Garhwali Temple Wood Carving',
                subtitle='Living Architecture of the High Himalayas',
                district='Uttarkashi',
                cover_image_url='/static/images/Arts/WoodenCarving/woodencarving.png',
                story_text="""The kath-khuni style of traditional Garhwali architecture — alternating layers of wood and stone — is instantly recognizable in the hill temples and village homes of Chamoli and Uttarkashi. What makes it extraordinary is the ornamental woodcarving applied to every exposed surface: window frames, doorposts, column capitals, eaves, and structural brackets.

The motifs are drawn from Puranic mythology, local forest imagery, and geometric patterns of great mathematical complexity. A single carved doorframe might depict the ten avatars of Vishnu, flanked by celestial musicians (gandharvas), all enclosed in a border of interlocking lotus petals and running vine patterns — each element carved with hand tools by craftsmen who could not always read but could reproduce every religious narrative their community had ever told.

The Dhari Devi temple complex, the Triyuginarayan temple, and the village temples of the Rawain valley contain some of the finest surviving examples. Several of these temples are centuries old; the carved wood has survived monsoons and earthquakes that destroyed later stone construction.""",
                destination_id=rishikesh.id
            ),
        ]
        db.session.add_all(arts)

        # -----------------------------------------------------------
        # Food Items
        # -----------------------------------------------------------
        foods = [
            FoodItem(
                name='Bhatt ki Churkani', region='kumaon', category='main',
                description='A slow-cooked black soybean (bhatt) curry thickened with its own starch — smoky, deeply savory, and warming. The bhatt soybean is native to Kumaon\'s high-altitude fields and has no commercial equivalent; its flavor is earthy and nutty in a way that no other legume quite achieves. Eaten with rice or madua roti, particularly in winter.',
                ingredients='Black soybeans (bhatt), garlic, dry red chilies, hing (asafoetida), mustard oil, cumin, coriander',
                image_url='/static/images/food/bhatt_ki_churkani.jpg',
                where_to_try='Almora local dhabas, Nainital heritage restaurants, rural homestays',
                destination_id=almora.id
            ),
            FoodItem(
                name='Madua ki Roti', region='garhwal', category='main',
                description='Rustic, wholesome flatbread crafted from organic finger millet (mandua/ragi) stone-ground in traditional watermills (gharats). Slathered with fresh churned white butter, mountain sea salt, and fiery hill chillies, it provides sustained warmth and energy across Himalayan winters.',
                ingredients='Finger millet (mandua) flour, stone-ground whole wheat, pure desi ghee or fresh white butter, hill chillies, raw onions',
                image_url='/static/images/food/madua_ki_roti.jpg',
                where_to_try='Traditional village homestays in Chamoli, Uttarkashi, and Almora dhabas',
                destination_id=rishikesh.id
            ),
            FoodItem(
                name='Kafuli', region='garhwal', category='main',
                description='A rich, slow-cooked curry of spinach or fenugreek leaves, thickened with rice flour or stone-ground atta — bright green, intensely flavored, and deeply nourishing. Kafuli is considered the flagship dish of Garhwali cuisine: you cannot understand Garhwali food without eating it from a home kitchen at altitude.',
                ingredients='Spinach or fenugreek, rice flour, garlic, mustard oil, dry spices',
                image_url='https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=600&q=80',
                where_to_try='Rishikesh ayurvedic restaurants, Pauri homestays',
                destination_id=rishikesh.id
            ),
            FoodItem(
                name='Jhangora ki Kheer', region='kumaon', category='sweet',
                description='A milky pudding made from jhangora (barnyard millet) — lighter than rice kheer, with a subtle earthy sweetness. Jhangora grows at 2,000m+ and is one of Kumaon\'s native supergrains. Served at festivals and as the final dish of ceremonial meals.',
                ingredients='Barnyard millet (jhangora), full-fat milk, sugar, cardamom, raisins, dry fruits',
                image_url='/static/images/food/jhangora_ki_kheer.jpg',
                where_to_try='Festival days, rural homestays, Kausani tea-estate restaurants',
                destination_id=kausani.id
            ),
            FoodItem(
                name='Aloo ke Gutke', region='kumaon', category='snack',
                description='Pan-roasted Himalayan potatoes tempered with jakhiya (Himalayan wild caper seeds, unique to Uttarakhand), dry red chilies, coriander, and mustard oil. The jakhiya tempering gives Gutke an aroma and flavor impossible to replicate with standard spices. It\'s eaten as a side, a snack, or a late-night dhaba dish.',
                ingredients='Boiled potatoes, jakhiya seeds, dry red chilies, mustard oil, fresh coriander, lime',
                image_url='/static/images/food/aloo_ke_gutke.jpg',
                where_to_try='Every Kumaoni dhaba and home kitchen',
                destination_id=nainital.id
            ),
            FoodItem(
                name='Bal Mithai', region='kumaon', category='sweet',
                description='A dark-brown, fudge-like sweet made from slow-roasted khoya (reduced milk solids), shaped into cubes and coated in tiny white sugar pearls. The roasting gives it a distinctive bitter-caramel depth unlike any other Indian mithai. Almora is its home; the famous Sarthi Sweets has been making it for over a century.',
                ingredients='Khoya (reduced milk), sugar, white sugar pearls for coating',
                image_url='/static/images/food/bal_mithai.jpg',
                where_to_try='Almora — Sarthi Sweets, Lala Bazar; also available at Nainital sweet shops',
                destination_id=almora.id
            ),
            FoodItem(
                name='Chainsoo', region='garhwal', category='main',
                description='Ground black gram (urad) slow-cooked with dry red chilies, garlic, and hing into a thick, smoky, deeply earthy dal. The grinding step makes Chainsoo unlike any other dal preparation — the flour integrates into the cooking water, creating a dense, porridge-like consistency that clings to madua roti and warms the body from the inside on sub-zero Garhwal winters.',
                ingredients='Black gram (split urad), dry red chilies, garlic, hing, mustard oil, cumin',
                image_url='/static/images/food/chainsoo.jpg',
                where_to_try='Garhwal village homestays, Chamoli dhabas, Uttarkashi',
                destination_id=valley_of_flowers.id
            ),
            FoodItem(
                name='Gahat (Kulath) ki Dal', region='kumaon', category='main',
                description='Horse-gram lentils cooked with garlic, ginger, and Pahadi spices. Gahat is celebrated in Ayurveda for its warming properties and ability to dissolve kidney stones — mountain communities eat it through winter precisely because it generates internal heat. The flavor is nutty and slightly smoky, unlike ordinary dal.',
                ingredients='Horse-gram (kulath), garlic, ginger, dry spices, mustard oil, fresh coriander',
                image_url='/static/images/food/gahat_dal.jpg',
                where_to_try='Traditional Kumaoni restaurants, rural homestays in winter months',
                destination_id=munsiyari.id
            ),
        ]
        db.session.add_all(foods)

        # -----------------------------------------------------------
        # Hotels / Homestays (Authentic Local Stays with Real Host Photos)
        # -----------------------------------------------------------
        hotels_data = [
            # Almora
            Hotel(
                owner_id=host.id,
                name='Bloom HomeStay',
                hotel_type='homestay',
                district='Almora',
                destination_id=almora.id,
                price_min=1200,
                price_max=2200,
                amenities='["wifi", "parking", "mountain-view", "meals-included", "hot-water", "garden"]',
                images='["/static/images/hotels/bloom_homestay.jpg"]',
                cover_image_url='/static/images/hotels/bloom_homestay.jpg',
                host_name='Diwan Singh & Family',
                host_story='Located at Snobhyun, Almora, Uttarakhand (PIN: 263601). A charming hillside homestay featuring traditional red-roofed gabled architecture, expansive mountain balconies, and serene pine forest vistas. Hosted by a warm local Kumaoni family serving organic home-cooked meals (Bhatt ki Churkani, fresh chapatis, pahadi dal) and genuine mountain hospitality.',
                rating=4.9,
                review_count=38,
                featured=True,
                lat=29.6120,
                lng=79.6640
            ),
            Hotel(
                owner_id=host.id,
                name='The Hosteller Kasar Devi',
                hotel_type='hotel',
                district='Almora',
                destination_id=almora.id,
                price_min=850,
                price_max=2800,
                amenities='["wifi", "parking", "mountain-view", "cafe", "bonfire", "workstation", "games"]',
                images='["/static/images/hotels/the_hosteller_kasar_devi.jpg"]',
                cover_image_url='/static/images/hotels/the_hosteller_kasar_devi.jpg',
                host_name='The Hosteller Team',
                host_story='Located at Upper Binsar, Almora-Bageshwar Road, Balt Bari Road, Kasar Devi, Almora. A vibrant experiential hostel and mountain lodge crafted with timber facades, scenic private balconies, fast WiFi, and a lively travelers\' cafe. Popular among backpackers, remote workers, and spiritual seekers visiting Kasar Devi.',
                rating=4.8,
                review_count=94,
                featured=True,
                lat=29.6385,
                lng=79.6795
            ),
            Hotel(
                owner_id=host.id,
                name='Eja Homestay Falsima',
                hotel_type='homestay',
                district='Almora',
                destination_id=almora.id,
                price_min=1000,
                price_max=1900,
                amenities='["wifi", "mountain-view", "meals-included", "terrace", "village-walk", "organic-food"]',
                images='["/static/images/hotels/eja_homestay_falsima.jpg"]',
                cover_image_url='/static/images/hotels/eja_homestay_falsima.jpg',
                host_name='Kamala Joshi & Family',
                host_story='Located at Village Falsima, ITI Almora, Balta, Almora. An authentic heritage Kumaoni stone house with sky-blue hand-painted doors, whitewashed sunlit courtyards, and organic terrace farms. Features traditional woodfire cooking, Aipan art workshops, and breathtaking sunrise views over the Kumaon valleys.',
                rating=4.9,
                review_count=47,
                featured=True,
                lat=29.5875,
                lng=79.6480
            ),
            Hotel(
                owner_id=host.id,
                name='Ghumakkad Stay Jageshwar',
                hotel_type='homestay',
                district='Almora',
                destination_id=almora.id,
                price_min=1400,
                price_max=2500,
                amenities='["wifi", "parking", "mountain-view", "bonfire", "meals-included", "temple-trail", "garden"]',
                images='["/static/images/hotels/ghumakkad_stay_jageshwar.jpg"]',
                cover_image_url='/static/images/hotels/ghumakkad_stay_jageshwar.jpg',
                host_name='Harish Tewari',
                host_story='Located near sacred Jageshwar Dham, Almora. A peaceful nature retreat surrounded by towering deodar forests, just minutes from the sacred 124 9th-century stone temple complex. Features red-canopied cottages, flowering stone pathways, sprawling sunny lawns, and serene mountain river tranquility.',
                rating=4.8,
                review_count=52,
                featured=True,
                lat=29.6410,
                lng=79.8520
            ),
            # Uttarkashi
            Hotel(
                owner_id=host.id,
                name='Gaonvasi Homestay Uttarkashi',
                hotel_type='homestay',
                district='Uttarkashi',
                destination_id=uttarkashi.id,
                price_min=900,
                price_max=1800,
                amenities='["wifi", "mountain-view", "meals-included", "hot-water", "art-corner", "village-walk", "bonfire"]',
                images='["/static/images/hotels/gaonvasi_homestay_uttarkashi.jpg"]',
                cover_image_url='/static/images/hotels/gaonvasi_homestay_uttarkashi.jpg',
                host_name='Rawat Family & Gaonvasi Hosts',
                host_story='A soulful, rustic village homestay in Uttarkashi blending traditional Pahadi exposed brick architecture with creative bohemian touches. Features warm brick-walled rooms adorned with music and tarot art, homemade Garhwali meals (Mandua rotis, Gahat dal, fresh cow milk), and quiet mountain starlit evenings away from commercial crowds.',
                rating=4.9,
                review_count=34,
                featured=True,
                lat=30.7420,
                lng=78.4650
            ),
            Hotel(
                owner_id=host.id,
                name='Pine View Resort Uttarkashi',
                hotel_type='hotel',
                district='Uttarkashi',
                destination_id=uttarkashi.id,
                price_min=1500,
                price_max=2800,
                amenities='["wifi", "parking", "restaurant", "mountain-view", "room-service", "hot-water", "travel-desk"]',
                images='["/static/images/hotels/pine_view_resort_uttarkashi.png"]',
                cover_image_url='/static/images/hotels/pine_view_resort_uttarkashi.png',
                host_name='Devendra Singh Panwar & Team',
                host_story='Situated amidst fragrant pine-clad mountain slopes on the route to Gangotri, Pine View Resort offers spacious sunlit rooms with private balconies, secure gated parking, and an on-site multi-cuisine Pahadi restaurant. A favored stopover for Gangotri pilgrims, Dayara Bugyal trekkers, and family road-trippers seeking scenic comfort.',
                rating=4.8,
                review_count=58,
                featured=True,
                lat=30.7180,
                lng=78.4120
            ),
            Hotel(
                owner_id=host.id,
                name='Shiv Pariwar Yogic Resort Uttarkashi',
                hotel_type='hotel',
                district='Uttarkashi',
                destination_id=uttarkashi.id,
                price_min=1600,
                price_max=3200,
                amenities='["wifi", "river-view", "yoga-deck", "parking", "meditation-hall", "satvik-meals", "temple-trail", "bonfire"]',
                images='["/static/images/hotels/shiv_pariwar_yogic_resort.png"]',
                cover_image_url='/static/images/hotels/shiv_pariwar_yogic_resort.png',
                host_name='Acharya Anand & Shiv Pariwar Team',
                host_story='Set directly along the sacred banks of the Bhagirathi river next to the iconic green mountain suspension bridge, Shiv Pariwar Yogic Resort is a sanctuary for spiritual seekers, yogis, and nature lovers. Features daily yoga & meditation sessions by the river, satvik Ayurvedic dining, peaceful riverfront meditation decks, and easy access to Gangotri Dham.',
                rating=4.9,
                review_count=62,
                featured=True,
                lat=30.7720,
                lng=78.5080
            ),
            Hotel(
                owner_id=host.id,
                name='SKY HOME STAY',
                hotel_type='homestay',
                district='Uttarkashi',
                destination_id=uttarkashi.id,
                price_min=1100,
                price_max=2200,
                amenities='["wifi", "snow-peak-view", "trekking-guide", "meals-included", "organic-food", "parking", "terrace", "bonfire"]',
                images='["/static/images/hotels/sky_home_stay_uttarkashi.jpg"]',
                cover_image_url='/static/images/hotels/sky_home_stay_uttarkashi.jpg',
                host_name='Rawat Bandhu & Family (Raithal)',
                host_story='Perched high in the picturesque heritage village of Raithal (the gateway to the world-famous Dayara Bugyal alpine meadows), SKY HOME STAY boasts front-row panoramic views of snow-draped Greater Himalayan peaks from its sunny courtyard and balconies. Hosted by the warm Rawat family, offering authentic Garhwali hospitality, organic apple orchard walks, and local trekking guidance.',
                rating=4.9,
                review_count=45,
                featured=True,
                lat=30.8250,
                lng=78.5980
            ),
            # Champawat
            Hotel(
                owner_id=host.id,
                name='Hotel Shivansh',
                hotel_type='hotel',
                district='Champawat',
                destination_id=baleshwar.id,
                price_min=1200,
                price_max=2400,
                amenities='["wifi", "parking", "restaurant", "mountain-view", "hot-water", "travel-desk"]',
                images='["/static/images/hotels/hotel_shivansh_champawat.png"]',
                cover_image_url='/static/images/hotels/hotel_shivansh_champawat.png',
                host_name='Kailash Joshi & Team',
                host_story='Located centrally along the Champawat highway, Hotel Shivansh offers modern glass-paneled rooms, prompt room service, and secure parking. Ideal for travelers visiting the historic Baleshwar Temple, tea gardens of Champawat, and pilgrims en route to Purnagiri Dham and Reetha Sahib.',
                rating=4.8,
                review_count=36,
                featured=True,
                lat=29.3370,
                lng=80.0910
            ),
            Hotel(
                owner_id=host.id,
                name='Hotel Taj Tanakpur',
                hotel_type='hotel',
                district='Champawat',
                destination_id=purnagiri.id,
                price_min=1100,
                price_max=2200,
                amenities='["wifi", "parking", "lawn", "restaurant", "room-service", "hot-water", "pilgrim-friendly"]',
                images='["/static/images/hotels/hotel_taj_tanakpur.png"]',
                cover_image_url='/static/images/hotels/hotel_taj_tanakpur.png',
                host_name='Farooq Ahmed & Staff',
                host_story='Conveniently situated in Tanakpur with a sprawling green front lawn and ample private parking, Hotel Taj Tanakpur is a preferred hospitality stop for families, pilgrims visiting the revered Maa Purnagiri Temple, and travelers entering the Kumaon hills via Tanakpur railway junction.',
                rating=4.7,
                review_count=42,
                featured=True,
                lat=29.0720,
                lng=80.1110
            ),
            Hotel(
                owner_id=host.id,
                name='Hotel Shiva Residency',
                hotel_type='hotel',
                district='Champawat',
                destination_id=baleshwar.id,
                price_min=1300,
                price_max=2600,
                amenities='["wifi", "parking", "restaurant", "conference-room", "mountain-view", "elevator", "hot-water"]',
                images='["/static/images/hotels/hotel_shiva_residency.png"]',
                cover_image_url='/static/images/hotels/hotel_shiva_residency.png',
                host_name='Shiva Management Group',
                host_story='A contemporary commercial hotel in Champawat featuring distinctive crimson-and-silver exterior styling, spacious executive rooms, on-site dining, and banking/ATM convenience on premises. Provides easy connectivity to Abbott Mount, Mayawati Ashram, and ancient Chand Dynasty heritage monuments.',
                rating=4.8,
                review_count=49,
                featured=True,
                lat=29.3350,
                lng=80.0890
            ),
            # Nainital
            Hotel(
                owner_id=host.id,
                name='Hotel Lake View',
                hotel_type='hotel',
                district='Nainital',
                destination_id=nainital.id,
                price_min=1600,
                price_max=3000,
                amenities='["wifi", "lake-view", "mountain-view", "restaurant", "balcony", "hot-water", "terrace"]',
                images='["/static/images/hotels/hotel_lake_view_nainital.jpg"]',
                cover_image_url='/static/images/hotels/hotel_lake_view_nainital.jpg',
                host_name='Naveen Chandra Pant',
                host_story='Perched on the scenic hillside slopes overlooking the iconic emerald waters of Naini Lake, Hotel Lake View offers sweeping panoramic vistas from every room and private balcony. Guests enjoy brisk morning walks down to Mall Road and sunset tea while watching the colored sailboats glide across the lake.',
                rating=4.9,
                review_count=68,
                featured=True,
                lat=29.3895,
                lng=79.4520
            ),
            Hotel(
                owner_id=host.id,
                name='Hotel Himalayan',
                hotel_type='hotel',
                district='Nainital',
                destination_id=nainital.id,
                price_min=1800,
                price_max=3200,
                amenities='["wifi", "parking", "lake-view", "heritage", "garden", "restaurant", "games-room", "bonfire"]',
                images='["/static/images/hotels/hotel_himalayan_nainital.png"]',
                cover_image_url='/static/images/hotels/hotel_himalayan_nainital.png',
                host_name='The Himalaya Heritage Team',
                host_story='One of Nainital\'s classic heritage retreats, Hotel Himalayan stands gracefully on the mountain slopes with its distinct vintage gabled architecture, expansive sun decks, and uninterrupted views of Naini Lake. Features mini golf, spacious family suites, lush gardens, and warm Kumaoni hospitality.',
                rating=4.9,
                review_count=82,
                featured=True,
                lat=29.3840,
                lng=79.4590
            ),
            Hotel(
                owner_id=host.id,
                name='The Pavilion Hotel',
                hotel_type='hotel',
                district='Nainital',
                destination_id=nainital.id,
                price_min=2200,
                price_max=3800,
                amenities='["wifi", "parking", "garden", "restaurant", "heritage", "bonfire", "room-service", "hot-water"]',
                images='["/static/images/hotels/the_pavilion_hotel_nainital.jpg"]',
                cover_image_url='/static/images/hotels/the_pavilion_hotel_nainital.jpg',
                host_name='The Pavilion Heritage Hospitality',
                host_story='Built during the British Raj era near the historic Nainital cricket ground (The Flats), The Pavilion Hotel combines colonial architectural charm with warm modern comfort. Surrounded by deodar and oak trees, it features sprawling heritage verandahs, wooden gables, cozy open lawns with bonfire evenings, and immediate walking proximity to Naini Lake and Cheena Peak trails.',
                rating=4.9,
                review_count=95,
                featured=True,
                lat=29.3920,
                lng=79.4540
            ),
            Hotel(
                owner_id=host.id,
                name='Hotel Maharaja',
                hotel_type='hotel',
                district='Nainital',
                destination_id=nainital.id,
                price_min=1300,
                price_max=2500,
                amenities='["wifi", "parking", "mountain-view", "restaurant", "hot-water", "family-rooms", "travel-desk"]',
                images='["/static/images/hotels/hotel_maharaja_nainital.png"]',
                cover_image_url='/static/images/hotels/hotel_maharaja_nainital.png',
                host_name='Maharaja Hospitality Group',
                host_story='Conveniently nestled on the serene hillside of Upper Mallital on Zoo Road, Hotel Maharaja is a popular family hotel known for its warm stone-textured exterior, modern amenities, and peaceful vantage point away from crowded traffic. Offers quick access to the Pt. G.B. Pant High Altitude Zoo, Snow View Point, and traditional Kumaoni hospitality.',
                rating=4.8,
                review_count=54,
                featured=True,
                lat=29.3950,
                lng=79.4610
            ),
        ]
        db.session.add_all(hotels_data)
        db.session.flush()

        # -----------------------------------------------------------
        # Guides
        # -----------------------------------------------------------
        guides_data = [
            Guide(
                user_id=admin.id,
                name='Sujal Gaira',
                region='kumaon',
                district='Almora',
                districts_served='Almora, Jageshwar, Binsar',
                bio='Native of Almora with deep roots in local village culture. Specializes in village heritage walks, traditional stone house architecture, hidden forest trails, and authentic homestay coordination across the Kumaon hills.',
                specialties='["village tour", "local culture", "hidden trails", "homestays", "stone houses", "stories & history"]',
                languages='["English", "Hindi", "Kumaoni"]',
                daily_rate=2200,
                profile_image='/static/images/guides/sujal_gaira_avatar.jpg',
                gallery_images='["/static/images/guides/sujal_gaira.jpg", "/static/images/Almora/almora.png", "/static/images/Almora/jagwasher.png"]',
                availability_dates='["2026-09-18", "2026-09-19", "2026-09-20", "2026-09-24", "2026-09-25"]',
                rating=4.9,
                review_count=52,
                verified=True,
                years_experience=6
            ),
            Guide(
                user_id=admin.id,
                name='Priyanshu Negi',
                region='kumaon',
                district='Almora',
                districts_served='Almora, Jageshwar Dham, Kasar Devi',
                bio='Dedicated heritage and spiritual guide native to Jageshwar and Almora. Leading immersive pilgrimages through ancient Katyuri stone temples, deodar sanctuary pathways, and village cultural traditions.',
                specialties='["temple architecture", "spiritual tours", "hidden trails", "local culture", "village tour"]',
                languages='["English", "Hindi", "Kumaoni"]',
                daily_rate=2400,
                profile_image='/static/images/guides/priyanshu_negi_avatar.jpg',
                gallery_images='["/static/images/guides/priyanshu_negi.jpg", "/static/images/Almora/jagwasher.png", "/static/images/Almora/kashardevi.png"]',
                availability_dates='["2026-09-17", "2026-09-18", "2026-09-21", "2026-09-22", "2026-09-26"]',
                rating=5.0,
                review_count=64,
                verified=True,
                years_experience=8
            ),
            Guide(
                user_id=admin.id,
                name='Kunal Rana',
                region='garhwal',
                district='Uttarkashi',
                districts_served='Uttarkashi, Dayara Bugyal, Gangotri',
                bio='Certified mountaineer and high-altitude trekking guide trained at NIM Uttarkashi. Expert in alpine snow trails, Dayara Bugyal high meadows, and responsible community tourism throughout the upper Bhagirathi valley.',
                specialties='["snow expeditions", "high altitude trekking", "hidden trails", "wildlife", "village tour"]',
                languages='["English", "Hindi", "Garhwali"]',
                daily_rate=2600,
                profile_image='/static/images/guides/kunal_rana_avatar.jpg',
                gallery_images='["/static/images/guides/kunal_rana.jpg", "/static/images/destinations/uttarkashi.jpg", "/static/images/festivals/dyara_bugyal_holi.jpg"]',
                availability_dates='["2026-09-19", "2026-09-20", "2026-09-23", "2026-09-27"]',
                rating=4.9,
                review_count=58,
                verified=True,
                years_experience=7
            ),
            Guide(
                user_id=admin.id,
                name='Gaurav Rawat',
                region='garhwal',
                district='Uttarkashi',
                districts_served='Uttarkashi, Harsil Valley, Gangotri',
                bio='Local naturalist, storyteller, and landscape artist from Uttarkashi. Guiding riverside art & culture walks, scenic mountain vistas, artisan craft exchanges, and apple orchard village trails where art meets travel.',
                specialties='["art & crafts", "scenic spots", "river trails", "local food", "photography tours"]',
                languages='["English", "Hindi", "Garhwali"]',
                daily_rate=2300,
                profile_image='/static/images/guides/gaurav_rawat_avatar.jpg',
                gallery_images='["/static/images/guides/gaurav_rawat.jpg", "/static/images/destinations/uttarkashi.jpg", "/static/images/Arts/WoodenCarving/woodencarving.png"]',
                availability_dates='["2026-09-17", "2026-09-18", "2026-09-22", "2026-09-25"]',
                rating=4.8,
                review_count=41,
                verified=True,
                years_experience=5
            ),
        ]
        db.session.add_all(guides_data)
        db.session.flush()

        # -----------------------------------------------------------
        # Community Posts (Instagram 4:5 / 1:1, YouTube 16:9, YouTube Shorts 9:16, Instagram Embed)
        # -----------------------------------------------------------
        posts = [
            # 1. Instagram Photo Post (4:5 Portrait Ratio)
            CommunityPost(
                user_id=traveler.id,
                content='First light touching the snow ridge of Nanda Devi and Panchachuli. Shot at 6:10 AM from the Chandak ridge in Pithoragarh. The valley mist cleared just long enough for this single exposure.\n\nCaptured on 35mm lens · 4:5 Instagram Portrait format.',
                media_type='photo',
                aspect_ratio='4:5',
                images='["https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1080&q=85"]',
                district_tag='Pithoragarh',
                likes_count=142
            ),

            # 2. YouTube Standard Video (16:9 Widescreen)
            CommunityPost(
                user_id=admin.id,
                content='Exploring the forgotten high-altitude villages and pine forests of Kumaon. This 16:9 travel piece documents our 4-day homestay journey through Jageshwar, Kasar Devi, and Binsar sanctuary.',
                media_type='youtube',
                youtube_id='WqS3L427R9Q',
                video_format='16:9',
                aspect_ratio='16:9',
                media_url='https://www.youtube.com/watch?v=WqS3L427R9Q',
                district_tag='Almora',
                likes_count=218
            ),

            # 3. YouTube Shorts (9:16 Vertical Format)
            CommunityPost(
                user_id=traveler.id,
                content='Morning bell chimes and turquoise river roar at the sacred Bhagirathi riverbank in Uttarkashi at 5:30 AM. Tap to watch the 9:16 vertical short!',
                media_type='youtube_shorts',
                youtube_id='gT-x4-2_eXw',
                video_format='9:16',
                aspect_ratio='9:16',
                media_url='https://www.youtube.com/shorts/gT-x4-2_eXw',
                district_tag='Uttarkashi',
                likes_count=195
            ),

            # 4. Instagram Discovery Embed
            CommunityPost(
                user_id=traveler.id,
                content='Sunrise reflections over Naini Lake. The quiet morning stillness before the paddle boats come out is something everyone visiting Uttarakhand should experience.',
                media_type='instagram',
                media_url='https://www.instagram.com/p/C-nainiLake01/',
                instagram_shortcode='C-nainiLake01',
                aspect_ratio='4:5',
                district_tag='Nainital',
                likes_count=124
            ),

            # 5. Multi-photo Instagram 1:1 Square Grid
            CommunityPost(
                user_id=admin.id,
                content='Aipan art across Kumaoni homes: geometric rice-flour motifs drawn with the ring finger to invoke Lakshmi. Swipe through the square feed captures from Almora old bazaar.',
                media_type='photo',
                aspect_ratio='1:1',
                images='["https://images.unsplash.com/photo-1587474260584-136574528ed5?w=800&q=80", "https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=800&q=80"]',
                district_tag='Almora',
                likes_count=168
            ),

            # 6. YouTube Shorts - Munsiyari high-pass expedition
            CommunityPost(
                user_id=traveler2.id,
                content='Golden hour hitting the Panchachuli peaks from Khaliya Top at 3,500m. 9:16 vertical short of our sunrise camp!',
                media_type='youtube_shorts',
                youtube_id='dQw4w9WgXcQ',
                video_format='9:16',
                aspect_ratio='9:16',
                media_url='https://www.youtube.com/shorts/dQw4w9WgXcQ',
                district_tag='Pithoragarh',
                likes_count=230
            ),

            # 7. Photo - Dayara Bugyal Alpine Meadows
            CommunityPost(
                user_id=traveler3.id,
                content='Walking across endless velvet meadows of Dayara Bugyal with Bandarpoonch massif looming right ahead. One of the cleanest treks in Uttarkashi.',
                media_type='photo',
                aspect_ratio='4:5',
                images='["https://images.unsplash.com/photo-1604537529428-15bcbeecfe4d?w=1080&q=85"]',
                district_tag='Uttarkashi',
                likes_count=177
            ),

            # 8. Instagram Reel - Pangot Bird Sanctuary & Kilbury Forest
            CommunityPost(
                user_id=traveler4.id,
                content='Spotting Himalayan monals and cheer pheasants in the dense oak-rhododendron forest above Nainital. Pure wilderness 15km from the lake.',
                media_type='instagram',
                media_url='https://www.instagram.com/reel/C-pangotBirds02/',
                instagram_shortcode='C-pangotBirds02',
                aspect_ratio='9:16',
                district_tag='Nainital',
                likes_count=284
            ),
        ]
        db.session.add_all(posts)

        # -----------------------------------------------------------
        # Authentic Reviews (Hotels, Guides, Destinations)
        # -----------------------------------------------------------
        reviews = [
            # --- Hotel Reviews (Authentic Properties) ---
            # 1. Bloom HomeStay (Almora)
            Review(
                user_id=traveler.id,
                target_type='hotel',
                target_id=hotels_data[0].id,
                rating=5,
                comment='Staying at Bloom HomeStay in Snobhyun was unforgettable. Diwan Singh ji and his family welcomed us like old friends. The red gabled roof and wide mountain balconies overlook peaceful pine valleys. We enjoyed steaming home-cooked Bhatt ki Churkani and fresh phulkas with mountain ghee.'
            ),
            Review(
                user_id=traveler2.id,
                target_type='hotel',
                target_id=hotels_data[0].id,
                rating=5,
                comment='Peaceful mountain retreat away from the town noise. Clean, comfortable rooms with large windows letting in the morning Himalayan sun. Great hot water supply and warm blankets.'
            ),
            Review(
                user_id=traveler5.id,
                target_type='hotel',
                target_id=hotels_data[0].id,
                rating=5,
                comment='Incredible warmth from the host family. The garden area is lovely for morning chai while listening to birds in the pine woods. Definitely coming back!'
            ),

            # 2. The Hosteller Kasar Devi (Almora)
            Review(
                user_id=traveler2.id,
                target_type='hotel',
                target_id=hotels_data[1].id,
                rating=5,
                comment='The wooden aesthetics and mountain cafe here are top-tier! Perfect blend of social traveler vibes and quiet corners for remote work. High-speed WiFi and panoramic balcony vistas of the Binsar ridges.'
            ),
            Review(
                user_id=traveler3.id,
                target_type='hotel',
                target_id=hotels_data[1].id,
                rating=4,
                comment='Loved the sunset bonfire sessions and board games in the cafe. Very easy trail access up to Kasar Devi temple. Helpful staff and super clean dorms and private rooms.'
            ),

            # 3. Eja Homestay Falsima (Almora)
            Review(
                user_id=traveler.id,
                target_type='hotel',
                target_id=hotels_data[2].id,
                rating=5,
                comment='Eja Homestay is true Kumaoni cultural preservation! The traditional whitewashed stone house with sky-blue painted doors and hand-drawn Aipan motifs made us fall in love instantly. Kamala didi cooked delicious organic chulha meals.'
            ),
            Review(
                user_id=traveler4.id,
                target_type='hotel',
                target_id=hotels_data[2].id,
                rating=5,
                comment='Quiet village life in Falsima. Waking up to misty valley sunrises and taking farm walks through terraced fields. Genuine village hospitality at its best.'
            ),
            Review(
                user_id=traveler3.id,
                target_type='hotel',
                target_id=hotels_data[2].id,
                rating=5,
                comment='A deeply rejuvenating stay. The stone architecture stays naturally insulated, and the views across the Balta valley towards distant snow lines are breathtaking.'
            ),

            # 4. Ghumakkad Stay Jageshwar (Almora)
            Review(
                user_id=traveler5.id,
                target_type='hotel',
                target_id=hotels_data[3].id,
                rating=5,
                comment='Surrounded by ancient deodar forests just minutes from the sacred Jageshwar Dham temples. The red-roofed cottages and flower-lined stone pathways give it an enchanting fairy-tale feel. Harish ji arranged an early temple darshan for us.'
            ),
            Review(
                user_id=traveler2.id,
                target_type='hotel',
                target_id=hotels_data[3].id,
                rating=4,
                comment='Serene lawn, crisp mountain river breeze, and delicious hot dal-bhat. Perfect spiritual getaway destination.'
            ),

            # 5. Gaonvasi Homestay Uttarkashi (Uttarkashi)
            Review(
                user_id=traveler4.id,
                target_type='hotel',
                target_id=hotels_data[4].id,
                rating=5,
                comment='Gaonvasi Homestay has so much soul! The rustic exposed brick walls painted olive-green and cream, the vintage Queen poster and tarot wall hangings, and the warm winter quilts make it feel like a bohemian mountain sanctuary. Homemade Mandua rotis and pahadi dal were delicious.'
            ),
            Review(
                user_id=traveler3.id,
                target_type='hotel',
                target_id=hotels_data[4].id,
                rating=5,
                comment='Authentic village experience away from noisy highways. Quiet starlit nights, warm hospitality by the Rawat family, and great conversations by the evening bonfire.'
            ),

            # 6. Pine View Resort Uttarkashi (Uttarkashi)
            Review(
                user_id=traveler2.id,
                target_type='hotel',
                target_id=hotels_data[5].id,
                rating=5,
                comment='Spacious, sparkling clean rooms with private balconies facing the pine-covered hills. Ample gated parking and an excellent in-house restaurant serving hot parathas and local Garhwali dishes. Ideal stopover on the Gangotri highway.'
            ),
            Review(
                user_id=traveler.id,
                target_type='hotel',
                target_id=hotels_data[5].id,
                rating=5,
                comment='Great hospitality and prompt room service. Devendra ji and staff helped us with road information and travel planning for Gangotri. Highly recommended for families.'
            ),

            # 7. Shiv Pariwar Yogic Resort Uttarkashi (Uttarkashi)
            Review(
                user_id=traveler3.id,
                target_type='hotel',
                target_id=hotels_data[6].id,
                rating=5,
                comment='The location right on the banks of the sacred Bhagirathi next to the green mountain bridge is unmatched. Waking up to the sound of rushing waters and attending early morning yoga on the riverside deck was divine. Delicious satvik meals prepared with pure ingredients.'
            ),
            Review(
                user_id=traveler5.id,
                target_type='hotel',
                target_id=hotels_data[6].id,
                rating=5,
                comment='A true spiritual and wellness sanctuary in Uttarkashi. The aerial views of the valley, the river breeze, and the peaceful meditation atmosphere make this an unforgettable place.'
            ),

            # 8. SKY HOME STAY (Raithal, Uttarkashi)
            Review(
                user_id=traveler4.id,
                target_type='hotel',
                target_id=hotels_data[7].id,
                rating=5,
                comment='The snow-peak panorama from the veranda here is mind-blowing! You get front-row seats to the Greater Himalayas right from your morning tea chair. Located right in Raithal village at the start of the Dayara Bugyal trek.'
            ),
            Review(
                user_id=traveler2.id,
                target_type='hotel',
                target_id=hotels_data[7].id,
                rating=5,
                comment='Rawat Bandhu and their family treated us with unmatched warmth. They guided us on the Dayara Bugyal trail and shared wonderful stories about the village apple orchards. The best homestay experience in Garhwal!'
            ),

            # --- Guide Reviews ---
            # 1. Kishan Negi (Almora)
            Review(
                user_id=traveler.id,
                target_type='guide',
                target_id=guides_data[0].id,
                rating=5,
                comment='Kishan is an extraordinary guide. His knowledge of Jageshwar and local Kumaoni folklore made our trek truly memorable. He knows every hidden shrine and cedar trail.'
            ),
            Review(
                user_id=traveler2.id,
                target_type='guide',
                target_id=guides_data[0].id,
                rating=5,
                comment='Led us on an offbeat forest trail from Kasar Devi to Binsar sanctuary. Kishan identified dozens of Himalayan bird species and shared fascinating oral history about the Chand Kings.'
            ),
            Review(
                user_id=traveler4.id,
                target_type='guide',
                target_id=guides_data[0].id,
                rating=5,
                comment='Professional, patient, and deeply rooted in mountain heritage. Highly recommend Kishan for both spiritual journeys and rigorous nature walks.'
            ),

            # 2. Rekha Bisht (Pithoragarh / Munsiyari)
            Review(
                user_id=traveler2.id,
                target_type='guide',
                target_id=guides_data[1].id,
                rating=5,
                comment='Rekha is one of the toughest and most dependable mountain leaders in Uttarakhand. Certified wilderness responder who kept our high-altitude trek completely safe through sudden hail.'
            ),
            Review(
                user_id=traveler.id,
                target_type='guide',
                target_id=guides_data[1].id,
                rating=5,
                comment='Traveling with Rekha gave us access to traditional Bhotia tribal homestays that regular tourists never get to see. Inspiring woman guide!'
            ),
            Review(
                user_id=traveler3.id,
                target_type='guide',
                target_id=guides_data[1].id,
                rating=5,
                comment='Superb logistics on the Milam trail. Rekha knows every local family and mountain spring. We felt in safe, expert hands every day.'
            ),

            # 3. Ramesh Semwal (Uttarkashi)
            Review(
                user_id=traveler3.id,
                target_type='guide',
                target_id=guides_data[2].id,
                rating=5,
                comment='Ramesh accompanied our group along the Dayara Bugyal meadows and Gartang Gali cliff trail in Uttarkashi. His botanical knowledge of alpine flora and Himalayan medicinal plants made every kilometer fascinating.'
            ),
            Review(
                user_id=traveler4.id,
                target_type='guide',
                target_id=guides_data[2].id,
                rating=5,
                comment='Exceptional naturalist. Ramesh knows the Garhwali legends behind every peak and waterfall along the Bhagirathi corridor.'
            ),
            Review(
                user_id=traveler2.id,
                target_type='guide',
                target_id=guides_data[2].id,
                rating=5,
                comment='Knowledgeable guide who respects the mountain ecology deeply. Paced the ascent up to Dayara Bugyal ridges perfectly.'
            ),

            # --- Destination Reviews ---
            # 1. Nainital
            Review(
                user_id=traveler2.id,
                target_type='destination',
                target_id=nainital.id,
                rating=5,
                comment='Nainital\'s emerald lake framed by the seven surrounding hills is majestic. Avoid the peak holiday weekends to experience the peaceful morning mist and quiet ridge trails of Ayarpatta and Cheena Peak.'
            ),
            Review(
                user_id=traveler5.id,
                target_type='destination',
                target_id=nainital.id,
                rating=5,
                comment='Evening aarti at Naina Devi Temple followed by a slow boat ride across the emerald waters is deeply calming. The colonial library on the Flats is worth visiting.'
            ),

            # 2. Almora
            Review(
                user_id=traveler.id,
                target_type='destination',
                target_id=almora.id,
                rating=5,
                comment='Almora is the cultural soul of Kumaon. Lala Bazar\'s 200-year-old stone shops, the Aipan artists, and authentic Bal Mithai from Mohan Singh Rautela are pure mountain treasures.'
            ),
            Review(
                user_id=traveler3.id,
                target_type='destination',
                target_id=almora.id,
                rating=5,
                comment='The cosmic geomagnetic energy at Kasar Devi is palpable. Peaceful trails through deodar and pine forests with uninterrupted Himalayan vistas of Trishul.'
            ),

            # 3. Munsiyari
            Review(
                user_id=traveler2.id,
                target_type='destination',
                target_id=munsiyari.id,
                rating=5,
                comment='The sheer proximity of the Panchachuli Five Peaks feels surreal. Pristine air, raw mountain beauty, and the gateway to high-altitude Himalayan wilderness.'
            ),
            Review(
                user_id=traveler.id,
                target_type='destination',
                target_id=munsiyari.id,
                rating=5,
                comment='A dream for mountain photographers. Sunrise over Panchachuli turning pink then gold is etched in my memory forever.'
            ),

            # 4. Jageshwar
            Review(
                user_id=traveler4.id,
                target_type='destination',
                target_id=jageshwar.id,
                rating=5,
                comment='Cluster of 124 ancient 7th to 12th-century stone temples nestled deep in a dense deodar grove. The architectural stone carvings and silence of the valley are divine.'
            ),

            # 5. Auli
            Review(
                user_id=traveler2.id,
                target_type='destination',
                target_id=auli.id,
                rating=5,
                comment='Spectacular ski slopes with the towering pyramid of Nanda Devi dominating the eastern horizon. The cable car ride from Joshimath is world-class.'
            ),

            # 6. Valley of Flowers
            Review(
                user_id=traveler3.id,
                target_type='destination',
                target_id=valley_of_flowers.id,
                rating=5,
                comment='A living tapestry of thousands of wild alpine blossoms between July and September. Truly feels like stepping into another realm.'
            ),

            # 7. Baleshwar Temple
            Review(
                user_id=traveler4.id,
                target_type='destination',
                target_id=baleshwar.id,
                rating=5,
                comment='The stone masonry of Baleshwar Temple rivals the finest medieval temples. Intricate celestial dancers and deities carved into basalt stone.'
            ),

            # 8. Abbott Mount
            Review(
                user_id=traveler5.id,
                target_type='destination',
                target_id=abbott_mount.id,
                rating=5,
                comment='One of Uttarakhand\'s best-kept secrets. Secluded church, towering Himalayan deodars, and views that stretch endlessly into Nepal.'
            ),
        ]
        db.session.add_all(reviews)

        # -----------------------------------------------------------
        # Sample Bookings
        # -----------------------------------------------------------
        bookings = [
            Booking(
                user_id=traveler.id,
                target_type='hotel',
                target_id=hotels_data[0].id,
                check_in=date(2026, 9, 20),
                check_out=date(2026, 9, 23),
                guests=2,
                total_amount=16500,
                status='confirmed',
                message='Lake view room preferred. Arriving by Kathgodam train.'
            ),
            Booking(
                user_id=traveler.id,
                target_type='guide',
                target_id=guides_data[0].id,
                check_in=date(2026, 9, 24),
                check_out=date(2026, 9, 25),
                guests=2,
                total_amount=5000,
                status='confirmed',
                message='Guided cultural walking tour of Jageshwar temple complex.'
            ),
        ]
        db.session.add_all(bookings)

        # -----------------------------------------------------------
        # Sample Trip
        # -----------------------------------------------------------
        sample_trip = Trip(
            user_id=traveler.id,
            title='Autumn in Kumaon: Almora and Nainital Trail',
            itinerary_json=json.dumps({
                "title": "Autumn in Kumaon: Almora and Nainital Trail",
                "summary": "A 4-day immersive cultural journey through lake country and heritage temples.",
                "days": [
                    {"day": 1, "theme": "Naini Lake and Old Town", "stops": [{"time": "Morning", "place": "Naini Lake", "activity": "Lakeside walk and boating", "tip": "Start at dawn"}]},
                    {"day": 2, "theme": "Almora Heritage and Aipan", "stops": [{"time": "Morning", "place": "Lala Bazar", "activity": "Explore old bazaars and taste Bal Mithai", "tip": "Visit Sarthi Sweets"}]}
                ]
            }),
            days=4,
            budget=18000,
            group_type='couple',
            interests='["culture", "food", "photography"]',
            start_city='Kathgodam',
            status='confirmed'
        )
        db.session.add(sample_trip)

        db.session.commit()

        # Synchronize Upcoming Festivals of Kumaon
        from app.sync_kumaon_festivals import sync as sync_kumaon_festivals
        sync_kumaon_festivals(app)

        # Populate all 51 district hotels across Uttarakhand with verified data
        from app.seed_all_location_hotels import arrange_all_hotels
        arrange_all_hotels()


        print("Beyond Tour database seeded successfully!")
        print(f"   -> {len(destinations)} destinations")
        print(f"   -> {len(festivals) + len(arts)} culture entries")
        print(f"   -> {len(foods)} food items")
        print(f"   -> {len(hotels_data)} hotels/homestays")
        print(f"   -> {len(guides_data)} guides")
        print(f"   -> {len(posts)} community posts")
        print(f"   -> {len(reviews)} reviews")
        print(f"   -> {len(bookings)} bookings")
        print("\n   Admin login: admin@beyondtour.in / admin@123")
        print("   Tourist login: priya@example.com / password123")
        print("   Business login: gopal@example.com / password123")


if __name__ == '__main__':
    seed()

"""
Updates Nainital destinations with:
1. Naini Lake (with lakenanital.png and rich story)
2. Naina Devi Temple (with NainaDeviTemple.png and rich story)
3. Mall Road Nainital (with Mallroad.png and rich story)
4. Naini Peak (with Naini_Peak.png and rich story)
5. Tiffin Top (with Tiffin_Top.png and rich story)
Also updates Nainital city hero image, culture entries, and district cards.
"""
from app import create_app
from app.extensions import db
from app.models import Destination, CultureEntry

def update_nainital():
    app = create_app()
    with app.app_context():
        # 1. Naini Lake (existing destination 1 or slug nainital)
        naini_lake = Destination.query.filter_by(slug='nainital').first()
        lake_story = (
            "The jewel of Kumaon and the sacred heart of the hill station, Naini Lake is a natural crescent-shaped "
            "freshwater lake cradled at 2,084m by seven majestic peaks (Sapta-Shring). In sacred Hindu mythology recorded in the "
            "Skanda Purana, the waterbody was known as 'Tririshi Sarovar'—carved by the great sages Atri, Pulastya, and Pulaha, "
            "who channeled sacred waters from Mount Kailash's holy Lake Mansarovar. It is also celebrated as the divine spot where "
            "Goddess Sati's left eye (Naina) fell as Lord Shiva danced in cosmic grief. Divided into Mallital (northern head) "
            "and Tallital (southern foot), the emerald waters mirror the floating silhouettes of heritage yachts, colorful wooden "
            "paddleboats, and mist-veiled cedar ridges."
        )
        if naini_lake:
            naini_lake.name = 'Naini Lake'
            naini_lake.description = lake_story
            naini_lake.cover_image_url = '/static/images/Nanital/lakenanital.png'
            naini_lake.best_time = 'March–June, September–November'
            naini_lake.featured = True
            print("Updated Naini Lake.")
        else:
            naini_lake = Destination(
                name='Naini Lake',
                slug='nainital',
                region='kumaon',
                category='lake',
                district='Nainital',
                lat=29.3919,
                lng=79.4542,
                altitude_m=2084,
                description=lake_story,
                cover_image_url='/static/images/Nanital/lakenanital.png',
                best_time='March–June, September–November',
                featured=True
            )
            db.session.add(naini_lake)
            print("Created Naini Lake.")

        # 2. Naina Devi Temple
        naina_devi = Destination.query.filter_by(slug='naina-devi-temple').first()
        naina_story = (
            "Standing venerated on the northern edge of Naini Lake at the Flatts, the sacred Naina Devi Temple is one "
            "of the revered Shakti Peethas of northern India. The sanctum sanctorum houses two divine eyes representing Goddess "
            "Naina Devi (Maa Durga), flanked by the fierce form of Maa Kali and Lord Ganesha. Following a tragic landslide in 1880 "
            "that swept away the ancient shrine, devout townspeople and hill communities rebuilt the present temple structure in 1883 "
            "with deep reverence. Every autumn during Bhadrapad Ashtami, the temple hosts the historic Nanda Devi Mela, where towering "
            "banana-trunk idols are paraded through lakeside lanes accompanied by the rhythmic clatter of Chholiya swords and conch "
            "shells before sacred ritual immersion into the lake."
        )
        if naina_devi:
            naina_devi.name = 'Naina Devi Temple'
            naina_devi.description = naina_story
            naina_devi.cover_image_url = '/static/images/Nanital/NainaDeviTemple.png'
            naina_devi.best_time = 'Year-round (Bhadrapad Ashtami for Nanda Devi Mela)'
            naina_devi.featured = True
            print("Updated Naina Devi Temple.")
        else:
            naina_devi = Destination(
                name='Naina Devi Temple',
                slug='naina-devi-temple',
                region='kumaon',
                category='temple',
                district='Nainital',
                lat=29.3950,
                lng=79.4510,
                altitude_m=2088,
                description=naina_story,
                cover_image_url='/static/images/Nanital/NainaDeviTemple.png',
                best_time='Year-round (Bhadrapad Ashtami for Nanda Devi Mela)',
                featured=True
            )
            db.session.add(naina_devi)
            print("Created Naina Devi Temple.")

        # 3. Mall Road Nainital
        mall_road = Destination.query.filter_by(slug='mall-road-nainital').first()
        mall_story = (
            "Constructed during British colonial rule in the mid-19th century, Mall Road—officially named Govind Ballabh Pant Marg—is "
            "the vibrant pedestrian artery connecting Tallital and Mallital along the tranquil shoreline of Naini Lake. Flanked by "
            "colonial-era lampposts, ornate wooden eaves, and lakefront benches, the promenade buzzes with mountain life. Visitors "
            "stroll past heritage bakeries like Sakley's, local wool markets offering hand-woven Pashminas, artisanal candle workshops "
            "renowned for aromatic hand-carved pillars, and traditional dhabas serving hot Pahadi Aloo ke Gutke. In the evening, traffic "
            "is halted to allow pedestrians to watch the twilight reflections of lakeside cottages glimmering over the darkening lake."
        )
        if mall_road:
            mall_road.name = 'Mall Road Nainital'
            mall_road.description = mall_story
            mall_road.cover_image_url = '/static/images/Nanital/Mallroad.png'
            mall_road.best_time = 'Year-round (evenings for leisurely lakeside strolls)'
            mall_road.featured = True
            print("Updated Mall Road Nainital.")
        else:
            mall_road = Destination(
                name='Mall Road Nainital',
                slug='mall-road-nainital',
                region='kumaon',
                category='heritage',
                district='Nainital',
                lat=29.3900,
                lng=79.4580,
                altitude_m=2080,
                description=mall_story,
                cover_image_url='/static/images/Nanital/Mallroad.png',
                best_time='Year-round (evenings for leisurely lakeside strolls)',
                featured=True
            )
            db.session.add(mall_road)
            print("Created Mall Road Nainital.")

        # 4. Naini Peak (China Peak)
        naini_peak = Destination.query.filter_by(slug='naini-peak').first()
        peak_story = (
            "Perched at a commanding elevation of 2,615 meters (8,579 ft), Naini Peak—historically known as Cheena Peak—is the highest "
            "summit in the Nainital hills. The rewarding 6-kilometer trail winds through canopies of Himalayan cypress, oak, deodar cedar, "
            "and blooming red rhododendrons, alive with the calls of kalij pheasants and Himalayan black-throated jays. At the summit, "
            "hikers are greeted with a panoramic 360-degree vista: looking north across a 300-kilometer horizon of snowcapped Himalayan "
            "giants from Bandarpoonch to Nanda Devi and Trishul, and looking south onto the entire jewel-like emerald basin of Naini Lake "
            "nestled far below in the valley."
        )
        if naini_peak:
            naini_peak.name = 'Naini Peak (China Peak)'
            naini_peak.description = peak_story
            naini_peak.cover_image_url = '/static/images/Nanital/Naini_Peak.png'
            naini_peak.best_time = 'October–June (morning hours for crystalline Himalayan views)'
            naini_peak.featured = True
            print("Updated Naini Peak.")
        else:
            naini_peak = Destination(
                name='Naini Peak (China Peak)',
                slug='naini-peak',
                region='kumaon',
                category='trek',
                district='Nainital',
                lat=29.4167,
                lng=79.4500,
                altitude_m=2615,
                description=peak_story,
                cover_image_url='/static/images/Nanital/Naini_Peak.png',
                best_time='October–June (morning hours for crystalline Himalayan views)',
                featured=True
            )
            db.session.add(naini_peak)
            print("Created Naini Peak.")

        # 5. Tiffin Top (Dorothy's Seat)
        tiffin_top = Destination.query.filter_by(slug='tiffin-top').first()
        tiffin_story = (
            "Located atop the Ayarpatta hill at an altitude of 2,292 meters (7,520 ft), Tiffin Top is celebrated as one of Nainital's "
            "most scenic picnic knolls and tranquil forest viewpoints. At its summit stands 'Dorothy's Seat'—a stone memorial masonry bench "
            "erected by British officer Col. J.P. Kellett in memory of his artist wife Dorothy Kellett, who spent days painting the mountain "
            "landscapes from this cliffside knoll. The 4 km trek from the town center winds through moss-draped deodar woods and terraced "
            "farmland, opening up onto majestic panoramic vistas of the Kumaon countryside, Nainital valley, and distant snow peaks glistening "
            "under the mountain sun."
        )
        if tiffin_top:
            tiffin_top.name = "Tiffin Top (Dorothy's Seat)"
            tiffin_top.description = tiffin_story
            tiffin_top.cover_image_url = '/static/images/Nanital/Tiffin_Top.png'
            tiffin_top.best_time = 'March–June, September–November'
            tiffin_top.featured = True
            print("Updated Tiffin Top.")
        else:
            tiffin_top = Destination(
                name="Tiffin Top (Dorothy's Seat)",
                slug='tiffin-top',
                region='kumaon',
                category='trek',
                district='Nainital',
                lat=29.3833,
                lng=79.4417,
                altitude_m=2292,
                description=tiffin_story,
                cover_image_url='/static/images/Nanital/Tiffin_Top.png',
                best_time='March–June, September–November',
                featured=True
            )
            db.session.add(tiffin_top)
            print("Created Tiffin Top.")

        db.session.flush()

        # Update Culture Entries for Nainital
        nanda_devi_entry = CultureEntry.query.filter_by(slug='nanda-devi-mela-nainital').first()
        if nanda_devi_entry:
            nanda_devi_entry.cover_image_url = '/static/images/Nanital/NainaDeviTemple.png'
            if naina_devi:
                nanda_devi_entry.destination_id = naina_devi.id
            print("Updated Nanda Devi Mela culture entry image and destination link.")

        carnival_entry = CultureEntry.query.filter_by(slug='nainital-winter-carnival').first()
        if carnival_entry:
            carnival_entry.cover_image_url = '/static/images/Nanital/Mallroad.png'
            print("Updated Nainital Winter Carnival culture entry image.")

        db.session.commit()
        print("Nainital destinations successfully updated!")

if __name__ == '__main__':
    update_nainital()

"""
Curated dataset and helpers for the 'Upcoming Festivals of Kumaon' section.
Accurate dates, rich cultural storytelling, authentic 16:9 photographic imagery,
stay/homestay connections, how-to-reach transport guides, celebration venues,
and celebration duration for Uttarakhand tourism.
"""

KUMAON_UPCOMING_FESTIVALS = [
    {
        'id': 'nanda-devi-mela',
        'title': 'Nanda Devi Mela',
        'slug': 'nanda-devi-mela',
        'date': 'Around 16–20 September 2026',
        'important_date': 'Nanda Ashtami – 19 September 2026',
        'badge_date': '16–20 Sep 2026',
        'duration': '5 to 7 Days (Main Fair: 16–20 Sep; Peak Nanda Ashtami on 19 Sep)',
        'location': 'Almora & Nainital',
        'celebration_venue': 'Almora: Historic Malla Mahal Fort & Nanda Devi Temple, Lala Bazaar | Nainital: Flats Ground & Naina Devi Temple lakeside promenade',
        'district_filter_key': 'almora',
        'season_filter': 'september',
        'month_name': 'September',
        'month_number': 9,
        'image': '/static/images/festivals/nanda_devi_mela.jpg',
        'short_story': 'Nanda Devi is one of the most revered goddesses of Kumaon and is deeply connected with the cultural heritage of the region. During the festival, beautifully decorated Nanda and Sunanda dolas are carried in colourful processions accompanied by traditional music, devotees and local celebrations.',
        'full_story': """For centuries, the royal and folk communities of Kumaon have worshipped Goddess Nanda Devi as their supreme guardian and sister of the mountain heights. Held annually during Bhadrapad Ashtami, the historic fair dates back to the 16th-century Chand dynasty when King Kalyan Chand established royal court rituals inside Almora's Malla Mahal fort.

The most sacred moment of the festival is the sculpting of the twin murtis of Nanda and Sunanda from chosen wild banana trunks brought from auspicious village forests. Priests paint the deities' compassionate features behind closed temple sanctums before unveiling them to tens of thousands of cheering devotees.

The grand dola palanquin is carried through the cobblestone lanes of Almora and the lakeside Flats in Nainital, accompanied by Chholiya sword dancers, the deep resonance of brass Ransingha horns, and community Jhora-Chanchari folk singing that unites every valley of Kumaon.""",
        'what_to_experience': [
            'Nanda-Sunanda Dola procession',
            'Kumaoni folk music',
            'Traditional costumes',
            'Local food',
            'Handicraft markets',
            'Temple traditions'
        ],
        'highlights': [
            'Sacred Banana-Trunk Idols carved and painted by hereditary priests',
            'Spectacular Chholiya Sword Dance and Ransingha brass horns',
            'Historic Almora Lala Bazaar & Nainital Flatts processions'
        ],
        'how_to_reach': {
            'nearest_airport': 'Pantnagar Airport (PGH) — 115 km to Almora (~3.5 hrs drive) / 70 km to Nainital (~2 hrs drive). Scheduled flights from New Delhi.',
            'nearest_railway': 'Kathgodam Railway Station (KGM) — 85 km to Almora (~2.5 hrs) / 34 km to Nainital (~1 hr). Key daily trains: Kathgodam Shatabdi Express (12040) and Ranikhet Express (15014) from New Delhi.',
            'by_road': 'Direct connectivity via NH 109 from New Delhi (360 km, 7–8 hrs). Regular UTC Volvo and Deluxe buses run from ISBT Anand Vihar, Delhi to Haldwani, Nainital, and Almora.',
            'local_commute': 'Frequent shared Maxx cabs and taxis from Kathgodam/Haldwani taxi stand. Special pedestrian festival shuttles run from outer parking zones to Almora Lala Bazaar and Nainital Mall Road.'
        },
        'nearby_attractions': [
            {'name': 'Chitai Golu Devta Temple', 'url': '/destinations/23'},
            {'name': 'Kasar Devi Temple', 'url': '/destinations/22'},
            {'name': 'Naini Lake', 'url': '/destinations/1'},
            {'name': 'Naina Devi Temple', 'url': '/destinations/18'}
        ],
        'local_food': [
            'Singodi wrapped in fresh Malu leaves',
            'Traditional roasted Bal Mithai from Lala Bazaar',
            'Spiced Pahadi Aloo ke Gutke with hemp chutney',
            'Hot ginger Pahadi Chai'
        ],
        'travel_info': 'Almora is ~90 km and Nainital is ~35 km from Kathgodam Railway Station. Sturdy walking shoes are essential for exploring the festive cobblestone streets. Book lakeside and heritage homestays 3–4 weeks ahead.',
        'photo_gallery': [
            '/static/images/festivals/nanda_devi_mela.jpg',
            '/static/images/Almora/nandadevi.png',
            '/static/images/Nanital/NainaDeviTemple.png',
            '/static/images/Almora/almora.png'
        ]
    },
    {
        'id': 'khatarua',
        'title': 'Khatarua',
        'slug': 'khatarua-festival',
        'date': '17 September 2026',
        'important_date': '17 September 2026 (Ashwin Sankranti)',
        'badge_date': '17 Sep 2026',
        'duration': '1 Day & Evening (Ashwin Sankranti harvest festival)',
        'location': 'Kumaon villages, Uttarakhand',
        'celebration_venue': 'Terraced village courtyards, traditional cattle sheds (gaushalas), and panoramic hilltop ridges across Almora, Nainital, Bageshwar, and Champawat',
        'district_filter_key': 'almora',
        'season_filter': 'september',
        'month_name': 'September',
        'month_number': 9,
        'image': '/static/images/festivals/khatarua.jpg',
        'short_story': 'Khatarua marks the transition from the monsoon season toward autumn. Traditionally, Kumaoni communities celebrate with bonfires, livestock-related rituals and seasonal customs, reflecting the close relationship between mountain communities, agriculture and nature.',
        'full_story': """Khatarua is an intimate pastoral festival celebrated across the terraced valleys and stone hamlets of Kumaon on the first day of the Hindu solar month of Ashwin. Originating from ancient agricultural traditions and historical Chand military victories, the festival marks the retreat of heavy monsoon rains and the onset of crisp Himalayan autumn.

Throughout the day, farmers thoroughly clean and decorate their stone cowsheds (gaushalas) and pamper cattle with fresh green grass and cucumber slices as an expression of gratitude.

At twilight, villagers gather atop hillocks and courtyards to light towering bonfires (Khatarua pyres) made of dry grass, pine needles, and wooden twigs. Villagers dance around the glowing flames chanting traditional folk couplets to invoke warmth, drive away agricultural pests, and bless the herds for the upcoming winter.""",
        'what_to_experience': [
            'Traditional bonfires',
            'Village celebrations',
            'Livestock traditions',
            'Kumaoni food',
            'Rural Himalayan culture'
        ],
        'highlights': [
            'Hilltop community bonfires lighting up valley ridges',
            'Ancient livestock blessing ceremonies in traditional stone gaushalas',
            'Folk chants celebrating the autumn transition'
        ],
        'how_to_reach': {
            'nearest_airport': 'Pantnagar Airport (PGH) — ~110–130 km to central Kumaoni homestay villages (~3.5 hrs drive).',
            'nearest_railway': 'Kathgodam Railway Station (KGM) — 80–110 km connecting to rural village clusters. Regular Shatabdi & overnight mail trains from Delhi.',
            'by_road': 'Scenic mountain drives via NH 109 through Bhowali, Khairna, and Almora connecting rural village links.',
            'local_commute': 'Shared local utility jeeps (Maxx) from Almora, Ranikhet, or Bageshwar main bazaars connect directly to interior farming hamlets.'
        },
        'nearby_attractions': [
            {'name': 'Binsar Wildlife Sanctuary', 'url': '/destinations/6'},
            {'name': 'Jageshwar Dham', 'url': '/destinations/4'},
            {'name': 'Almora Heritage Town', 'url': '/destinations/2'}
        ],
        'local_food': [
            'Crisp mountain Kakdi (cucumber) with spiced yellow mustard salt (Pisi Loon)',
            'Bhatt ki Churkani cooked in cast-iron kadhais',
            'Traditional Mandua (finger millet) rotis with fresh cow ghee'
        ],
        'travel_info': 'Best experienced through village homestays in Binsar, Almora, and Mukteshwar. Evenings turn pleasantly crisp in mid-September; carry a light woolen jacket or fleece.',
        'photo_gallery': [
            '/static/images/festivals/khatarua.jpg',
            '/static/images/Almora/almora.png',
            '/static/images/champwat/champawat.png'
        ]
    },
    {
        'id': 'kumaoni-dussehra',
        'title': 'Kumaoni Dussehra & Ramlila',
        'slug': 'kumaoni-dussehra-ramlila',
        'date': 'October 2026',
        'important_date': 'Dussehra – 20 October 2026',
        'badge_date': 'Oct 2026',
        'duration': '10 to 11 Nights (Nightly operatic performances throughout Navratri to Vijayadashami)',
        'location': 'Almora and other Kumaon towns',
        'celebration_venue': 'Historic town squares and open-air Ramlila stages in Almora (Badreshwar, Lala Bazaar, Nanda Devi ground, Malla Mahal), Nainital Flats, and Ranikhet',
        'district_filter_key': 'almora',
        'season_filter': 'october',
        'month_name': 'October',
        'month_number': 10,
        'image': '/static/images/festivals/kumaoni_ramlila.jpg',
        'short_story': 'Dussehra in Kumaon is closely associated with the region\'s famous Ramlila traditions. Communities come together for theatrical performances based on the Ramayana, combining storytelling, music, traditional costumes and devotional culture.',
        'full_story': """Kumaon's musical Ramlila is an intangible cultural marvel that traces its origin over 160 years back to the cultural renaissance of Almora under patron Badri Datt Joshi in 1860. Recognized by UNESCO as one of the world's representative cultural masterpieces, Kumaoni Ramlila blends classical Hindustani ragas with dramatic mountain operatic singing.

For ten nights leading to Dussehra, open-air amphitheatres and town chowks echo with poetic verses sung live by local actors dressed in resplendent brocades and ornate wooden masks.

The culmination on Vijayadashami features magnificent, towering bamboo and paper-mache effigies created by neighborhood artisan guilds (mohallas), paraded through Almora's narrow ridges in a grand carnival before their ceremonial bonfire under the stars.""",
        'what_to_experience': [
            'Traditional Ramlila',
            'Folk music',
            'Traditional costumes',
            'Night performances',
            'Local celebrations'
        ],
        'highlights': [
            '160-year-old classical raga singing and poetic Hindi-Kumaoni dialogue',
            'Elaborate wooden masks and traditional brocade royal attire',
            'Spectacular multi-neighborhood effigy street parade in Almora'
        ],
        'how_to_reach': {
            'nearest_airport': 'Pantnagar Airport (PGH) — 115 km from Almora (~3.5 hrs drive). Taxis easily available outside the terminal.',
            'nearest_railway': 'Kathgodam Railway Station (KGM) — 85 km from Almora (~2.5 hrs). Direct trains: Kathgodam Shatabdi (12040) and Ranikhet Express (15014).',
            'by_road': 'Overnight AC Volvo buses from ISBT Anand Vihar, Delhi to Almora / Haldwani via Rampur, Bilaspur, and Kathgodam.',
            'local_commute': 'Within Almora town, all primary Ramlila stages (Badreshwar, Malla Mahal, Lala Bazaar) are easily accessible on foot through pedestrian heritage lanes.'
        },
        'nearby_attractions': [
            {'name': 'Almora Heritage Town', 'url': '/destinations/2'},
            {'name': 'Katarmal Sun Temple', 'url': '/destinations/2'},
            {'name': 'Kasar Devi Temple', 'url': '/destinations/22'}
        ],
        'local_food': [
            'Festive Jalebis and hot milk in clay kulhads',
            'Singori sweets wrapped in Malu leaves',
            'Dubuk and spicy Kumaoni cucumber raita'
        ],
        'travel_info': 'October brings crystal-clear autumn skies with breathtaking mountain views. Book accommodations within walking distance of Almora town squares to attend evening performances.',
        'photo_gallery': [
            '/static/images/festivals/kumaoni_ramlila.jpg',
            '/static/images/Almora/almora.png',
            '/static/images/Almora/nandadevi.png'
        ]
    },
    {
        'id': 'kumaoni-diwali',
        'title': 'Kumaoni Diwali',
        'slug': 'kumaoni-diwali',
        'date': '8 November 2026',
        'important_date': '8 November 2026 (Kartik Amavasya)',
        'badge_date': '8 Nov 2026',
        'duration': '2 to 3 Days (Dhanteras, Main Diwali on 8 Nov, and Govardhan celebrations)',
        'location': 'Kumaon region',
        'celebration_venue': 'Traditional slate-roofed mountain homes, village courtyards, threshold stone doorframes decorated with Aipan art, and local bazaars across Kumaon',
        'district_filter_key': 'nainital',
        'season_filter': 'november',
        'month_name': 'November',
        'month_number': 11,
        'image': '/static/images/festivals/kumaoni_diwali.jpg',
        'short_story': 'Diwali brings homes and villages across Kumaon alive with lamps, traditional decorations, family rituals and local food. Kumaoni celebrations can also feature beautiful Aipan designs, adding a distinctive regional identity to the festival.',
        'full_story': """In the Himalayan ridges of Kumaon, Diwali is an intimate, sacred communion between family, home, and nature. Unlike noisy metropolitan celebrations, mountain Diwali is characterized by the warm flicker of thousands of terracotta diyas lining slate roofs, carved deodar balconies, and terrace stone walls.

The heart of the festival lies in the ancient Aipan art tradition. Women coat the threshold and prayer room with red-ochre Geru clay, drawing sacred linear motifs using rice paste (Biswar) applied with the ring finger. Special patterns like Lakshmi Chowk, lotus petals, and divine footsteps lead from the courtyard to the home shrine.

Families gather around wood chulhas to share freshly fried Singal sweets, hot Kheer, and savory pahadi delicacies while prayer bells ring peacefully across the misty valleys.""",
        'what_to_experience': [
            'Traditional Aipan art',
            'Diyas and decorations',
            'Kumaoni sweets and food',
            'Village celebrations',
            'Local markets'
        ],
        'highlights': [
            'Sacred Aipan floor art drawn with fermented rice paste and red ochre',
            'Terracotta oil lamps glowing along village mountain terraces',
            'Authentic community family feasts in stone mountain homestays'
        ],
        'how_to_reach': {
            'nearest_airport': 'Pantnagar Airport (PGH) — 70 km to Nainital, 115 km to Almora.',
            'nearest_railway': 'Kathgodam Railway Station (KGM) — 34 km to Nainital / 85 km to Almora. Frequent trains connect to Delhi, Moradabad, and Bareilly.',
            'by_road': 'NH 109 from New Delhi (310–360 km, approx. 7 hrs drive) through scenic pine forests.',
            'local_commute': 'Private taxis, mountain cabs, and local bus services connect hill stations and rural homestay clusters.'
        },
        'nearby_attractions': [
            {'name': 'Kasar Devi Temple', 'url': '/destinations/22'},
            {'name': 'Jageshwar Dham', 'url': '/destinations/4'},
            {'name': 'Naini Lake', 'url': '/destinations/1'}
        ],
        'local_food': [
            'Crispy fried Singal (sweet semolina rings)',
            'Rich mountain Kheer prepared with local cow milk and dry fruits',
            'Gahat ke Paranthe with fresh homemade churned butter'
        ],
        'travel_info': 'November in Kumaon brings chilly nights (5°C–10°C) with starry skies and daytime warmth (18°C). Carry warm woolens, thermals, and windbreakers.',
        'photo_gallery': [
            '/static/images/festivals/kumaoni_diwali.jpg',
            '/static/images/Almora/almora.png',
            '/static/images/Nanital/lakenanital.png'
        ]
    },
    {
        'id': 'egaas-bagwal',
        'title': 'Egaas Bagwal',
        'slug': 'egaas-bagwal',
        'date': '20 November 2026',
        'important_date': '20 November 2026 (Haribodhini Ekadashi)',
        'badge_date': '20 Nov 2026',
        'duration': '1 Full Day & Night (Celebrated exactly 11 days after Diwali on Haribodhini Ekadashi)',
        'location': 'Kumaon villages',
        'celebration_venue': 'Village community courtyards, agricultural threshing floors (khaliyaan), and mountain temple precincts across Almora, Champawat, and Bageshwar',
        'district_filter_key': 'champawat',
        'season_filter': 'november',
        'month_name': 'November',
        'month_number': 11,
        'image': '/static/images/festivals/egaas_bagwal.jpg',
        'short_story': 'Egaas Bagwal is popularly known as the “Second Diwali” in Uttarakhand. Traditionally celebrated eleven days after Diwali, the festival is associated with communities celebrating together after people who had been away returned home. It is marked by lamps, traditional food, music and community gatherings.',
        'full_story': """Egaas Bagwal—celebrated on the eleventh day after Diwali (Igas or Haribodhini Ekadashi)—is an indigenous festival deeply rooted in the folklore of Uttarakhand. According to legend, the news of Lord Rama's return to Ayodhya reached the deep, isolated Himalayan valleys eleven days late; another beloved regional account marks the triumphant return of mountain commander Madho Singh Bhandari from northern battles.

On this night, villagers illuminate their stone houses with mustard oil lamps and gather in open community fields.

The central ritual is the spinning of "Bhailo"—bundles of resinous pine wood bound with mountain grass ropes that are ignited and spun in mesmerizing circular fire trails by youth. The celebration echoes with traditional folk dances like Jhora and Chanchari, uniting entire valleys in community camaraderie.""",
        'what_to_experience': [
            'Traditional lamps',
            'Kumaoni food',
            'Folk songs',
            'Village gatherings',
            'Local traditions'
        ],
        'highlights': [
            'The thrilling Bhailo spinning fire dance under starry night skies',
            'Community circle dancing to the beat of Dhol-Damau folk drums',
            'Heartfelt village homecoming feasts and story-sharing'
        ],
        'how_to_reach': {
            'nearest_airport': 'Pantnagar Airport (PGH) — 135 km to Champawat / 115 km to Almora.',
            'nearest_railway': 'Tanakpur Railway Station (TPU) — 75 km to Champawat | Kathgodam Railway Station (KGM) — 85 km to Almora / 140 km to Champawat.',
            'by_road': 'Scenic mountain roads via Tanakpur–Champawat highway or Kathgodam–Dhanachuli–Lohaghat corridor.',
            'local_commute': 'Shared local utility jeeps and mountain taxis connect block centers to interior villages.'
        },
        'nearby_attractions': [
            {'name': 'Baleshwar Temple Champawat', 'url': '/destinations/14'},
            {'name': 'Shyamlatal Lake', 'url': '/destinations/17'},
            {'name': 'Chitai Golu Devta Temple', 'url': '/destinations/23'}
        ],
        'local_food': [
            'Patode (steamed & crisped colocasia leaf rolls with spices)',
            'Gahat (Horsegram) stuffed puris and rotis',
            'Sweet Jhangora (Barnyard millet) kheer'
        ],
        'travel_info': 'Celebrated with exceptional vibrancy in rural villages across Kumaon. Visiting an eco-homestay in Champawat, Almora, or Bageshwar provides an authentic insider perspective.',
        'photo_gallery': [
            '/static/images/festivals/egaas_bagwal.jpg',
            '/static/images/champwat/champawat.png',
            '/static/images/Almora/almora.png'
        ]
    },
    {
        'id': 'uttarayani-fair',
        'title': 'Uttarayani Fair',
        'slug': 'uttarayani-fair-bageshwar',
        'date': '14 January 2027',
        'important_date': '14 January 2027 (Makar Sankranti)',
        'badge_date': '14 Jan 2027',
        'duration': '7 Days (Begins on Makar Sankranti, 14 January 2027, continuing for one full week)',
        'location': 'Bageshwar',
        'celebration_venue': 'Sacred River Confluence (Sangam) of Saryu and Gomti rivers at the 8th-century Bagnath Temple grounds, Bageshwar town',
        'district_filter_key': 'bageshwar',
        'season_filter': 'january',
        'month_name': 'January',
        'month_number': 1,
        'image': '/static/images/festivals/uttarayani_fair.jpg',
        'short_story': 'Uttarayani is celebrated around Makar Sankranti and is one of Kumaon\'s important traditional fairs. The famous celebration at Bageshwar takes place near the confluence of the Saryu and Gomti rivers and brings together pilgrims, traders, artisans and performers.',
        'full_story': """The Uttarayani Fair in Bageshwar is Kumaon's most ancient and culturally significant winter mela, held at the holy Sangam where the sacred Saryu and Gomti rivers meet. Since antiquity, trans-Himalayan Bhotia traders from Tibet and higher valleys traveled across snow passes to barter handwoven Dan carpets, sheep wool shawls, and rare mountain herbs for lowland grain and iron.

During Uttarayani, thousands of pilgrims take ritual dawn dips in the sacred river confluence before visiting the 8th-century stone temple of Lord Bagnath (Shiva).

The river ghats transform into a bustling open-air craft bazaar filled with bell-makers, copper smiths, and folk performers. Children celebrate Kale Kauva, offering fried sweet dough twists (Ghughuti) to crows while singing traditional invitations.""",
        'what_to_experience': [
            'Bageshwar fair',
            'Saryu–Gomti confluence',
            'Folk music',
            'Traditional handicrafts',
            'Local food',
            'Temple visit'
        ],
        'highlights': [
            'Sacred confluence river bath and worship at 8th-century Bagnath Temple',
            'Bhotia tribal craft market featuring hand-knotted woolen Dan rugs',
            'Traditional Ghughuti and Kale Kauva folk songs sung by children'
        ],
        'how_to_reach': {
            'nearest_airport': 'Pantnagar Airport (PGH) — 180 km from Bageshwar (approx. 5.5 hrs drive via Almora and Kausani).',
            'nearest_railway': 'Kathgodam Railway Station (KGM) — 150 km from Bageshwar (approx. 4.5–5 hrs drive). Direct trains: Kathgodam Shatabdi and Ranikhet Express from New Delhi.',
            'by_road': 'Well-connected via NH 309A from Almora (70 km) and Haldwani (155 km). Regular UTC state buses and private coaches depart from Haldwani and Almora bus depots.',
            'local_commute': 'Frequent shared Maxx cabs operate between Kathgodam, Almora, Kausani, and Bageshwar bus stand daily.'
        },
        'nearby_attractions': [
            {'name': 'Bagnath Temple Bageshwar', 'url': '/destinations/2'},
            {'name': 'Baijnath Temple Complex', 'url': '/destinations/4'},
            {'name': 'Kausani Heritage & Tea Gardens', 'url': '/destinations/5'}
        ],
        'local_food': [
            'Ghughuti (sweet fried dough treats shaped into spirals)',
            'Traditional Khichdi served with pure mountain cow ghee',
            'Til ke Laddu (sesame jaggery sweets)'
        ],
        'travel_info': 'Bageshwar is situated 150 km from Kathgodam. January temperatures range from 3°C to 14°C; bring heavy thermal woolens, beanies, and insulated footwear.',
        'photo_gallery': [
            '/static/images/festivals/uttarayani_fair.jpg',
            '/static/images/Almora/jagwasher.png',
            '/static/images/Almora/almora.png'
        ]
    },
    {
        'id': 'phool-dei',
        'title': 'Phool Dei',
        'slug': 'phool-dei-festival',
        'date': 'March 2027',
        'important_date': 'Around 14–15 March 2027 (Chaitra Sankranti)',
        'badge_date': 'Mar 2027',
        'duration': '1 to 3 Days (First days of Hindu month Chaitra marking the arrival of Himalayan spring)',
        'location': 'Kumaon villages',
        'celebration_venue': 'Doorsteps of traditional stone mountain homes, temple thresholds, and terraced orchard hamlets across Kumaon villages (Almora, Nainital, Bageshwar, Champawat)',
        'district_filter_key': 'almora',
        'season_filter': 'spring',
        'month_name': 'March',
        'month_number': 3,
        'image': '/static/images/festivals/phool_dei.jpg',
        'short_story': 'Phool Dei welcomes the arrival of spring in the Himalayan region. Children traditionally collect colourful flowers and place them at the entrances of homes while offering blessings for prosperity and happiness. Families respond with traditional sweets and treats.',
        'full_story': """Phool Dei is an endearing spring festival celebrating the flowering of the Himalayas on the first day of the Chaitra month. As winter thaws give way to emerald terraced fields and wild scarlet Rhododendrons (Buransh) and yellow Pyoli blooms carpet the hill slopes, young village children assume the sacred role of "Phoolyari" (flower-bearers).

At dawn, children carry handcrafted ringal baskets and brass plates loaded with freshly picked petals, green wheat shoots, and uncooked rice.

They wander from house to house, showering doorstep thresholds with vibrant petals and singing the melodious blessing: "Phool Dei, Chhamma Dei, Deno Dwar, Bhartu Bhakar" (May flowers bring joy and peace, and may your granaries be always full). Welcoming elders reward the children with coins, gur, and fresh sweet Sei pudding.""",
        'what_to_experience': [
            'Spring flowers',
            'Kumaoni village life',
            'Traditional clothing',
            'Local sweets',
            'Children\'s celebrations',
            'Himalayan nature'
        ],
        'highlights': [
            'Village children singing the ancient "Phool Dei, Chhamma Dei" threshold blessings',
            'Morning wildflower gathering walks through blooming rhododendron forests',
            'Freshly prepared Sei pudding and floral hospitality in mountain homes'
        ],
        'how_to_reach': {
            'nearest_airport': 'Pantnagar Airport (PGH) — 70–120 km depending on valley destination (~2.5–3.5 hrs drive).',
            'nearest_railway': 'Kathgodam Railway Station (KGM) — 34–90 km connecting Nainital, Almora, Mukteshwar, and Ranikhet valleys.',
            'by_road': 'NH 109 and scenic pine-lined mountain highways through blossoming rhododendron forest corridors.',
            'local_commute': 'Shared local jeeps, village walking paths, and taxi operators connect central hill stations with surrounding hamlets.'
        },
        'nearby_attractions': [
            {'name': 'Kausani Scenic Ridge', 'url': '/destinations/5'},
            {'name': 'Binsar Forest Sanctuary', 'url': '/destinations/6'},
            {'name': 'Mukteshwar Orchards', 'url': '/destinations/1'}
        ],
        'local_food': [
            'Sei (festive sweet pudding of roasted rice flour, curd, and jaggery)',
            'Freshly squeezed Buransh (rhododendron blossom) mountain cordial',
            'Sweet Singodi wrapped in fragrant green Malu leaves'
        ],
        'travel_info': 'Mid-March offers pleasant, crisp spring days (14°C–22°C) with glorious clear views of snow-capped peaks and hills painted in bright red rhododendrons.',
        'photo_gallery': [
            '/static/images/festivals/phool_dei.jpg',
            '/static/images/Nanital/lakenanital.png',
            '/static/images/Almora/almora.png'
        ]
    },
    {
        'id': 'nanda-devi-raj-jat',
        'title': 'Shri Nanda Devi Raj Jat Yatra',
        'slug': 'nanda-devi-raj-jat',
        'date': '5 – 23 September 2026',
        'important_date': 'Homkund Maha-Hawan (Nanda Ashtami) – 19 September 2026',
        'badge_date': '5–23 Sep 2026',
        'duration': '19 to 22 Days (5–23 Sep 2026; Homkund Culmination: 19 Sep 2026)',
        'location': 'Chamoli & Kumaon Confluence',
        'celebration_venue': 'Nauti Village (Base Temple) · Nandkeshari (Kumaon-Garhwal Confluence) · Wan Village (Latu Devta) · Bedni Bugyal · Roopkund · Homkund Lake (4,061 m) at Mount Trishul',
        'district_filter_key': 'chamoli',
        'season_filter': 'september',
        'month_name': 'September',
        'month_number': 9,
        'image': '/static/images/Almora/nandadevi.png',
        'short_story': 'Known as the Himalayan Mahakumbh, the Nanda Devi Raj Jat is a legendary 280-km barefoot pilgrimage held once every 12 years. It portrays the intensely emotional bridal farewell (Vidaai) of Goddess Nanda Devi returning to Lord Shiva\'s abode beneath Mount Trishul, led by a miraculous four-horned ram.',
        'full_story': """The Nanda Devi Raj Jat is the supreme spiritual celebration of Uttarakhand, joining Garhwal and Kumaon in an unbroken 12-year bond.

The pilgrimage begins at Nauti village in Chamoli with the royal Golden Chhantoli (ringed umbrella) of Kasuwa royalty and the miraculous four-horned ram (Chausingha Khadu) born specifically before each pilgrimage. At Nandkeshari camp on the Pranmati river, the Kumaon procession bearing the holy Doli from Almora, Nainital, and Johar Valley unites with the Garhwal devotees in tears of shared devotion.

Beyond Wan village—the last human settlement—pilgrims walk barefoot across the velvet alpine carpets of Bedni Bugyal, pass the ancient glacial skeleton lake of Roopkund (4,778 m), cross the precipitous Jurangali crest (4,850 m), and reach the final sanctuary of Homkund (4,061 m) at the feet of Mount Trishul.

On Nanda Ashtami, following the sacred concluding Maha-Hawan, the four-horned ram is tearfully anointed and released: walking alone into the snows toward Mount Trishul, it vanishes into the eternal Himalayan mists.""",
        'what_to_experience': [
            '280-km barefoot high-Himalayan pilgrimage',
            'Miracle of the Four-Horned Ram (Chausingha Khadu)',
            'Sacred Golden Chhantoli royal umbrella',
            'Garhwal and Kumaon unity at Nandkeshari',
            'Bedni Bugyal alpine meadows & Vaitarini Kund',
            'Roopkund glacial tarn (4,778 m)',
            'Final sacred Hawan at Homkund (4,061 m)'
        ],
        'highlights': [
            '12-year sacred cycle uniting thousands of devotees across Uttarakhand',
            'Emotional Vidaai farewell of mountain daughter Goddess Nanda to Lord Shiva',
            'Miraculous guide: Four-Horned Ram walking unrestrained ahead of pilgrims'
        ],
        'how_to_reach': {
            'nearest_airport': 'Jolly Grant Airport, Dehradun (DED) — ~210 km to base camp at Karnaprayag/Nauti.',
            'nearest_railway': 'Rishikesh / Yog Nagari Rishikesh (YNRK) — ~190 km to Karnaprayag via NH 07. Regular road buses and mountain taxis connect along the Alaknanda river corridor.',
            'by_road': 'NH 07 from Rishikesh/Haridwar via Devprayag, Srinagar, and Rudraprayag to Karnaprayag (junction for Nauti and Wan base camps).',
            'local_commute': 'Shared local utility jeeps operate between Karnaprayag, Tharali, Deval, Mundoli, and Wan village (the roadhead).'
        },
        'nearby_attractions': [
            {'name': 'Bedni Bugyal', 'url': '/destinations'},
            {'name': 'Roopkund Lake', 'url': '/destinations'},
            {'name': 'Karnaprayag Confluence', 'url': '/destinations'}
        ],
        'local_food': [
            'Mandua (Finger millet) rotis with mountain ghee',
            'Bhatt ki Churkani and Pahadi Dal',
            'Warm Pahadi ginger tea with mountain honey'
        ],
        'travel_info': 'High-altitude acclimatization is strictly required. Leather items, plastic, and footwear are banned beyond Bedni Bugyal. Carry heavy thermal layers suitable for sub-zero temperatures.',
        'photo_gallery': [
            '/static/images/Almora/nandadevi.png',
            '/static/images/coverpic/gharwal.png',
            '/static/images/festivals/dyara_bugyal_holi.jpg'
        ]
    }
]


def get_kumaon_festivals():
    """Returns the curated list of Kumaon upcoming festivals."""
    return KUMAON_UPCOMING_FESTIVALS


def get_kumaon_festival_by_slug(slug):
    """Find a festival by slug or id."""
    slug_clean = str(slug).lower().strip()
    for f in KUMAON_UPCOMING_FESTIVALS:
        if f['slug'] == slug_clean or f['id'] == slug_clean:
            return f
        if slug_clean in ('nanda-devi-mela-nainital', 'nanda-devi-fair-almora') and f['id'] == 'nanda-devi-mela':
            return f
        if slug_clean in ('nanda-devi-raj-jat-yatra', 'nanda-raj-jat', 'raj-jat-yatra', 'raj-jat') and f['id'] == 'nanda-devi-raj-jat':
            return f
    return None


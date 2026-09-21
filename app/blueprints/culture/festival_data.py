"""
Centralized Cultural Dataset for 'Festivals & Living Culture of Uttarakhand'.
Authentic historical, geographical, and cultural information for 12 featured
Himalayan festivals & fairs and 6 living cultural disciplines.
"""

FEATURED_FESTIVALS = [
    {
        'id': 'bada-haat-mela',
        'slug': 'bada-haat-mela',
        'title': 'Bada Haat Mela',
        'subtitle': 'Ancient Himalayan Trade & Market Heritage',
        'region': 'garhwal',
        'region_name': 'Garhwal',
        'district': 'Uttarkashi',
        'location': 'Badahat / Uttarkashi town, Garhwal',
        'map_location_key': 'uttarkashi',
        'category': 'Traditional Fair & Trade Heritage',
        'type_key': 'fairs',
        'season': 'winter',
        'season_name': 'Winter / Makar Sankranti (14–21 Jan)',
        'date_display': '14 – 21 January 2027 (Makar Sankranti / Magh Mela)',
        'date_note': 'Celebrated annually during Makar Sankranti week along the sacred Bhagirathi River.',
        'verified': True,
        'image': '/static/images/festivals/bada_haat_mela.jpg',
        'image_attribution': 'Uttarakhand Tourism / Himalayan Cultural Archives',
        'short_story': 'Bada Haat, historically rooted in ancient Badahat, celebrates Uttarkashi\'s centuries-old legacy as a trans-Himalayan trade hub. The fair connected valley communities with Tibetan traders, offering handwoven wool, Himalayan herbs, and copper crafts alongside sacred temple processions.',
        'full_story': """Historically known as Badahat ("the great marketplace"), Uttarkashi was a vital trading outpost along ancient routes linking the Gangetic plains with high Himalayan passes and western Tibet. The Bada Haat Mela grew around the auspicious festival of Makar Sankranti as sheep herders, Bhotia merchants, and village artisans descended to the banks of the sacred Bhagirathi River.

The fair seamlessly blends religious reverence with bustling mountain commerce. Local deities (Doli devi-devtas) from surrounding mountain hamlets are carried down in palanquins with resonant beating of dhol and damau drums, offering their divine blessings to the congregation.

Today, Bada Haat remains an authentic window into Uttarakhand's pastoral barter and craft traditions, featuring handloom sheep-wool blankets (pankhis), Ringal bamboo work, mountain spices, and traditional Garhwali folk dances.""",
        'visitor_experience': [
            'Traditional Himalayan marketplace',
            'Local handicrafts & handlooms',
            'Wool and handmade products',
            'Folk music and cultural performances',
            'Religious deity palanquin processions',
            'Garhwali local food stalls',
            'Traditional village products'
        ],
        'cultural_significance': 'A living continuation of the ancient Indo-Tibetan trade trail and communal barter heritage, accompanied by traditional Garhwali devta doli blessings.',
        'where_to_experience': 'Ramleela Ground and riverside ghats of Uttarkashi along the Bhagirathi River.',
        'when_celebrated': '14–21 January annually (Next: 14 January 2027 during Makar Sankranti)',
        'local_tips': 'Look out for pure sheep-wool carpets (chutka) and freshly ground Himalayan mustard (jakhiya). Early mornings feature traditional riverbank prayers.'
    },
    {
        'id': 'rishi-muni-maharaj-mela',
        'slug': 'rishi-muni-maharaj-mela',
        'title': 'Rishi Muni Maharaj Mela',
        'subtitle': 'Sacred Deity Assembly of the Rawain Valley',
        'region': 'garhwal',
        'region_name': 'Garhwal',
        'district': 'Barkot / Uttarkashi',
        'location': 'Barkot, Rawain Valley, Garhwal',
        'map_location_key': 'barkot',
        'category': 'Religious Fair & Local Heritage',
        'type_key': 'fairs',
        'season': 'spring',
        'season_name': 'Spring / Pre-Summer (April)',
        'date_display': '18 – 20 April 2026 (Spring Assembly)',
        'date_note': 'Annual Rawain valley spring assembly held during Baisakhi / Chaitra transition.',
        'verified': True,
        'image': '/static/images/festivals/rishi_muni_mela.jpg',
        'image_attribution': 'Rawain Cultural Preservation Society / Local Archive',
        'short_story': 'A deeply revered spiritual gathering in the Rawain valley of Barkot, honoring Sage Muni Maharaj. Village deities converge in colorful palanquins amidst ancient rhythmic drumming, folk chants, and pastoral brotherhood.',
        'full_story': """The Rishi Muni Maharaj Mela is an authentic pastoral fair deeply rooted in the agrarian and spiritual worldview of the Rawain belt between the Yamuna and Tons river basins. Dedicated to Sage Muni Maharaj—venerated as the guardian hermit and spiritual anchor of these mountain slopes—the mela is an annual occasion of communal solidarity and village reconciliation.

Villagers from dozens of surrounding hamlets walk for hours across mountain ridges bearing wooden palanquins (Dolis) adorned with silks, brass masks (mohra), and silver tridents. The atmosphere resonates with the resonant clash of bronze thalis, dhol-damau, and ancient Raso dance circles.

Rather than commercialized tourism, this fair remains an intimate, community-governed Himalayan congregation where visitors are welcomed with generous mountain warmth and shared community feasts (bhandara).""",
        'visitor_experience': [
            'Local religious traditions & prayers',
            'Community gathering of 20+ village clans',
            'Traditional Rawain folk music & Raso dance',
            'Village culture & oral ballads',
            'Local mountain food & prasad',
            'Regional handcrafted woollens'
        ],
        'cultural_significance': 'Preserves the ancient Rawain socio-religious assembly tradition where regional grievances are dissolved and agricultural blessings invoked before seasonal sowing.',
        'where_to_experience': 'Barkot main temple precinct and surrounding valley grounds, Uttarkashi district.',
        'when_celebrated': 'Mid-April annually during spring sowing (Next: 18–20 April 2026)',
        'local_tips': 'Visitors must remove footwear before entering the deity ring. Modest traditional attire is appreciated by the village elders.'
    },
    {
        'id': 'dyara-bugyal-makha-holi',
        'slug': 'dyara-bugyal-makha-holi',
        'title': 'Dyara Bugyal Makha Holi',
        'subtitle': 'High-Altitude Meadow Butter & Folk Celebration',
        'region': 'garhwal',
        'region_name': 'Garhwal',
        'district': 'Uttarkashi',
        'location': 'Dyara Bugyal (3,048 m), Uttarkashi',
        'map_location_key': 'dyara-bugyal',
        'category': 'Folk Festival / Seasonal Mountain Culture',
        'type_key': 'seasonal',
        'season': 'summer',
        'season_name': 'Late Summer / Meadow Cycle (17–18 August)',
        'date_display': '17 – 18 August 2026 (Bhadon Sankranti / Butter Festival)',
        'date_note': 'Celebrated annually on Bhadrapada Sankranti (17–18 August) in high alpine meadows.',
        'verified': True,
        'image': '/static/images/festivals/dyara_bugyal_holi.jpg',
        'image_attribution': 'Raithal Ecotourism Cooperative / Village Archive',
        'short_story': 'Perched in the lush alpine meadows of Dyara at 3,000 meters, Makha Holi (popularly known as the Butter Festival or Anduri) is an ancient pastoral thanksgiving where shepherds celebrate the abundance of dairy by playing with fresh butter and milk.',
        'full_story': """High above the treeline in Uttarkashi lie the vast rolling velvet meadows of Dyara Bugyal, framed by the towering snow peaks of Bandarpoonch, Gangotri, and Black Peak. For centuries, the pastoral villages of Raithal and Barsu have migrated their cattle to these lush summer grasslands.

Makha Holi (Butter Festival) is the shepherd community\'s joyful expression of gratitude to Mother Nature and Lord Krishna for keeping their livestock safe and healthy during the high-altitude grazing season. Instead of artificial chemical colors, the villagers play with fresh, churned organic butter (makhan), buttermilk (chhaas), and mountain spring water.

Women and men dress in customary Garhwali attire—woollen coats, headscarves, and silver necklaces—dancing the spirited Raso and Tandi circle dances across emerald carpets of grass under crisp blue Himalayan skies.""",
        'visitor_experience': [
            'Traditional folk songs and shepherd ballads',
            'Communal Raso and Tandi circle dances',
            'Authentic playful celebration with churned butter',
            'Traditional Garhwali handwoven clothing',
            'Mountain pastoral village life in Raithal & Barsu',
            'Breathtaking high-altitude Himalayan meadow views'
        ],
        'cultural_significance': 'A nature-centric pastoral festival celebrating ecological harmony, dairy prosperity, and community gratitude to the mountain meadows.',
        'where_to_experience': 'Dyara Bugyal alpine meadow, reached via an 8 km trek from Raithal village near Uttarkashi.',
        'when_celebrated': '17–18 August 2026 (Bhadon Sankranti / Anduri Butter Festival)',
        'local_tips': 'Stay overnight in community-run homestays in Raithal village. Carry windproof jackets and eco-friendly reusable water containers.'
    },
    {
        'id': 'jauljibi-fair',
        'slug': 'jauljibi-fair',
        'title': 'Jauljibi Fair',
        'subtitle': 'Tri-Cultural Confluence at Kali and Gori Rivers',
        'region': 'kumaon',
        'region_name': 'Kumaon',
        'district': 'Pithoragarh',
        'location': 'Jauljibi, Kali–Gori River Confluence, Pithoragarh',
        'map_location_key': 'jauljibi',
        'category': 'Trade Fair & Cross-Border Culture',
        'type_key': 'fairs',
        'season': 'autumn',
        'season_name': 'Autumn / November (14–21 Nov)',
        'date_display': '14 – 21 November 2026 (Annual Trade Confluence)',
        'date_note': 'Annual 8-day trans-Himalayan trade confluence starting promptly on November 14.',
        'verified': True,
        'image': '/static/images/festivals/jauljibi_fair.jpg',
        'image_attribution': 'Pithoragarh District Cultural Council',
        'short_story': 'Held at the scenic sacred confluence of the roaring Kali and Gori rivers on the India-Nepal border, Jauljibi Mela is a legendary cross-border trade fair uniting Kumaoni, Nepali, and Shauka/Bhotia mountain communities.',
        'full_story': """First established in 1914 by the Askot royal estate, Jauljibi Fair sits directly at the geographical and cultural junction where the Gori River surges into the emerald waters of the Kali River, marking the international border between India and Nepal.

For over a century, trans-Himalayan trade routes converged here before winter snows sealed the high passes. Shauka and Bhotia traders from Johar and Darma valleys brought pashmina shawls, sheep-wool Dan carpets, and pure Himalayan herbs (cordyceps/yartsa gunbu), while traders from western Nepal crossed suspension bridges with handwoven bamboo items, mountain honey, and hand-beaten bronze.

The fair is alive with Chholiya martial sword dancers, Nepali folk singers, street food stalls serving steaming momos and hot Jhangora kheer, and heartfelt reunions between families living on opposite riverbanks.""",
        'visitor_experience': [
            'Historic cross-border trading market',
            'Spectacular Chholiya sword and shield dance',
            'Handwoven Shauka woolen carpets and pashminas',
            'Himalayan medicinal herbs and natural rock salt',
            'Cross-border cultural interaction with Nepal',
            'Authentic border food (momos, sel roti, pahadi thali)'
        ],
        'cultural_significance': 'One of the few remaining historic barter and cultural meeting fairs connecting India, Nepal, and high-Himalayan Tibetan borderlands.',
        'where_to_experience': 'Confluence grounds of Jauljibi, 68 km from Pithoragarh along the Dharchula highway.',
        'when_celebrated': '14–21 November every year (Commencing 14 November 2026)',
        'local_tips': 'Carry valid government ID as this is an international border area. Don\'t miss buying authentic hand-knotted woolen slippers and pure Johari rajma.'
    },
    {
        'id': 'hill-jatra',
        'slug': 'hill-jatra',
        'title': 'Hill Jatra',
        'subtitle': 'Agrarian Mask Theatre & The Legend of Lakhia Bhoot',
        'region': 'kumaon',
        'region_name': 'Kumaon',
        'district': 'Pithoragarh',
        'location': 'Kumor & surrounding villages, Pithoragarh',
        'map_location_key': 'pithoragarh',
        'category': 'Agricultural & Folk Festival',
        'type_key': 'folk_culture',
        'season': 'monsoon',
        'season_name': 'Monsoon / Paddy Sowing (Aug–Sep)',
        'date_display': '30 August – 2 September 2026 (Paddy Plantation / Bhadon)',
        'date_note': 'Celebrated in Kumor village following the completion of terrace paddy transplantation.',
        'verified': True,
        'image': '/static/images/festivals/hill_jatra.jpg',
        'image_attribution': 'Kumor Village Gram Sabha / Pithoragarh Cultural Archives',
        'short_story': 'A dramatic centuries-old pastoral mask theatre celebrated during the monsoon paddy transplantation. The centerpiece is the fearsome arrival of Lakhia Bhoot—the protective spirit of Lord Shiva who blesses the crops and livestock.',
        'full_story': """Originating during the reign of the Chand kings, Hill Jatra ("the march through the mud") is celebrated in the fertile bowl of the Soar Valley, particularly in the village of Kumor. Associated with the rigorous labour of transplanting rice seedlings (Ropai) in flooded terraces, the festival turns agricultural toil into a vibrant community theatre.

The festival unfolds in three distinct musical acts:
1. In the first act, actors wearing wooden bull masks re-enact the comic and strenuous labor of mountain plowing.
2. In the second act, regional folk characters (the deer, the shepherd, the forest witch) interact playfully with the village audience.
3. The grand finale is the breathtaking entry of Lakhia Bhoot—Lord Shiva\'s fierce attendant. Draped in black yak wool, wearing a frightening carved wooden mask with tusks, and flanked by attendants holding him with thick ropes, Lakhia Bhoot blesses children and promises bumper harvests.

The performance showcases living folk theatre unmediated by commercial stages.""",
        'visitor_experience': [
            'Traditional wooden mask theatre performances',
            'Dramatic arrival of Lakhia Bhoot',
            'Paddy planting songs and harvest folklore',
            'Traditional village costumes and cowherd masks',
            'Communal celebration uniting all valley hamlets'
        ],
        'cultural_significance': 'Living indigenous mask theatre fusing Shaivite rituals with animist pastoral customs and agricultural thanksgiving.',
        'where_to_experience': 'Kumor village grounds and Bajethi outskirts, 3 km from Pithoragarh town center.',
        'when_celebrated': 'Late August / Early September during paddy transplantation (Bhadon month)',
        'local_tips': 'Expect muddy village grounds; wear sturdy waterproof sandals. The evening culmination is accompanied by massive crowds of villagers.'
    },
    {
        'id': 'kumaoni-holi',
        'slug': 'kumaoni-holi',
        'title': 'Kumaoni Holi',
        'subtitle': 'Classical Ragas, Baithki, Khari & Mahila Holi',
        'region': 'kumaon',
        'region_name': 'Kumaon',
        'district': 'Almora / Nainital / Kumaon',
        'location': 'Almora, Nainital, Bageshwar, and Kumaoni villages',
        'map_location_key': 'almora',
        'category': 'Musical Folk Tradition',
        'type_key': 'festivals',
        'season': 'spring',
        'season_name': 'Spring / Phalgun (Feb–March)',
        'date_display': '2 – 4 March 2026 (Baithki from Vasant Panchami; Chharadi on 4 March)',
        'date_note': 'Baithki sessions run from Vasant Panchami to Phalgun Purnima; Khari & Chharadi climax on 2–4 March 2026.',
        'verified': True,
        'image': '/static/images/festivals/kumaoni_holi.jpg',
        'image_attribution': 'Almora Heritage Society / Classical Music Archive',
        'short_story': 'Unlike loud color parties elsewhere, Kumaoni Holi is a sophisticated two-month musical odyssey blending Hindustani classical ragas with sacred folklore through Baithki (seated chamber music), Khari (standing courtyard song-dance), and Mahila Holi.',
        'full_story': """Dating back over four centuries to the royal courts of Champawat and Almora, Kumaoni Holi is one of the most intellectually and aesthetically elevated musical traditions in South Asia.

The festival unfolds in three distinct musical formats:
1. **Baithki Holi (Seated Holi)**: Begins on Vasant Panchami in temple courtyards and heritage homes. Accomplished singers and harmonium players perform complex classical ragas timed strictly to the hour of the day—Raga Kafi and Bhairavi in the morning, Pilu and Sarang in the afternoon, and Yaman and Khamaj by twilight.
2. **Khari Holi (Standing Holi)**: In rural villages, men dress in pristine white churidars, kurta, and traditional topi, dancing in coordinated circles to the syncopated rhythms of the dhol, damau, and hudka.
3. **Mahila Holi**: Women gather in courtyard sanctuaries to compose witty, poignant, and devotional songs celebrating marital bonds and Himalayan village life.

Colors (natural abir and water) are used gently and only in the final two days (Chharadi).""",
        'visitor_experience': [
            'Baithki Holi classical music mehfils in historic courtyards',
            'Khari Holi standing circle dance and drum syncopation',
            'Mahila Holi songs celebrating feminine folklore',
            'Classical-style folk singing with harmonium and tabla',
            'Traditional white pahadi festive attire',
            'Warm hospitality with Alu ke Gutke and Bal Mithai'
        ],
        'cultural_significance': 'A rare and peerless synthesis of Hindustani classical music with community folk festivities, preserved continuously for over 400 years.',
        'where_to_experience': 'Almora old town (Lala Bazaar, Malla Mahal), Kasar Devi courtyards, and Nainital Flatts.',
        'when_celebrated': 'Vasant Panchami through Phalgun Purnima (Peak celebration: 2–4 March 2026)',
        'local_tips': 'Attend an evening Baithki session in Almora for an unforgettable acoustic experience. Photography should be discreet during temple recitals.'
    },
    {
        'id': 'uttarayani-kauthig',
        'slug': 'uttarayani-kauthig',
        'title': 'Uttarayani / Uttarayani Kauthig',
        'subtitle': 'Sacred Confluence Fair of Saryu and Gomti',
        'region': 'kumaon',
        'region_name': 'Kumaon',
        'district': 'Bageshwar',
        'location': 'Bagnath Temple & River Confluence, Bageshwar',
        'map_location_key': 'bageshwar',
        'category': 'Traditional Fair',
        'type_key': 'fairs',
        'season': 'winter',
        'season_name': 'Winter / Makar Sankranti (13–19 Jan)',
        'date_display': '13 – 19 January 2027 (Makar Sankranti Confluence Fair)',
        'date_note': 'Historic 7-day fair commencing on Makar Sankranti eve at Bagnath Temple.',
        'verified': True,
        'image': '/static/images/festivals/uttarayani_fair.jpg',
        'image_attribution': 'Uttarakhand Tourism Development Board (UTDB)',
        'short_story': 'Celebrated on Makar Sankranti at the sacred confluence of the Saryu and Gomti rivers, the Uttarayani Fair in Bageshwar is Kumaon\'s historic marketplace and spiritual gathering place, centered around the 10th-century Bagnath Temple.',
        'full_story': """Uttarayani marks the moment the sun begins its northern journey (Uttarayan). Held in the temple town of Bageshwar—often called the "Varanasi of Kumaon"—the fair has both spiritual holiness and monumental historic resonance.

Devotees take ritual cleansing dips at the confluence of the sacred Saryu and Gomti rivers before daybreak and offer jal to the self-manifested stone shivling at the Bagnath Temple, originally erected by Katyuri kings and renovated by King Laxmi Chand in 1602.

Historically, Uttarayani was Kumaon\'s largest winter trade fair where Bhotia traders from Tibet and Johar exchanged yak tails, rock salt, and borax for grain, jaggery, and brass utensils. It was also the site of the historic 1921 Coolie-Begar abolition movement, where thousands of freedom fighters dumped the hated forced-labor registers into the Saryu River under Mahatma Gandhi\'s inspiration.""",
        'visitor_experience': [
            'Sunrise holy bathing at the Saryu–Gomti confluence',
            'Darshan at the ancient 10th-century Bagnath Temple',
            'Spectacular Jhora and Chanchari folk circle singing',
            'Handmade copper water pots (tamta craft)',
            'Traditional Ringal bamboo baskets and woolens',
            'Bageshwar street food (roasted sweet potatoes, jalebi)'
        ],
        'cultural_significance': 'Spiritual confluence, historic trans-Himalayan trade hub, and iconic center of Uttarakhand\'s non-violent freedom movement.',
        'where_to_experience': 'Bageshwar town confluence ghats, Bagnath temple precinct, and fairgrounds.',
        'when_celebrated': '13–19 January 2027 (Makar Sankranti Sangam fair)',
        'local_tips': 'Nights are very chilly; pack heavy woollens. Try to witness the midnight folk song duets (Bair) between veteran village singers.'
    },
    {
        'id': 'nanda-devi-mela',
        'slug': 'nanda-devi-mela',
        'title': 'Nanda Devi Mela',
        'subtitle': 'Sacred Procession of Goddess Nanda & Sunanda',
        'region': 'kumaon',
        'region_name': 'Kumaon',
        'district': 'Almora & Nainital',
        'location': 'Almora (Malla Mahal) & Nainital (Flats / Naina Devi)',
        'map_location_key': 'almora',
        'category': 'Religious & Cultural Festival',
        'type_key': 'festivals',
        'season': 'autumn',
        'season_name': 'Autumn / September (16–20 Sep)',
        'date_display': '16 – 20 September 2026 (Nanda Ashtami on 19 September)',
        'date_note': 'Celebrated on Bhadrapad Shukla Ashtami (Peak Nanda Ashtami on 19 September 2026).',
        'verified': True,
        'image': '/static/images/festivals/nanda_devi_mela.jpg',
        'image_attribution': 'Almora Nanda Devi Temple Trust & UTDB',
        'short_story': 'Nanda Devi is the revered guardian goddess of the Uttarakhand Himalayas. The annual fair features the ceremonial sculpting of twin murtis of Nanda and Sunanda from chosen banana trunks, carried in grand processions amidst Chholiya sword dances and Ransingha horns.',
        'full_story': """For centuries, the communities of Uttarakhand have worshipped Goddess Nanda Devi not merely as a cosmic deity, but as their own royal daughter (dhyani) who visits her parental mountain home every autumn. The historic fair dates back to King Kalyan Chand\'s establishment of her royal shrine inside Almora\'s Malla Mahal fort in the 16th century.

The most sacred ritual of the festival is the ceremonial felling of auspicious wild banana trees from sacred village groves. In solemn secrecy, hereditary priests sculpt and paint the twin effigies of Goddess Nanda and her sister Sunanda with divine compassion.

On Nanda Ashtami, tens of thousands of pilgrims fill the ancient stone alleys of Almora and the lakeside promenade of Nainital. The sacred palanquin (Dola) is paraded accompanied by Chholiya martial sword dancers, traditional drummers, and the soaring call of giant curved brass horns (Ransingha).""",
        'visitor_experience': [
            'Nanda-Sunanda grand Dola palanquin procession',
            'Traditional Chholiya sword dance & Ransingha horns',
            'Revered banana-trunk murti darshan and blessings',
            'Ancient Almora cobblestone bazaar festivity',
            'Authentic Kumaoni handicraft and sweet stalls',
            'Temple rituals and evening devotional aartis'
        ],
        'cultural_significance': 'The supreme cultural festival of Kumaon celebrating the emotional bond between the mountain daughter goddess and her Himalayan people.',
        'where_to_experience': 'Almora (Malla Mahal & Nanda Devi Temple) and Nainital (Flats & Naina Devi lakeside temple).',
        'when_celebrated': '16–20 September 2026 (Nanda Ashtami procession on 19 September 2026)',
        'local_tips': 'Book accommodations weeks in advance as hotels fill up quickly. Wear comfortable walking shoes for the procession through Almora\'s stepped alleys.'
    },
    {
        'id': 'egaas-bagwal',
        'slug': 'egaas-bagwal',
        'title': 'Egaas Bagwal',
        'subtitle': 'Uttarakhand\'s Authentic Second Diwali & Bhailyo',
        'region': 'all',
        'region_name': 'Kumaon & Garhwal',
        'district': 'Statewide Villages',
        'location': 'Mountain villages across Kumaon and Garhwal',
        'map_location_key': 'almora',
        'category': 'Community Festival',
        'type_key': 'seasonal',
        'season': 'autumn',
        'season_name': 'Autumn / November (20 Nov)',
        'date_display': '20 November 2026 (Haribodhini Ekadashi / 11 Days After Diwali)',
        'date_note': 'Celebrated exactly 11 days after Diwali on Kartik Shukla Ekadashi across Uttarakhand.',
        'verified': True,
        'image': '/static/images/festivals/egaas_bagwal.jpg',
        'image_attribution': 'Pahadi Heritage Collective / Village Homestay Network',
        'short_story': 'Celebrated eleven days after Diwali, Egaas Bagwal is Uttarakhand\'s true indigenous festival of lights. Villages light pine-torch fires, spin fiery wooden ropes called Bhailyo, worship mountain livestock, and dance into the starlit night.',
        'full_story': """According to beloved Himalayan lore, the news of Lord Rama\'s return to Ayodhya reached the deep, isolated mountain valleys of Uttarakhand eleven days later than the plains. Another historic legend recalls that the brave Garhwali commander Madho Singh Bhandari returned victorious from the Tibetan border campaign on this exact night.

On the night of Egaas, every stone-slate roofed village house is illuminated with earthen lamps (diyas) and resinous pine splints. The cattle are given warm water baths, their horns decorated with turmeric and oil, and fed festive rotis.

The highlight of the celebration is the spirited tradition of **Bhailyo**—ropes braided from mountain babila grass and dried pine wood, lit at the end and spun rhythmically in flaming circles by villagers performing agile acrobatic steps to the beat of dhol and damau drums.""",
        'visitor_experience': [
            'Spinning of flaming Bhailyo ropes in village squares',
            'Traditional oil lamps illuminating stone Himalayan homes',
            'Pashupalan rituals honoring mountain cattle & livestock',
            'Local culinary treats (Gulgule, Puda, Arsa, Swala)',
            'Spirited village circle dancing under the autumn stars',
            'Warm community hospitality in traditional homestays'
        ],
        'cultural_significance': 'An intimate indigenous mountain festival reflecting historical geography, livestock reverence, and heroic martial folk history.',
        'where_to_experience': 'Rural mountain villages of Tehri, Pauri, Chamoli, Almora, and Bageshwar.',
        'when_celebrated': '20 November 2026 (Haribodhini Ekadashi / Igas Bagwal)',
        'local_tips': 'Experience this inside a remote homestay rather than a commercial hotel to participate in making and spinning the Bhailyo.'
    },
    {
        'id': 'phool-dei',
        'slug': 'phool-dei',
        'title': 'Phool Dei',
        'subtitle': 'Children\'s Harvest Welcome to Himalayan Spring',
        'region': 'all',
        'region_name': 'Kumaon & Garhwal',
        'district': 'Statewide Villages',
        'location': 'Every village home across Uttarakhand',
        'map_location_key': 'dwarahat',
        'category': 'Spring Folk Tradition',
        'type_key': 'seasonal',
        'season': 'spring',
        'season_name': 'Spring / Chaitra (14–15 March)',
        'date_display': '14 – 15 March 2026 (Chaitra Sankranti / Spring Welcoming)',
        'date_note': 'Celebrated on the 1st day of the Hindu solar month of Chaitra as wildflowers bloom.',
        'verified': True,
        'image': '/static/images/festivals/phool_dei.jpg',
        'image_attribution': 'Chaitra Heritage Initiative / Uttarakhand Forest & Culture',
        'short_story': 'Phool Dei is the gentle spring festival where young children gather freshly bloomed wild flowers like yellow Pyoli and crimson Buransh, placing them on village doorsteps while singing blessings of prosperity and peace.',
        'full_story': """On the first day of the Hindu solar month of Chaitra (mid-March), the snow begins to melt on south-facing mountain slopes, and the Himalayan forests burst into incandescent crimson rhododendron (Buransh) and yellow Pyoli blossoms.

Phool Dei is an ode to nature, innocence, and ecological harmony. Early in the morning, young girls and boys known as *Phoolyari* wander through forest clearings with handcrafted Ringal bamboo baskets, collecting dew-kissed petals of wild wildflowers.

The children visit every home in the village, scattering colorful petals upon the wooden doorframes (Dehri) and singing the ancient folk couplet:
*"Phool Dei, Chhamma Dei, Daitkar, Mai Dei, Bhokar Bhari, Chhakar Phool, Dei Dei"*
(May your doorway bloom with flowers, may your granaries overflow, may peace and prosperity inhabit this home).

Householders welcome the children with blessings and gifts of jaggery, rice, and crisp coins.""",
        'visitor_experience': [
            'Children placing fresh wildflowers on village thresholds',
            'Vibrant crimson rhododendron and golden Pyoli blossoms',
            'Traditional Pahadi folk greetings and rhymes',
            'Freshly prepared local sweet porridge (Sei made of rice flour & curd)',
            'Springtime Himalayan village waking up from winter slumber'
        ],
        'cultural_significance': 'Celebrates the symbiotic relationship between childhood, seasonal floral renewal, and the sanctity of the Himalayan home.',
        'where_to_experience': 'Traditional stone villages throughout Kumaon and Garhwal (e.g. Dwarahat, Almora hamlets, Tehri villages).',
        'when_celebrated': '14–15 March 2026 (Chaitra Sankranti annually)',
        'local_tips': 'Wake up early at 6 AM in a village homestay to watch the children sing on the threshold. Offer small tokens or fruits respectfully.'
    },
    {
        'id': 'kandali-festival',
        'slug': 'kandali-festival',
        'title': 'Kandali Festival',
        'subtitle': 'The 12-Year Strobilanthes Bloom of Chaundas Valley',
        'region': 'kumaon',
        'region_name': 'Kumaon',
        'district': 'Pithoragarh',
        'location': 'Chaundas Valley, Dharchula / Pithoragarh',
        'map_location_key': 'pithoragarh',
        'category': 'Folk & Community Festival',
        'type_key': 'folk_culture',
        'season': 'autumn',
        'season_name': 'Autumn / 12-Year Botanical Bloom Cycle',
        'date_display': 'Autumn 2026 / 2027 (12-Year Strobilanthes Bloom Cycle)',
        'date_note': 'Once every 12 years in Autumn when the Strobilanthes wallichii (Kandali) flower carpets the ridges.',
        'verified': True,
        'image': '/static/images/festivals/kandali_festival.jpg',
        'image_attribution': 'Rung Kalyan Sanstha / Pithoragarh Anthropological Society',
        'short_story': 'Celebrated once every twelve years by the indigenous Rung (Shauka) community of Chaundas Valley, the Kandali festival commemorates the flowering of the sacred Kandali plant and the heroic defense of their valleys by mountain women.',
        'full_story': """The Kandali Festival is one of the most distinctive and rare cultural celebrations on earth, held only once every twelve years when the flowering shrub *Kandali* (Strobilanthes wallichii) carpets the high crags of the Chaundas Valley in royal purple.

Celebrated by the tribal Rung community in villages like Pangu and Sosa, the festival has deep mythological and historical layers. According to oral history, when local men were away trading in Tibet, enemy marauders attacked the valley. The courageous Rung women armed themselves with traditional wooden pestles and sickles, fighting off the invaders who hid among the tall Kandali thickets.

During the festival, a sacred Shiva linga made of barley flour is consecrated. Then, women clad in magnificent traditional attire (*Chungbala* dresses, silver coin necklaces, and ornate headwear) march in an energetic military formation to ceremonial drumbeats, ritualistically uprooting and cutting the Kandali plants in symbolic triumph.""",
        'visitor_experience': [
            'Historic once-in-a-twelve-year cultural spectacle',
            'Magnificent traditional Rung tribal costumes and heavy silver jewellery',
            'Martial women\'s procession armed with ceremonial sickles',
            'Sacred barley dough linga rituals and invocations',
            'Ancient Rung dialect songs and community solidarity banquets'
        ],
        'cultural_significance': 'Celebrates feminine valor, the ecological blooming cycle of Strobilanthes, and the distinct tribal identity of the Indo-Tibetan borderlands.',
        'where_to_experience': 'Chaundas Valley villages near Dharchula, Pithoragarh district.',
        'when_celebrated': '12-Year Botanical Bloom Cycle (Next expected: October 2026 / 2027)',
        'local_tips': 'Inner Line Permits may be required for foreign travelers near the border. Photography of specific inner sanctum rituals is restricted.'
    },
    {
        'id': 'syalde-bikhauti',
        'slug': 'syalde-bikhauti',
        'title': 'Syalde Bikhauti',
        'subtitle': 'Ancient Katyuri Martial Heritage & Jhoda Singing',
        'region': 'kumaon',
        'region_name': 'Kumaon',
        'district': 'Almora / Dwarahat',
        'location': 'Dwarahat, Almora district',
        'map_location_key': 'dwarahat',
        'category': 'Traditional Fair & Folk Culture',
        'type_key': 'fairs',
        'season': 'spring',
        'season_name': 'Spring / Baisakhi (13–14 April)',
        'date_display': '13 – 14 April 2026 (Baisakhi Eve & Bikhauti Day)',
        'date_note': 'Begins on the last day of Chaitra at Syalde Pokhar and culminates on Baisakhi at Vibhandeshwar.',
        'verified': True,
        'image': '/static/images/festivals/syalde_bikhauti.jpg',
        'image_attribution': 'Dwarahat Temple Restoration Guild / Local Archive',
        'short_story': 'Held in the ancient Katyuri temple town of Dwarahat, Syalde Bikhauti is a legendary fair celebrating regional pride, historical clan reconciliation, and unbroken traditions of night-long Jhoda singing and traditional martial staff displays.',
        'full_story': """Dwarahat, known as the "Valley of Temples," preserves over 55 structural stone shrines erected by the Katyuri kings between the 10th and 13th centuries. The Syalde Bikhauti Mela begins on the last day of the Hindu month of Chaitra at the Syalde Pokhar (pond) and culminates the following day (Bikhauti) at the Vibhandeshwar Mahadev temple.

Historically, the fair featured ritualized mock skirmishes between two rival regional factions (the Olya and Garhwal-allied clans), testing their martial prowess with brass-studded wooden staffs (*Lathis*). Today, this historic rivalry has transformed into enthusiastic ceremonial processions honoring ancient flags (Nishan).

As dusk settles over the stone temple complexes, hundreds of men and women link arms in circular Jhoda dances, chanting witty folk poetry and ancient ballads commemorating Katyuri chivalry until the early hours of morning.""",
        'visitor_experience': [
            'Night-long Jhoda circle singing under the stars',
            'Historic ceremonial staff and flag processions',
            '10th-century Katyuri stone temple architectural backdrop',
            'Bustling rural fair with brassware, handloom shawls, and mountain crafts',
            'Traditional Kumaoni culinary fare (crisp Jalebis, Singori, spicy Chana)'
        ],
        'cultural_significance': 'Unbroken medieval martial memory transformed into harmonious folk song culture amidst monumental architectural heritage.',
        'where_to_experience': 'Dwarahat town center, Syalde Pokhar, and Vibhandeshwar Temple complex, Almora district.',
        'when_celebrated': '13–14 April 2026 (Baisakhi period annually)',
        'local_tips': 'Spend time exploring the 11th-century Hat Kachari and Gujar Deo temple ruins while attending the fair.'
    },
    {
        'id': 'nanda-devi-raj-jat',
        'slug': 'nanda-devi-raj-jat',
        'title': 'Nanda Devi Raj Jat Yatra',
        'subtitle': 'The Himalayan Mahakumbh of Uttarakhand',
        'region': 'garhwal',
        'region_name': 'Garhwal & Kumaon',
        'district': 'Chamoli',
        'location': 'Nauti Village to Homkund, Chamoli',
        'map_location_key': 'homkund',
        'category': 'Sacred Pilgrimage & Himalayan Mahakumbh',
        'type_key': 'festivals',
        'season': 'autumn',
        'season_name': 'Autumn / Bhadon (12-Year Cycle: 5–23 Sep 2026)',
        'date_display': '5 – 23 September 2026 (Culmination on 19 Sep · Nanda Ashtami)',
        'date_note': 'Upcoming 2026 Pilgrimage: 5–23 September 2026. Peak Nanda Ashtami rituals at Homkund on 19 September 2026. Last historic Jat held 18 Aug – 6 Sep 2014.',
        'verified': True,
        'image': '/static/images/Almora/nandadevi.png',
        'image_attribution': 'Shri Nanda Devi Raj Jat Samiti / Nauti Cultural Archives',
        'short_story': 'The supreme Himalayan pilgrimage of Uttarakhand spanning ~280 km barefoot over 22 days. Accompanying Goddess Nanda Devi from her maternal home in Nauti to her divine consort Lord Shiva\'s abode at Mount Trishul, led by a miraculous four-horned ram.',
        'full_story': """Known as the Himalayan Mahakumbh, the Nanda Devi Raj Jat is Uttarakhand's most sacred and arduous pilgrimage, held once every 12 years across approximately 280 kilometers of high-altitude Himalayan wilderness.

The Yatra portrays the poignant farewell (Vidaai) of Goddess Nanda Devi—revered as the beloved daughter of the Himalayas—as she leaves her maternal home (Maika) at Nauti village to join her consort, Lord Shiva, at his celestial abode near Mount Trishul.

The pilgrimage is guided by a miraculous four-horned ram (Chausingha Khadu) born in Kasuwa village and accompanied by the royal golden ringed umbrella (Chhantoli) carried by the descendants of Garhwal's Parmar royalty. At Nandkeshari, Garhwal and Kumaon pilgrims unite in tearful devotion. Beyond Wan, the last human village, pilgrims discard footwear and traverse freezing meadows of Bedni Bugyal and the glacial mystery of Roopkund to reach Homkund (4,061 m), where the sacred ram is released alone into the eternal snows.""",
        'visitor_experience': [
            'Historic 280-km Himalayan pilgrimage trail',
            'Sacred Golden Chhantoli (ringed umbrella) procession',
            'Miracle of the Four-Horned Ram (Chausingha Khadu)',
            'Union of Garhwal and Kumaon pilgrims at Nandkeshari',
            'Barefoot walk across alpine Bedni Bugyal',
            'Glacial mystery lake of Roopkund (4,778 m)',
            'Final sacred Hawan at Homkund at the base of Mount Trishul'
        ],
        'cultural_significance': 'The ultimate spiritual expression of Uttarakhand, binding mountain geography, folklore, ecology, and the emotional daughterhood of Goddess Nanda into an unbroken living tradition.',
        'where_to_experience': 'From Nauti Temple (Karnaprayag) through Wan village, Bedni Bugyal, Roopkund, and culminating at Homkund lake at the foot of Mount Trishul.',
        'when_celebrated': '5–23 September 2026 (Bhadrapada Shukla Paksha; Homkund on 19 September 2026)',
        'local_tips': 'Pilgrims must maintain strict ecological purity. No leather items or synthetic plastics are permitted beyond Bedni Bugyal. High-altitude fitness and warm layering are mandatory.'
    }
]


LIVING_CULTURE = [
    {
        'id': 'aipan-art',
        'title': 'Aipan Art',
        'subtitle': 'The Sacred Geometry of Himalayan Thresholds',
        'region': 'Kumaon',
        'image': '/static/images/culture/aipan_art.jpg',
        'image_attribution': 'Aipan Heritage Foundation / Almora Artisans',
        'explanation': 'Ancient ritual art hand-painted on auspicious occasions using red clay (Geru) and ground rice paste (Biswar). Each geometric motif carries sacred symbolism for prosperity and protection.',
        'link_url': '/culture/art?region=kumaon',
        'tags': ['Folk Art', 'Ritual', 'Geometric Motifs', 'GI Tagged']
    },
    {
        'id': 'chholiya-dance',
        'title': 'Chholiya Dance',
        'subtitle': 'Sword Dance of Ancient Rajput Martial Heritage',
        'region': 'Kumaon & Garhwal',
        'image': '/static/images/culture/chholiya_dance.jpg',
        'image_attribution': 'Kumaon Folk Artists Guild',
        'explanation': 'A spectacular 10-century-old martial sword and shield dance accompanied by the resonant call of curved brass Ransingha horns, dhol, and damau to ward off evil spirits.',
        'link_url': '/culture/festivals/nanda-devi-mela',
        'tags': ['Martial Dance', 'Sword & Shield', 'Brass Horns', 'UNESCO Heritage Style']
    },
    {
        'id': 'jhora-dance',
        'title': 'Jhora Dance',
        'subtitle': 'The Unifying Communal Circle of Song',
        'region': 'Kumaon',
        'image': '/static/images/culture/jhora_dance.jpg',
        'image_attribution': 'Uttarakhand Cultural Heritage Trust',
        'explanation': 'A joyous community circle dance where men and women link arms, stepping rhythmically to poetic ballads that dissolve all village barriers during spring and autumn fairs.',
        'link_url': '/culture/festivals/syalde-bikhauti',
        'tags': ['Circle Dance', 'Community Folk', 'Poetic Ballads', 'Harvest Season']
    },
    {
        'id': 'kumaoni-folk-music',
        'title': 'Kumaoni Folk Music',
        'subtitle': 'Echoes of the High Valleys & Mountain Flutes',
        'region': 'Kumaon',
        'image': '/static/images/culture/kumaoni_music.jpg',
        'image_attribution': 'Himalayan Acoustic Traditions Archive',
        'explanation': 'Timeless vocal traditions and oral epics (Jagar, Bair, Neoli) accompanied by indigenous instruments including the small hourglass drum (hudka), dhol-damau, and bamboo flute (muralya).',
        'link_url': '/culture/festivals/kumaoni-holi',
        'tags': ['Oral Epics', 'Hudka Drum', 'Sacred Jagar', 'Classical Ragas']
    },
    {
        'id': 'bhotia-heritage',
        'title': 'Bhotia / Shauka Heritage',
        'subtitle': 'Trans-Himalayan Weavers & Highland Traders',
        'region': 'Kumaon & Garhwal',
        'image': '/static/images/culture/bhotia_heritage.jpg',
        'image_attribution': 'Sarmoli Village Cooperative / Johar Valley',
        'explanation': 'The resilient culture of the high Himalayan valleys (Johar, Darma, Byans), world-famed for exquisite hand-knotted sheep-wool Dan carpets, pashmina shawls, and frontier oral histories.',
        'link_url': '/culture/festivals/jauljibi-fair',
        'tags': ['Handloom Weaving', 'Wool Rugs', 'Trans-Himalayan', 'Tribal Legacy']
    },
    {
        'id': 'traditional-cuisine',
        'title': 'Traditional Kumaoni Cuisine',
        'subtitle': 'Wholesome Mountain Millets & Forest Herbs',
        'region': 'Kumaon & Garhwal',
        'image': '/static/images/culture/kumaoni_cuisine.jpg',
        'image_attribution': 'Pahadi Rasoi Initiative / Almora',
        'explanation': 'Nutrient-rich, slow-cooked mountain foods including black soybean curry (Bhatt ki Churkani), tempering with wild jakhiya seeds, roasted Bal Mithai, Singori in malu leaf, and barnyard millet kheer.',
        'link_url': '/culture/food?region=kumaon',
        'tags': ['Organic Millets', 'Bhatt ki Churkani', 'Bal Mithai', 'Singori']
    }
]


TRADITIONAL_ARTS = [
    {
        'id': 'ringal-craft',
        'title': 'Ringal Bamboo Craft of Garhwal',
        'subtitle': 'High-Altitude Eco-Friendly Wild Bamboo Weaving',
        'district': 'Chamoli & Uttarkashi',
        'region': 'Garhwal',
        'gi_tag': True,
        'gi_tag_badge': 'GI Tagged Uttarakhand (2021)',
        'cover_image': '/static/images/Arts/ringalCraft/ringalcraft.png',
        'gallery': [
            '/static/images/Arts/ringalCraft/ringalcraft.png',
            '/static/images/Arts/ringalCraft/ringalcrafttwo.png',
            '/static/images/Arts/ringalCraft/ringalcraftthree.png',
            '/static/images/Arts/ringalCraft/ringalcragtfour.png'
        ],
        'short_story': 'Woven from wild dwarf mountain bamboo harvested above 1,800m in Garhwal\'s high oak forests, Ringal artisans handcraft lightweight, water-resistant baskets, mats, and lanterns using centuries-old sacred interlocking weaves without nails or synthetic glues.',
        'story': """Deep within the moist oak and rhododendron forests of the Garhwal Himalayas (elevations between 1,800 and 2,800 meters) grows Ringal (Drepanostachyum falcatum)—a slender, highly flexible wild dwarf bamboo. For centuries, rural Himalayan communities have sustainably harvested this perennial grass to handcraft essential pastoral, agricultural, and household wares.

Hereditary weavers, primarily from the Rudia and artisanal communities, split mature culms using traditional hand-knives (Daranti) into fine, supple ribbons. Without nails or synthetic glues, they weave the pliable strands into the iconic 'Mosta' (impermeable floor mats for drying grains), 'Supas' (winnowing scoops), 'Kandi' (heavy-load carrying hampers shaped ergonomically for steep mountain trails), and contemporary modern decor items like lanterns, fruit trays, and pen stands.

In 2021, Uttarakhand Ringal Craft was awarded the prestigious Geographical Indication (GI) tag, recognizing its irreplaceable socio-economic role in sustainable mountain livelihoods.""",
        'what_makes_unique': 'Sourced exclusively from wild sub-alpine mountain bamboo; naturally pest-resistant, biodegradable, and woven using centuries-old sacred interlocking geometry.',
        'raw_materials': ['Wild Ringal Dwarf Bamboo (Drepanostachyum falcatum)', 'Natural Mountain River Water for Softening', 'Vegetable Oil Finishing'],
        'products': ['Mosta floor mats', 'Kandi mountain backpacks', 'Supa winnowing trays', 'Bamboo lampshades', 'Fruit baskets', 'Tea coasters'],
        'vendor_cluster': {
            'name': 'Garhwal Ringal Mahila Utthan Samiti & Pipalkoti Crafts Guild',
            'artisan_leader': 'Master Weaver Rajendra Rudia & 35 Village Women Weavers',
            'exact_location': 'Pipalkoti Village Craft Center, Main Badrinath Highway (NH-7), Chamoli District',
            'visiting_hours': '9:00 AM – 6:30 PM (Daily — Live demonstrations open to tourists)',
            'price_range': '₹180 to ₹2,800 (Direct Cooperative Fair-Trade Pricing)',
            'phone': '+91 94115 82341 (Verified Cooperative Contact)',
            'whatsapp': '+919411582341',
            'how_to_reach': 'Pipalkoti is located right on the Rishikesh-Badrinath National Highway (NH-7), 220 km from Rishikesh and 30 km before Joshimath. Shared Maxx jeeps and UTC state buses run frequently from Rishikesh and Srinagar (Garhwal).'
        },
        'how_tourism_reaches_via_website': {
            'homestay_district': 'uttarkashi',
            'homestay_label': 'Book Verified Homestays in Chamoli & Uttarkashi',
            'homestay_url': '/hotels?district=uttarkashi',
            'guide_district': 'uttarkashi',
            'guide_label': 'Hire Local Garhwali Cultural Guide',
            'guide_url': '/guides?district=uttarkashi',
            'trip_planner_url': '/plan/',
            'trip_planner_label': 'Add Pipalkoti Craft Village to Your Itinerary'
        }
    },
    {
        'id': 'wooden-carving',
        'title': 'Traditional Wood Carving — Kath-Khuni & Likhai',
        'subtitle': 'Himalayan Temple Architecture & Intricate Doorframe Reliefs',
        'district': 'Barkot (Uttarkashi) & Dwarahat (Almora)',
        'region': 'Garhwal & Kumaon',
        'gi_tag': True,
        'gi_tag_badge': 'Uttarakhand State Heritage Craft',
        'cover_image': '/static/images/Arts/WoodenCarving/woodencarving.png',
        'gallery': [
            '/static/images/Arts/WoodenCarving/woodencarving.png',
            '/static/images/Arts/WoodenCarving/woodencarvingtwo.png',
            '/static/images/Arts/WoodenCarving/woodencarvingthrww.png',
            '/static/images/Arts/WoodenCarving/woodenvarvingfour.png'
        ],
        'short_story': 'Centuries before modern architecture, Himalayan master carvers chiseled fragrant Deodar cedar beams for earthquake-resistant Kath-Khuni temples, embellishing door lintels with sacred deities and cosmic floral mandalas.',
        'story': """The indigenous architectural woodcarving of the Central Himalayas, known as Likhai, is central to traditional Kath-Khuni (cator-and-cribbage) earthquake-resistant construction. Centuries before iron rebar, master woodsmiths (Odh or Badhai) interlocked thick beams of aromatic Himalayan Cedar (Deodar) and dry-dressed stone, crowning the facades with deeply chiseled relief carvings.

Every temple lintel (Dwarpat), courtyard balcony (Tibari), and pillar is etched with auspicious cosmic symbols: Lord Ganesha, pairs of dancing peacocks (Mayur), blooming lotuses (Kamal), and coiled serpents (Naga). Today, master artisans preserve this noble trade by crafting bespoke carved temple doors, jharokha mirrors, and wall mandalas.

Tourists visiting Barkot or Dwarahat can observe master craftsmen hand-chiseling seasoned deodar wood, producing durable heritage art that carries the authentic scent of high mountain forests.""",
        'what_makes_unique': 'Chiseled by hand from naturally fragrant, termite-proof Deodar cedar wood; combines traditional structural engineering with sacred Vedic iconometry.',
        'raw_materials': ['Aromatic Himalayan Deodar Wood', 'Tun (Red Cedar)', 'Hand Steel Chisels (Rukhi & Nihani)', 'Natural Walnut Oil'],
        'products': ['Carved Jharokha window frames', 'Deodar wall mandalas', 'Ganesha entrance lintels (Dwarpat)', 'Carved cedar spice boxes'],
        'vendor_cluster': {
            'name': 'Rawain Kath-Khuni Guild & Dwarahat Heritage Woodcraft Atelier',
            'artisan_leader': 'Master Carver Sunder Lal Badhai & Traditional Guild',
            'exact_location': 'Barkot Craft Hamlet, Rawain Valley (Garhwal) & Old Dwarahat Temple Lane (Kumaon)',
            'visiting_hours': '10:00 AM – 5:30 PM (Mon–Sat — Custom commissions welcome)',
            'price_range': '₹450 (carved deodar panels) to ₹15,000+ (architectural lintels)',
            'phone': '+91 94120 71892 (Master Craftsman Studio)',
            'whatsapp': '+919412071892',
            'how_to_reach': 'Barkot is situated 135 km from Dehradun via Mussoorie and Damta on NH-507. Dwarahat is 35 km from Ranikhet on the Ranikhet-Kausani circuit with regular taxi service.'
        },
        'how_tourism_reaches_via_website': {
            'homestay_district': 'barkot',
            'homestay_label': 'Book Authentic Kath-Khuni Homestays in Barkot & Almora',
            'homestay_url': '/hotels?district=barkot',
            'guide_district': 'almora',
            'guide_label': 'Hire Architectural Temple Walk Guide',
            'guide_url': '/guides?district=almora',
            'trip_planner_url': '/plan/',
            'trip_planner_label': 'Add Traditional Woodcraft Trail to Itinerary'
        }
    },
    {
        'id': 'woolen-craft',
        'title': 'Highland Woolen Craft & Dan Handloom Rugs',
        'subtitle': 'Trans-Himalayan Shauka Pit-Loom Weaving & Knotted Carpets',
        'district': 'Pithoragarh (Munsiyari & Johar Valley)',
        'region': 'Kumaon',
        'gi_tag': True,
        'gi_tag_badge': 'GI Tagged Uttarakhand Thulma & Dan (2021)',
        'cover_image': '/static/images/Arts/WoolenCraft/woolencraft.png',
        'gallery': [
            '/static/images/Arts/WoolenCraft/woolencraft.png',
            '/static/images/Arts/WoolenCraft/woolencrafttwo.png',
            '/static/images/Arts/WoolenCraft/woolencraftthree.png',
            '/static/images/Arts/WoolenCraft/woolencraftfour.png'
        ],
        'short_story': 'Under the glaciated spires of Panchachuli, Shauka tribal women spin raw mountain sheep wool into heirloom GI-tagged Thulma brushed blankets and hand-knotted Dan carpets on traditional pit looms.',
        'story': """Under the glaciated spires of the Panchachuli peaks in the Johar and Darma valleys, the Bhotia (Shauka) women have transformed harsh mountain winters into an art form. Using raw indigenous sheep wool and Tibetan fleece, weavers clean, card, and hand-spin yarn using drop spindles (Takli) and spinning wheels (Charkha).

On heavy horizontal pit looms (Rachh), they hand-weave thick, brushed blankets (Thulma), weather-resistant cloaks (Pankhi), and tightly knotted wool carpets (Dan) bearing ancient geometric and dragon motifs rooted in centuries of trans-Himalayan silk-and-wool barter trade. In 2021, Uttarakhand Thulma and Dan were officially granted GI status.

Buying directly from village cooperatives ensures 100% of proceeds support mountain women weavers while travelers acquire heirlooms designed to last decades.""",
        'what_makes_unique': '100% natural mountain sheep wool washed in glacial river streams; hand-knotted at 60–80 knots per square inch on pit looms with zero synthetic blends.',
        'raw_materials': ['Pure Mountain Sheep Wool', 'Fine Cashmere / Pashmina', 'Natural Walnut Bark & Madder Dyes', 'Wooden Pit Looms'],
        'products': ['GI-Tagged Thulma brushed blankets', 'Pure Wool Knotted Dan Carpets', 'Pankhi shawls', 'Tibetan wool caps & mufflers'],
        'vendor_cluster': {
            'name': 'Maati Women\'s Collective & Sarmoli Weaver Cooperative',
            'artisan_leader': 'Malika Virdi & 120 Shauka Women Artisans',
            'exact_location': 'Sarmoli & Darkot Weaver Villages, Munsiyari, Pithoragarh District',
            'visiting_hours': '9:00 AM – 5:00 PM (Daily — Meet weavers at their home looms)',
            'price_range': '₹850 (Pankhi shawls) to ₹9,500 (Pure Wool Knotted Dan Rugs)',
            'phone': '+91 94111 63920 (Maati Cooperative Direct Desk)',
            'whatsapp': '+919411163920',
            'how_to_reach': 'Munsiyari is located 275 km from Kathgodam railway station. Daily shared jeeps depart from Haldwani and Pithoragarh taxi stands via Almora and Thal.'
        },
        'how_tourism_reaches_via_website': {
            'homestay_district': 'pithoragarh',
            'homestay_label': 'Book Community Homestays in Munsiyari Facing Panchachuli',
            'homestay_url': '/hotels?district=pithoragarh',
            'guide_district': 'pithoragarh',
            'guide_label': 'Hire Certified Sarmoli Village Women Guide',
            'guide_url': '/guides?district=pithoragarh',
            'trip_planner_url': '/plan/',
            'trip_planner_label': 'Add Munsiyari Weaving Route to Trip Planner'
        }
    },
    {
        'id': 'aipan-art',
        'title': 'Aipan Art — Sacred Himalayan Geometric Ritual Art',
        'subtitle': 'Ritual Threshold Geometry Drawn with Geru and Rice Paste',
        'district': 'Almora',
        'region': 'Kumaon',
        'gi_tag': True,
        'gi_tag_badge': 'GI Tagged Uttarakhand Aipan (2021)',
        'cover_image': '/static/images/Arts/Aipanart/aipan_art.jpg',
        'gallery': [
            '/static/images/Arts/Aipanart/aipan_art.jpg',
            '/static/images/culture/aipan_art.jpg'
        ],
        'short_story': 'A thousand-year-old ritual art of Kumaon drawn freehand by women using red terracotta clay (Geru) and fermented rice paste (Biswar) to invoke divine protection and prosperity on sacred thresholds.',
        'story': """Aipan is the sacred ritual art of Kumaon, practiced for over a thousand years by women to invoke divine blessings and prosperity on auspicious thresholds. Grounded on an earthy terracotta wash of red ochre (Geru), intricate geometric and cosmic patterns are drawn freehand using the ring finger—never an artificial stencil—dipped in a white fermented rice-flour paste (Biswar).

Every symbol carries cosmic intent: the central bindu represents the seed of creation, the Lakshmi Chowki with lotus footprints invites abundance during Diwali, the Dhuli Arghya blesses weddings, and the Swastika invokes cosmic balance. Officially recognized with a GI Tag in 2021, Aipan has expanded from floors and walls to authentic handmade wooden home decor, ceremonial brass plates, and framed art.

Travelers visiting Almora can attend immersive 2-hour masterclasses with hereditary women artists at Lal Bazaar and Malla Mahal.""",
        'what_makes_unique': 'Hand-drawn exclusively using natural red earth (Geru) and ground rice paste (Biswar); strictly freehand sacred symmetry passed down orally through female lineage.',
        'raw_materials': ['Natural Red Ochre Earth (Geru)', 'Stone-ground White Rice Paste (Biswar)', 'Pure Cotton / Bamboo Canvas', 'Teak & Pine Frames'],
        'products': ['Lakshmi Chowki ceremonial plaques', 'Hand-painted wooden serving trays', 'Aipan tea coasters', 'Brass Diya Chowkis', 'Framed threshold art'],
        'vendor_cluster': {
            'name': 'Kumaon Aipan Mahila Samiti & Cheli Sansthan',
            'artisan_leader': 'Meenakshi Khati & Almora Women Crafts Collective',
            'exact_location': 'Lal Bazaar Craft Corridor & Malla Mahal Cultural Center, Almora',
            'visiting_hours': '10:00 AM – 7:00 PM (Daily — 2-Hour Hands-On Workshops Available)',
            'price_range': '₹250 (hand-painted diyas & coasters) to ₹4,500 (framed ceremonial chowkis)',
            'phone': '+91 94101 25488 (Aipan Cooperative Almora)',
            'whatsapp': '+919410125488',
            'how_to_reach': 'Almora is just 90 km from Kathgodam railway station. State UTC buses and shared pre-paid taxis run every 15 minutes from Kathgodam and Haldwani taxi stands.'
        },
        'how_tourism_reaches_via_website': {
            'homestay_district': 'almora',
            'homestay_label': 'Book Heritage Homestays in Almora & Kasar Devi',
            'homestay_url': '/hotels?district=almora',
            'guide_district': 'almora',
            'guide_label': 'Book Almora Heritage Walk & Aipan Masterclass Guide',
            'guide_url': '/guides?district=almora',
            'trip_planner_url': '/plan/',
            'trip_planner_label': 'Add Almora Aipan Workshop to Trip Route'
        }
    }
]


CULTURAL_MAP_LOCATIONS = [
    {
        'id': 'uttarkashi',
        'name': 'Uttarkashi',
        'region': 'Garhwal',
        'division': 'Garhwal',
        'type': 'both',
        'lat': 30.7268,
        'lng': 78.4354,
        'x': 27,
        'y': 28,
        'festivals': ['Bada Haat Mela'],
        'crafts': ['Ringal Bamboo Craft', 'Woolen Blankets'],
        'description': 'Ancient Badahat marketplace and Ringal bamboo crafts on the Bhagirathi River.',
        'vendor_name': 'Badahat Haat Craft Collective'
    },
    {
        'id': 'barkot',
        'name': 'Barkot',
        'region': 'Garhwal',
        'division': 'Garhwal',
        'type': 'both',
        'lat': 30.8133,
        'lng': 78.2081,
        'x': 18,
        'y': 32,
        'festivals': ['Rishi Muni Maharaj Mela'],
        'crafts': ['Kath-Khuni Wood Carving'],
        'description': 'Rawain valley center of pastoral deity assemblies and deodar wood carving.',
        'vendor_name': 'Rawain Kath-Khuni Wood Guild'
    },
    {
        'id': 'dyara-bugyal',
        'name': 'Dyara Bugyal',
        'region': 'Garhwal',
        'division': 'Garhwal',
        'type': 'festival',
        'lat': 30.8420,
        'lng': 78.5830,
        'x': 34,
        'y': 22,
        'festivals': ['Dyara Bugyal Makha Holi'],
        'crafts': [],
        'description': 'Alpine meadow at 3,048 m where shepherds celebrate Makha Holi with churned butter.',
        'vendor_name': 'Highland Pastoral Shepherds'
    },
    {
        'id': 'pipalkoti',
        'name': 'Pipalkoti (Chamoli)',
        'region': 'Garhwal',
        'division': 'Garhwal',
        'type': 'craft',
        'lat': 30.4285,
        'lng': 79.4312,
        'x': 42,
        'y': 36,
        'festivals': ['Alaknanda River Fair'],
        'crafts': ['Ringal Bamboo Craft (GI)'],
        'description': 'Premier craft center for wild dwarf bamboo weaving on the Badrinath route.',
        'vendor_name': 'Garhwal Ringal Mahila Utthan Samiti'
    },
    {
        'id': 'dwarahat',
        'name': 'Dwarahat',
        'region': 'Kumaon',
        'division': 'Kumaon',
        'type': 'both',
        'lat': 29.7820,
        'lng': 79.4280,
        'x': 58,
        'y': 52,
        'festivals': ['Syalde Bikhauti', 'Phool Dei'],
        'crafts': ['Katyuri Temple Woodcraft'],
        'description': 'Valley of 55 Katyuri stone-and-wood temples and Jhoda song celebrations.',
        'vendor_name': 'Dwarahat Heritage Woodsmiths'
    },
    {
        'id': 'almora',
        'name': 'Almora',
        'region': 'Kumaon',
        'division': 'Kumaon',
        'type': 'both',
        'lat': 29.5992,
        'lng': 79.6586,
        'x': 67,
        'y': 58,
        'festivals': ['Nanda Devi Mela', 'Kumaoni Holi', 'Egaas Bagwal'],
        'crafts': ['Aipan Art (GI)', 'Tamta Copperware'],
        'description': 'Cultural capital of Kumaon, world-renowned for Aipan geometric ritual art and Malla Mahal.',
        'vendor_name': 'Kumaon Aipan Mahila Samiti & Lal Bazaar'
    },
    {
        'id': 'nainital',
        'name': 'Nainital',
        'region': 'Kumaon',
        'division': 'Kumaon',
        'type': 'festival',
        'lat': 29.3919,
        'lng': 79.4542,
        'x': 57,
        'y': 70,
        'festivals': ['Nanda Devi Mela'],
        'crafts': ['Pahadi Candle Craft'],
        'description': 'Lakeside shrine where Nanda-Sunanda Dola processions gather on the Flatts.',
        'vendor_name': 'Nainital Artisans Guild'
    },
    {
        'id': 'bageshwar',
        'name': 'Bageshwar',
        'region': 'Kumaon',
        'division': 'Kumaon',
        'type': 'both',
        'lat': 29.8377,
        'lng': 79.7708,
        'x': 71,
        'y': 46,
        'festivals': ['Uttarayani Fair'],
        'crafts': ['Copperware & Woolen Shawls'],
        'description': 'Sacred Saryu–Gomti river confluence and 10th-century Bagnath Temple.',
        'vendor_name': 'Bagnath Coppersmiths Guild'
    },
    {
        'id': 'pithoragarh',
        'name': 'Pithoragarh',
        'region': 'Kumaon',
        'division': 'Kumaon',
        'type': 'festival',
        'lat': 29.5829,
        'lng': 80.2182,
        'x': 83,
        'y': 50,
        'festivals': ['Hill Jatra', 'Kandali Festival'],
        'crafts': ['Shauka Handlooms'],
        'description': 'Soar valley frontier famed for Lakhia Bhoot mask theatre and Kandali blooms.',
        'vendor_name': 'Soar Valley Artisans'
    },
    {
        'id': 'jauljibi',
        'name': 'Jauljibi',
        'region': 'Kumaon',
        'division': 'Kumaon',
        'type': 'festival',
        'lat': 29.7500,
        'lng': 80.3700,
        'x': 89,
        'y': 42,
        'festivals': ['Jauljibi Fair'],
        'crafts': ['Trans-Border Woolens'],
        'description': 'Kali and Gori river confluence hosting the iconic India–Nepal border trade fair.',
        'vendor_name': 'Jauljibi Border Traders'
    },
    {
        'id': 'munsiyari',
        'name': 'Munsiyari',
        'region': 'Kumaon',
        'division': 'Kumaon',
        'type': 'both',
        'lat': 30.0668,
        'lng': 80.2372,
        'x': 78,
        'y': 32,
        'festivals': ['Bhotia / Shauka Heritage'],
        'crafts': ['Highland Woolen Craft & Dan (GI)'],
        'description': 'Frontier Himalayan village overlooking Panchachuli, home of Dan carpet pit-loom weavers.',
        'vendor_name': 'Maati Women\'s Collective (Sarmoli)'
    },
    {
        'id': 'nauti',
        'name': 'Nauti Village',
        'region': 'Garhwal',
        'division': 'Garhwal',
        'type': 'festival',
        'lat': 30.2520,
        'lng': 79.2310,
        'x': 45,
        'y': 44,
        'festivals': ['Nanda Devi Raj Jat (Base)'],
        'crafts': ['Temple Offerings & Brass Bells'],
        'description': 'Maternal sanctuary (Maika) of Goddess Nanda Devi where the 280-km Raj Jat Yatra begins.',
        'vendor_name': 'Nauti Heritage & Temple Samiti'
    },
    {
        'id': 'wan-village',
        'name': 'Wan Village',
        'region': 'Garhwal',
        'division': 'Garhwal',
        'type': 'festival',
        'lat': 30.1347,
        'lng': 79.6231,
        'x': 50,
        'y': 48,
        'festivals': ['Latu Devta Temple', 'Nanda Raj Jat Stage 9'],
        'crafts': ['Alpine Sheep Woolens'],
        'description': 'The Last Inhabited Village on Earth for the Yatra. Gateway to the sacred alpine wilderness beyond.',
        'vendor_name': 'Wan Village Homestays Cooperative'
    },
    {
        'id': 'homkund',
        'name': 'Homkund (4,061m)',
        'region': 'Garhwal',
        'division': 'Garhwal',
        'type': 'festival',
        'lat': 30.2790,
        'lng': 79.7620,
        'x': 54,
        'y': 38,
        'festivals': ['Nanda Devi Raj Jat (Culmination)'],
        'crafts': ['Brahma Kamal Sanctuary'],
        'description': 'The Last Location! Glacial lake at the foot of Mount Trishul where the Chausingha Khadu is released.',
        'vendor_name': 'Trishul Glacial Sanctuary'
    }
]

# Ensure consistent field aliases for seamless rendering across models and dictionaries
for _fest in FEATURED_FESTIVALS:
    if 'cover_image_url' not in _fest:
        _fest['cover_image_url'] = _fest.get('image', '')
    if 'story_text' not in _fest:
        _fest['story_text'] = _fest.get('full_story') or _fest.get('short_story', '')
    if 'travel_tips' not in _fest:
        _fest['travel_tips'] = _fest.get('local_tips', '')
    if 'venue' not in _fest:
        _fest['venue'] = _fest.get('where_to_experience') or _fest.get('location', '')
    if 'deity_or_ritual' not in _fest:
        _fest['deity_or_ritual'] = _fest.get('cultural_significance', '')
    if 'when_celebrated' not in _fest:
        _fest['when_celebrated'] = _fest.get('date_display', '')


# ==============================================================================
# NANDA DEVI RAJ JAT YATRA: THE HIMALAYAN MAHAKUMBH (DEDICATED CULTURAL DATASET)
# ==============================================================================
NANDA_RAJ_JAT_YATRA = {
    'id': 'nanda-devi-raj-jat-yatra',
    'slug': 'nanda-devi-raj-jat',
    'title': 'Shri Nanda Devi Raj Jat Yatra',
    'hindi_title': 'श्री नंदा देवी राजजात यात्रा',
    'subtitle': 'The Himalayan Mahakumbh & 280-km Barefoot Sacred Pilgrimage',
    'frequency': 'Once every 12 years (12-Year Cycle)',
    'total_distance_km': 280,
    'total_duration_days': '19 – 22 Days',
    'upcoming_yatra_dates': '5 September 2026 – 23 September 2026',
    'culmination_date': '19 September 2026 (Nanda Ashtami / Bhadrapada Shukla Ashtami)',
    'last_conducted_yatra': '18 August – 6 September 2014 (Homkund on 3 September 2014)',
    'cycle_status': '12-Year Cycle (Last: 2014 · Current: 2026–2027 Mahakumbh)',
    'auspicious_window': 'Bhadrapada Shukla Paksha (Pratipada to Ashtami and Dashami)',
    'max_altitude_m': 4850,  # Jurangali Pass
    'max_altitude_label': '4,850 m (15,912 ft) at Jurangali Pass',
    'starting_point': 'Nauti Village (Chamoli, Garhwal) — Altitude 1,450 m',
    'final_destination': 'Homkund Lake (Foot of Mt. Trishul) — Altitude 4,061 m',
    'key_deity': 'Goddess Nanda Devi (Himalayan Daughter & Consort of Lord Shiva)',
    'region': 'Garhwal & Kumaon (Unified Sacred Pilgrimage of Uttarakhand)',
    'district': 'Chamoli',
    'image': '/static/images/Almora/nandadevi.png',
    'banner_image': '/static/images/coverpic/gharwal.png',
    
    # Story & Cultural Significance
    'story_summary': (
        "Regarded as the 'Himalayan Mahakumbh' of Uttarakhand, the Nanda Devi Raj Jat is a legendary "
        "280-kilometer barefoot pilgrimage undertaken once every 12 years. It portrays the intensely emotional "
        "'Vidaai' (bridal departure) of Goddess Nanda Devi—the beloved daughter of the Himalayas—leaving her "
        "maternal childhood home (Maika) at Nauti village to join her divine consort, Lord Shiva, at his eternal "
        "icy abode beneath Mount Trishul. Over three weeks, thousands of pilgrims walk through mist-veiled forests, "
        "river valleys, high alpine bugyals, and glaciated passes, united in devotion."
    ),

    'full_sacred_story': """The Nanda Devi Raj Jat is unlike any other pilgrimage on earth: it is not a pilgrimage to visit a temple, but a moving odyssey to escort a beloved daughter back to her husband's home in the high snows.

In Uttarakhand folk memory, Goddess Nanda is not merely a distant deity, but the elder daughter (Dhyani) of every mountain household. When the auspicious 12-year planetary alignment occurs, hereditary astrologers and priests of Nauti decree the commencement of the Raj Jat. 

From across Chamoli and Tehri, villagers gather at Nauti Village. Leading the procession is the royal golden umbrella (Chhantoli) carried by the Kunwars of Kasuwa, descendants of the ancient Parmar monarchs of Garhwal. Walking freely ahead of all pilgrims is the divine four-horned ram (Chausingha Khadu), miraculously born before each Yatra to carry the offerings of the people.

At Nandkeshari, on the banks of the Pranmati river, a moment of profound unity occurs: hundreds of Kumaoni pilgrims carrying the holy Doli of Nanda from Almora and Nainital merge into the Garhwal procession.

Beyond Wan village—the last inhabited human settlement—the landscape turns supernatural. Pilgrims remove their shoes, walk barefoot through the carpet of wild edelweiss on Bedni Bugyal, pass the ancient skeletal mystery of Roopkund (4,778m), negotiate the razor-edge crest of Jurangali, cross the glacial boulder plain of Shila Samudra, and reach the final sanctuary of Homkund (4,061m) at the feet of Mount Trishul.

There, after the sacred Maha-Yajna, the tears flow freely as the maternal farewell concludes. The four-horned ram is anointed and released: without looking back, it walks alone into the glaciated peaks toward Lord Shiva, vanishing into the eternal Himalayan mists.""",

    'four_horned_ram_lore': (
        "A living miracle at the center of the pilgrimage: prior to each Raj Jat, a male sheep born with "
        "four horns (Chausingha Khadu) is birthed in the village of Kasuwa or surrounding hamlets. The ram is "
        "bathed in mountain herbs, adorned with red vermilion and silken garments, and carries the sacred offerings "
        "(Kanthi, Choli, and ornaments). Unrestrained by rope or leash, the sacred ram guides the procession across "
        "steep rocky cols. At Homkund, it ascends alone into the glacial slopes toward Mount Trishul, carrying "
        "the hopes and prayers of all Uttarakhand into the realm of the gods."
    ),

    'garhwali_kumaoni_unity': (
        "While the pilgrimage trail begins in Garhwal, the Raj Jat is the sacred spiritual bridge uniting Garhwal and "
        "Kumaon. At Nandkeshari camp, the Kumaon procession—bearing the sacred palanquins from Almora, Nainital, and "
        "the Johar Valley—unites with the Garhwal devotees in tears of shared sisterhood, dissolving all geographical "
        "and cultural boundaries."
    ),

    # Live Yatra Status & Checkpoint Progress ("Where Yatra Reach")
    'live_yatra_status': {
        'active_stage_number': 9,
        'current_stage_name': 'Stage 9: Wan Village (2,438 m)',
        'stage_date': '13 September 2026',
        'yatra_window': '5 – 23 September 2026',
        'culmination_date': '19 September 2026 (Nanda Ashtami at Homkund)',
        'current_location_tag': 'The Last Inhabited Village on Earth',
        'status_headline': 'Procession Gathered at the Shrine of Latu Devta in Wan Village',
        'status_description': (
            'The holy procession has arrived at Wan village after covering 105 kilometers across the lower mountain valleys. '
            'Devotees are offering night prayers at the temple of Latu Devta (the divine brother of Nanda Devi). '
            'Tomorrow at dawn, the pilgrimage crosses into the alpine wilderness where shoes, leather items, and modern conveniences '
            'are left behind as pilgrims walk barefoot toward Gairoli Patal and Bedni Bugyal.'
        ),
        'kilometers_covered': 105,
        'remaining_kilometers': 175,
        'next_staging_camp': 'Stage 10: Gairoli Patal (2,800 m) & Bedni Bugyal (3,354 m)',
        'altitude_warning': 'Approaching high-altitude alpine zone. Nighttime temperatures drop to 2°C; oxygen saturation decreases.',
        'last_location_destination': 'Homkund Lake (4,061 m) at the base of Mount Trishul (19 September 2026)'
    },

    # The Last Location & Final Destination Spotlight
    'the_last_location': {
        'name': 'Homkund Lake (होमकुण्ड)',
        'english_tag': 'The Final Sacred Destination & Terminal Point',
        'altitude': '4,061 m (13,323 ft)',
        'culmination_date': '19 September 2026 (Bhadrapad Shukla Ashtami / Nanda Ashtami)',
        'location_description': 'A small glacial tarn nestled in an amphitheater of lateral moraines right below the precipitous south face of Mount Trishul (7,120 m) and Mount Nanda Ghunti (6,309 m) in Chamoli district.',
        'significance': 'The ultimate terrestrial location accessible to mortals. In sacred Himalayan geography, human beings are forbidden to walk beyond Homkund.',
        'what_happens_at_last_location': (
            'At Homkund, the hereditary priests of Nauti perform the grand concluding Maha-Hawan (sacred fire sacrifice). '
            'Devotees offer their jewelry, clothes, and prayers to the Goddess. The tearful final farewell (Vidaai) culminates: '
            'the four-horned ram (Chausingha Khadu) is anointed with red vermilion, silken shawls, and divine offerings, and '
            'tearfully released into the snows. Miraculously, the ram sheds tears, turns toward Mount Trishul, and walks ahead '
            'alone into the glaciated peaks without turning back. No human follows it. Devotees then begin the return descent '
            'via Sutol, Ghat, and Nandprayag.'
        ),
        'survival_warning': 'Extreme high-altitude glaciated terrain. Hypothermia risk, sudden blizzards, and oxygen saturation under 60%. Extreme endurance and permits required.'
    },

    # The 18 Stages of the Pilgrimage Trail
    'stages': [
        {
            'number': 1,
            'name': 'Nauti Village',
            'altitude': '1,450 m',
            'distance': '0 km',
            'day': 'Day 1',
            'date': '5 September 2026',
            'date_short': '5 Sep',
            'tag': 'Pilgrimage Base & Starting Point',
            'significance': 'The sacred maternal home (Maika) of Goddess Nanda Devi. Royal Kunwars of Kasuwa arrive with the Golden Chhantoli, and preliminary Vedic rituals begin.'
        },
        {
            'number': 2,
            'name': 'Idabhadani',
            'altitude': '1,620 m',
            'distance': '10 km',
            'day': 'Day 2',
            'date': '6 September 2026',
            'date_short': '6 Sep',
            'tag': 'Valley Foothills',
            'significance': 'The procession winds through pine forests as village elders perform traditional Mangal Geet farewell songs.'
        },
        {
            'number': 3,
            'name': 'Chandpur Garhi',
            'altitude': '1,600 m',
            'distance': '22 km',
            'day': 'Day 3',
            'date': '7 September 2026',
            'date_short': '7 Sep',
            'tag': 'Historic 9th-Century Fortress',
            'significance': 'Ancient capital of the Parmar dynasty of Garhwal; royal blessings and sanctification of ancient emblems.'
        },
        {
            'number': 4,
            'name': 'Kulsari',
            'altitude': '1,250 m',
            'distance': '34 km',
            'day': 'Day 4',
            'date': '8 September 2026',
            'date_short': '8 Sep',
            'tag': 'Pindar River Confluence',
            'significance': 'Ancient Sun Temple on the banks of Pindar River; night prayers and ritual bath by pilgrims.'
        },
        {
            'number': 5,
            'name': 'Chepdyun',
            'altitude': '1,400 m',
            'distance': '46 km',
            'day': 'Day 5',
            'date': '9 September 2026',
            'date_short': '9 Sep',
            'tag': 'Terraced Hamlets',
            'significance': 'Mountain communities shower fresh barley shoots and wild flower garlands on the Golden Chhantoli.'
        },
        {
            'number': 6,
            'name': 'Nandkeshari',
            'altitude': '1,280 m',
            'distance': '60 km',
            'day': 'Day 6',
            'date': '10 September 2026',
            'date_short': '10 Sep',
            'tag': 'Garhwal & Kumaon Confluence Camp',
            'significance': 'The historic and emotional union! Pilgrims from Almora, Nainital, and Kumaon join the Garhwal Yatra with Goddess Nanda\'s Doli.'
        },
        {
            'number': 7,
            'name': 'Faldiya Gaon',
            'altitude': '1,500 m',
            'distance': '74 km',
            'day': 'Day 7',
            'date': '11 September 2026',
            'date_short': '11 Sep',
            'tag': 'Village Encampment',
            'significance': 'Night-long recitations of ancient Nanda Jagar epics and community bhandara feasts.'
        },
        {
            'number': 8,
            'name': 'Mundoli',
            'altitude': '2,100 m',
            'distance': '92 km',
            'day': 'Day 8',
            'date': '12 September 2026',
            'date_short': '12 Sep',
            'tag': 'Sub-Alpine Ridge',
            'significance': 'Steep climb through ancient deodar and rhododendron groves; motorable vehicle roads end here.'
        },
        {
            'number': 9,
            'name': 'Wan Village',
            'altitude': '2,438 m',
            'distance': '105 km',
            'day': 'Day 9',
            'date': '13 September 2026',
            'date_short': '13 Sep',
            'tag': 'The Last Inhabited Village on Earth',
            'significance': 'The ultimate human settlement on the trail. Here stands the shrine of Latu Devta. Beyond Wan, no human dwellings exist.'
        },
        {
            'number': 10,
            'name': 'Gairoli Patal',
            'altitude': '2,800 m',
            'distance': '117 km',
            'day': 'Day 10',
            'date': '14 September 2026',
            'date_short': '14 Sep',
            'tag': 'Primeval Oak Wilderness',
            'significance': 'Trek through moss-draped forest; mountain winds pick up as pilgrims approach the treeline.'
        },
        {
            'number': 11,
            'name': 'Bedni Bugyal',
            'altitude': '3,354 m',
            'distance': '129 km',
            'day': 'Day 11',
            'date': '15 September 2026',
            'date_short': '15 Sep',
            'tag': 'Sacred Alpine Meadow & Vaitarini Kund',
            'significance': 'Asia\'s grandest alpine meadow with panoramic views of Mount Trishul. Pilgrims take a ritual dip in Vaitarini Kund; all footwear is abandoned here.'
        },
        {
            'number': 12,
            'name': 'Patar Nachauni',
            'altitude': '3,650 m',
            'distance': '138 km',
            'day': 'Day 12',
            'date': '16 September 2026',
            'date_short': '16 Sep',
            'tag': 'High-Altitude Pass Ridge',
            'significance': 'The legend of courtesans petrified into stone columns by Goddess Nanda for dancing inappropriately on the sacred trail.'
        },
        {
            'number': 13,
            'name': 'Baguabasa',
            'altitude': '4,100 m',
            'distance': '148 km',
            'day': 'Day 13',
            'date': '17 September 2026',
            'date_short': '17 Sep',
            'tag': 'Stone Shelter Bivouac Zone',
            'significance': 'Freezing stone shelters amid blooming yellow Brahma Kamal flowers; sub-zero temperatures and thin air.'
        },
        {
            'number': 14,
            'name': 'Roopkund Lake',
            'altitude': '4,778 m',
            'distance': '158 km',
            'day': 'Day 14',
            'date': '18 September 2026',
            'date_short': '18 Sep',
            'tag': 'Glacial Mystery Skeletal Lake',
            'significance': 'The high glacial tarn preserving ancient 9th-century skeletal remains under turquoise ice. Pre-dawn worship is conducted in freezing winds.'
        },
        {
            'number': 15,
            'name': 'Jurangali Pass',
            'altitude': '4,850 m',
            'distance': '164 km',
            'day': 'Day 15',
            'date': '18 September 2026 (Evening)',
            'date_short': '18 Sep',
            'tag': 'Highest Ridge / Alley of Death',
            'significance': 'The narrow knife-edge crest (4,850 m) crossing over from Roopkund into the glaciated amphitheater of Trishul.'
        },
        {
            'number': 16,
            'name': 'Shila Samudra',
            'altitude': '4,200 m',
            'distance': '176 km',
            'day': 'Day 16',
            'date': '19 September 2026 (Pre-Dawn)',
            'date_short': '19 Sep',
            'tag': 'The Sea of Glacial Stones',
            'significance': 'A colossal expanse of moraines and boulders directly beneath the sheer south wall of Mount Trishul.'
        },
        {
            'number': 17,
            'name': 'Homkund (The Last Location)',
            'altitude': '4,061 m',
            'distance': '188 km',
            'day': 'Day 17',
            'date': '19 September 2026 (Nanda Ashtami)',
            'date_short': '19 Sep',
            'tag': 'THE LAST LOCATION & FINAL SACRED CULMINATION',
            'significance': 'The sacred glacial tarn where the final Maha-Hawan is performed on Nanda Ashtami. The four-horned ram is tearfully released toward Mount Trishul, walking alone into the snows.'
        },
        {
            'number': 18,
            'name': 'Sutol & Ghat (Return Trail)',
            'altitude': '2,100 m',
            'distance': '225 km',
            'day': 'Day 18 – 21',
            'date': '20 – 23 September 2026',
            'date_short': '20–23 Sep',
            'tag': 'Descent & Return',
            'significance': 'The quiet return descent through remote virgin valleys of Chamoli back to Nandprayag.'
        }
    ],

    # Sacred Guidelines & Pilgrimage Etiquette
    'pilgrimage_rules': [
        'Strictly barefoot beyond Bedni Bugyal and sacred Vaitarini Kund.',
        'Zero leather tolerance: belts, wallets, shoes, and leather straps are strictly banned.',
        'Zero plastic and non-biodegradable waste policy; sacred alpine bugyals must remain pristine.',
        'Brahma Kamal blossoms are sacred to Goddess Nanda; unauthorized plucking is prohibited.',
        'High-altitude acclimatization is essential; warm thermal layering is mandatory for survival.'
    ],

    # Connected Village Homestays & Guides
    'connected_ecosystem': {
        'homestay_search_url': '/hotels?district=chamoli',
        'homestay_search_label': 'Explore Homestays in Wan, Mundoli & Karnaprayag',
        'guide_search_url': '/guides?district=chamoli',
        'guide_search_label': 'Book Certified High-Altitude Pilgrimage Guides',
        'trip_planner_url': '/plan/?destination=wan-village',
        'trip_planner_label': 'Add Nanda Raj Jat Base Camp to Trip Planner'
    }
}


def get_all_festivals():
    return FEATURED_FESTIVALS


def get_nanda_raj_jat_yatra():
    return NANDA_RAJ_JAT_YATRA


def get_festival_by_slug(slug):
    slug_clean = str(slug).lower().strip()
    for f in FEATURED_FESTIVALS:
        if f['slug'] == slug_clean or f['id'] == slug_clean:
            return f
    # Support common variants
    if slug_clean in ('nanda-devi-raj-jat-yatra', 'nanda-raj-jat', 'raj-jat-yatra', 'raj-jat'):
        return get_festival_by_slug('nanda-devi-raj-jat')
    if slug_clean in ('nanda-devi-mela-nainital', 'nanda-devi-fair-almora'):
        return get_festival_by_slug('nanda-devi-mela')
    if slug_clean in ('uttarayani-fair', 'uttarayani-fair-bageshwar', 'uttarayani'):
        return get_festival_by_slug('uttarayani-kauthig')
    if slug_clean in ('phool-dei-festival',):
        return get_festival_by_slug('phool-dei')
    if slug_clean in ('dyara-bugyal-butter-festival', 'dyara-makha-holi'):
        return get_festival_by_slug('dyara-bugyal-makha-holi')
    if slug_clean in ('rishi-muni-mela',):
        return get_festival_by_slug('rishi-muni-maharaj-mela')
    if slug_clean in ('bada-haat', 'badahat-mela'):
        return get_festival_by_slug('bada-haat-mela')
    if slug_clean in ('kandali',):
        return get_festival_by_slug('kandali-festival')
    if slug_clean in ('syalde-bikhauti-mela',):
        return get_festival_by_slug('syalde-bikhauti')
    return None


def get_living_culture():
    return LIVING_CULTURE


def get_traditional_arts():
    return TRADITIONAL_ARTS


def get_art_by_id(art_id):
    art_clean = str(art_id).lower().strip()
    for a in TRADITIONAL_ARTS:
        if a['id'] == art_clean:
            return a
    return None


def get_map_locations():
    return CULTURAL_MAP_LOCATIONS


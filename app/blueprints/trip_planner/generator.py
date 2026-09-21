import re
import json
import requests
from flask import current_app

# ---------------------------------------------------------------------------
# Natural Language Query Parser
# ---------------------------------------------------------------------------
def parse_natural_trip_query(query_text):
    """
    Parses natural language trip requests like:
    - "4 days almroa trip in 7000"
    - "3 days nainital under 12k"
    - "champawat 2 days solo budget 5000"
    - "weekend in rishikesh with friends"
    """
    if not query_text:
        return {
            'days': 5,
            'budget': 15000,
            'destination': 'almora',
            'group_type': 'couple',
            'interests': ['culture', 'nature'],
            'start_city': 'Delhi'
        }

    text = query_text.lower().strip()

    # 1. Group type & Members count
    members = None
    members_match = re.search(r'(\d+)\s*(?:members?|member|people|persons?|person|pax|travelers?|travellers?|adults?|friends)\b', text)
    if members_match:
        try:
            members = max(1, min(20, int(members_match.group(1))))
        except (ValueError, TypeError):
            members = None

    if not members:
        if re.search(r'\b(solo|alone|single|myself)\b', text):
            members = 1
        elif re.search(r'\b(couple|wife|husband|partner|honeymoon)\b', text):
            members = 2
        elif re.search(r'\b(family|kids|parents|children)\b', text):
            members = 4
        elif re.search(r'\b(friends|buddies|group|gang|boys|girls|college)\b', text):
            members = 4
        else:
            members = 2

    # Group type
    group_type = 'couple'
    if members == 1 or re.search(r'\b(solo|alone|single|myself)\b', text):
        group_type = 'solo'
    elif re.search(r'\b(family|kids|parents|children)\b', text):
        group_type = 'family'
    elif members >= 3 or re.search(r'\b(friends|buddies|group|gang|boys|girls|college)\b', text):
        group_type = 'friends'
    elif re.search(r'\b(couple|wife|husband|partner|honeymoon)\b', text):
        group_type = 'couple'

    # 2. Transport Mode detection (taxi / cab vs personal car vs shared/bus)
    transport_mode = 'personal_car'
    if re.search(r'\b(taxi|cab|cabs|driver|chauffeur|innova|dzire|hire|rental)\b', text):
        transport_mode = 'taxi'
    elif re.search(r'\b(personal\s*car|own\s*car|our\s*car|my\s*car|car|drive|self\s*drive|driving|road\s*trip)\b', text):
        transport_mode = 'personal_car'
    elif re.search(r'\b(bus|jeep|shared|public|train|utc|gmou)\b', text):
        transport_mode = 'shared'

    # 3. Budget parsing
    raw_budget = None
    # match 7k, 12k, 100k
    k_match = re.search(r'(?:in|under|budget|buget|around|approx|₹|rs\.?|inr)?\s*(\d+)\s*(?:k|thousand|l|lakh|lac)\b', text)
    if k_match:
        val = int(k_match.group(1))
        matched_str = k_match.group(0)
        if 'l' in matched_str or 'lakh' in matched_str or 'lac' in matched_str:
            raw_budget = val * 100000
        else:
            raw_budget = val * 1000
    else:
        # match prefix: "in 7000", "under 12000", "budget 8000", "buget 4000", "₹7000", "rs 7000"
        ctx_match = re.search(r'(?:in|under|budget|buget|for|around|approx|₹|rs\.?|inr)\s*(\d{3,7})\b', text)
        if ctx_match:
            raw_budget = int(ctx_match.group(1))
        else:
            # match postfix: "4000 buget", "4000 budget", "4000 rs", "4000 inr", "4000/-"
            postfix_match = re.search(r'(\d{3,7})\s*(?:budget|buget|rs\.?|inr|₹|\/-)\b', text)
            if postfix_match:
                raw_budget = int(postfix_match.group(1))
            else:
                # Standalone 4-7 digit number that is likely budget
                for num in re.findall(r'\b\d{3,7}\b', text):
                    val = int(num)
                    if val >= 500:
                        raw_budget = val
                        break

    if not raw_budget:
        raw_budget = 3500 if 'budget' in text or 'cheap' in text or 'buget' in text else 7000

    # Determine whether budget is TOTAL for the group or PER-PERSON:
    # Default is ALWAYS 'total' unless the user explicitly stated "per person", "per head", "/person", etc.
    is_explicit_per_person = bool(re.search(r'(?:per\s*(?:person|head|pax|each)|\/person|\/head|\/pax)\b', text))
    if is_explicit_per_person:
        budget_type = 'per_person'
        per_person_budget = raw_budget
        total_budget = raw_budget * members
    else:
        budget_type = 'total'
        total_budget = raw_budget
        per_person_budget = max(1, int(total_budget / members))

    # Active budget parameter for compatibility
    budget = total_budget

    # 4. Days parsing
    days = None
    days_explicit = False
    days_match = re.search(r'(\d+)\s*(?:days?|d|day|nights?|n)\b', text)
    if days_match:
        days = int(days_match.group(1))
        days_explicit = True
    elif 'weekend' in text:
        days = 2
        days_explicit = True
    elif 'week' in text:
        days = 7
        days_explicit = True
    elif re.search(r'\b(?:one|1)\s*day\b', text):
        days = 1
        days_explicit = True
    elif re.search(r'\b(?:two|2)\s*days\b', text):
        days = 2
        days_explicit = True
    elif re.search(r'\b(?:three|3)\s*days\b', text):
        days = 3
        days_explicit = True
    elif re.search(r'\b(?:four|4)\s*days\b', text):
        days = 4
        days_explicit = True
    elif re.search(r'\b(?:five|5)\s*days\b', text):
        days = 5
        days_explicit = True

    if days:
        days = max(1, min(14, days))
    else:
        # Intelligent Day Inference based on per-person budget
        if per_person_budget <= 1500:
            days = 1  # Realistic day-trip / excursion for ₹1,000
        elif per_person_budget <= 3500:
            days = 2  # Weekend getaway
        elif per_person_budget <= 7000:
            days = 3
        else:
            days = 4

    # 5. Destination detection restricted strictly to the 4 core districts:
    # 1. Almora, 2. Nainital, 3. Pithoragarh, 4. Uttarkashi
    dest_map = {
        'nainital': ['nainital', 'nanital', 'naini', 'bhital', 'bhimtal', 'mukteshwar', 'pangot', 'sattal', 'lake'],
        'almora': ['almora', 'almroa', 'almorah', 'kasar', 'jageshwar', 'chitai', 'katarmal', 'binsar', 'ranikhet', 'chaubatia', 'kumaon', 'kumaun'],
        'pithoragarh': ['pithoragarh', 'pithoraghar', 'pithoragar', 'munsiyari', 'munsiari', 'panchachuli', 'soar', 'askot', 'champawat', 'bageshwar', 'kausani'],
        'uttarkashi': ['uttarkashi', 'gangotri', 'harsil', 'yamunotri', 'dayara', 'dayara bugyal', 'dodital', 'chopta', 'tungnath', 'kedarnath', 'auli', 'badrinath', 'chamoli', 'haridwar', 'rishikesh', 'dehradun', 'tehri', 'rudraprayag', 'garhwal']
    }

    detected_dest = 'nainital'
    for dest, variants in dest_map.items():
        if any(v in text for v in variants):
            detected_dest = dest
            break

    # 6. Interests
    interests = []
    if re.search(r'\b(culture|cultural|heritage|tradition|aipan|festival|festivals|history|folk)\b', text):
        interests.append('culture')
    if re.search(r'\b(temple|temples|spiritual|divine|puja|aarti|shrine|darshan|shiva)\b', text):
        interests.append('spiritual')
    if re.search(r'\b(trek|trekking|adventure|camp|camping|hike|hiking|rafting)\b', text):
        interests.append('adventure')
    if re.search(r'\b(nature|wildlife|forest|birds|lake|mountains|views|snow|view)\b', text):
        interests.append('nature')
    if re.search(r'\b(food|dishes|thali|cuisine|mithai|sweets|eat|eating|bal mithai)\b', text):
        interests.append('food')
    if re.search(r'\b(art|craft|weaving|shawl|ringal)\b', text):
        interests.append('art')
    if re.search(r'\b(photo|photography|camera|scenic)\b', text):
        interests.append('photography')
    if re.search(r'\b(offbeat|peace|peaceful|quiet|remote|hidden)\b', text):
        interests.append('offbeat')

    if not interests:
        interests = ['culture', 'nature']

    return {
        'days': days,
        'days_explicit': days_explicit,
        'budget': budget,
        'total_budget': total_budget,
        'per_person_budget': per_person_budget,
        'budget_type': budget_type,
        'members': members,
        'transport_mode': transport_mode,
        'destination': detected_dest,
        'group_type': group_type,
        'interests': interests,
        'start_city': 'Delhi'
    }


# ---------------------------------------------------------------------------
# Destination Knowledge Base for Curated Itineraries
# ---------------------------------------------------------------------------
DESTINATION_PLANS = {
    'almora': {
        'title': "Almora Cultural & Heritage Trail",
        'tagline': "Cultural Capital of Kumaon, Ancient Temple Clusters & Himalayan Ridge Vistas",
        'days': [
            {
                "theme": "Arrival, Lala Bazaar & Himalayan Golden Sunset",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Almora Town — Check-in & Orientation",
                        "activity": "Arrive in Almora via Kathgodam/Haldwani route. Check into a traditional Kumaoni homestay nestled along the pine ridges.",
                        "tip": "Homestays near Bright End Corner or Kasar Devi offer sunrise views straight from your balcony under ₹800–₹1,000/night."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Historic Lala Bazaar & Malla Mahal",
                        "activity": "Stroll down the 200-year-old cobblestone pedestrian Lala Bazaar. Visit the historic Chand-era Malla Mahal and the sacred Nanda Devi Temple.",
                        "tip": "Taste authentic warm Bal Mithai (roasted khoya fudge with sugar pearls) and Singodi wrapped in maloo leaves."
                    },
                    {
                        "time": "Evening",
                        "place": "Bright End Corner",
                        "activity": "Watch the sunset over the snowcapped Trishul and Nanda Devi peaks. The twilight glow over the valley is pure poetry.",
                        "tip": "Reach by 5:15 PM with a hot flask of Pahadi chai."
                    }
                ]
            },
            {
                "theme": "Kasar Devi Geomagnetic Ridge & Crank's Ridge",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Kasar Devi Temple & Meditation Caves",
                        "activity": "Visit the world-renowned geomagnetic energy ridge (Van Allen belt zone) where Swami Vivekananda, Rabindranath Tagore, and Bob Dylan meditated.",
                        "tip": "Sit quietly in the ancient rock cave beneath the main shrine for a surreal, peaceful experience."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Crank's Ridge Trail & Mohan Joshi Park",
                        "activity": "Walk along the scenic pine-draped ridge overlooking the snow peaks. Stop by local artisan workshops showcasing sacred Aipan ritual art.",
                        "tip": "Shared jeeps from Almora taxi stand to Kasar Devi cost just ₹20–₹30."
                    },
                    {
                        "time": "Evening",
                        "place": "Simtola Pine Woods & Village Sunset Cafe",
                        "activity": "Enjoy a quiet evening in the whispering deodar and pine groves of Simtola. Enjoy ginger-lemon-honey tea and hot Pahadi Maggi.",
                        "tip": "Look out for Himalayan whistling thrushes and red-billed blue magpies."
                    }
                ]
            },
            {
                "theme": "Jageshwar Dham — Sacred 124 Stone Shrines",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Jageshwar Dham Temple Complex",
                        "activity": "Take a 35 km scenic journey through dense cedar forests to the 124 9th-century stone shrines of Jageshwar, one of the 12 sacred Jyotirlinga circuits.",
                        "tip": "Shared cabs leave Almora bus terminal frequently (₹80–₹100 per seat)."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Vriddha Jageshwar & Dandeshwar Shrines",
                        "activity": "Trek 1.5 km up the pine trail to Vriddha Jageshwar for 360-degree Himalayan vistas, followed by the towering riverside Dandeshwar temple cluster.",
                        "tip": "The ancient stone water-springs (dhara) here have sweet, pristine mountain water."
                    },
                    {
                        "time": "Evening",
                        "place": "Traditional Kumaoni Dhaba Dining",
                        "activity": "Relish a traditional Pahadi thali — Bhatt ki Churkani (black soybean stew), Aloo ke Gutke with jakhiya, Maduwa (millet) rotis, and Jhangora kheer.",
                        "tip": "Wholesome village thalis cost around ₹120–₹160 per person."
                    }
                ]
            },
            {
                "theme": "Katarmal Sun Temple & Chitai Golu Devta",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Katarmal Sun Temple (Baraditya)",
                        "activity": "Visit the 9th-century Sun Temple perched on a scenic knoll with exquisite Katyuri pillar carvings, second only to Konark.",
                        "tip": "The morning sun rays strike the main deity sanctum directly — an architectural marvel."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Chitai Golu Devta — God of Justice",
                        "activity": "Visit the legendary temple of justice, draped with tens of thousands of ringing brass bells and handwritten stamp-paper petitions from pilgrims.",
                        "tip": "Offer a small brass bell (₹50–₹100) and write your wish on the temple register."
                    },
                    {
                        "time": "Evening",
                        "place": "Local Craft Bazaars & Departure",
                        "activity": "Pick up handwoven Ringal bamboo crafts, copper water vessels from Almora's coppersmiths (Tamta community), and organic Pahadi spices before departure.",
                        "tip": "UTC state buses to Haldwani/Kathgodam depart hourly from Almora bus station."
                    }
                ]
            },
            {
                "theme": "Binsar Wildlife Sanctuary & Zero Point Hike",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Binsar Wildlife Sanctuary",
                        "activity": "Morning jungle drive through oak and rhododendron forests to Zero Point, the highest peak in Almora district (2,412 m).",
                        "tip": "Panoramic 300 km view of Himalayan peaks including Kedarnath, Trishul, and Nanda Devi."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Mary Budden Estate & Gairar Golu Devta",
                        "activity": "Gentle forest hike through ancient British-era bridle trails to the forest temple of Gairar.",
                        "tip": "Carry binoculars for birdwatching; Binsar hosts over 200 bird species."
                    },
                    {
                        "time": "Evening",
                        "place": "Sunset over Kosi Valley",
                        "activity": "Return through the pine canopy to your homestay for a bonfire and local storytelling session with your host.",
                        "tip": "Homestay hosts love sharing folk ballads of legendary King Golu Devta."
                    }
                ]
            }
        ]
    },

    'nainital': {
        'title': "Nainital Lakes & Pine Ridges Trail",
        'tagline': "Emerald Waters, Colonial Heritage & Himalayan Lookouts",
        'days': [
            {
                "theme": "Arrival, Naini Lake & Sacred Naina Devi",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Naini Lake Boating",
                        "activity": "Arrive in Nainital and take a traditional wooden gondola or sailboat ride across the emerald crescent lake.",
                        "tip": "Early morning boat rides (before 9 AM) have calm waters and mountain mist reflections."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Naina Devi Shakti Peeth",
                        "activity": "Visit the sacred lakeside temple where Goddess Sati's eyes fell, located at the northern edge of the lake (Mallital).",
                        "tip": "Dress respectfully; the brass prayer bells offer immense tranquility."
                    },
                    {
                        "time": "Evening",
                        "place": "Mall Road & Tibetan Bhotia Bazaar",
                        "activity": "Walk along the pedestrian Mall Road. Try local Thukpa, Momos, and hot mountain coffee in the Tibetan market.",
                        "tip": "Pick up handmade scented wax candles, a specialty of Nainital's cottage artisans."
                    }
                ]
            },
            {
                "theme": "Dorothy's Seat & Snow View Point",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Tiffin Top (Dorothy's Seat) Trek",
                        "activity": "A refreshing 4 km forested walk through deodars to Ayarpatta Hill for panoramic 360° valley views.",
                        "tip": "Pony rides are available, but walking the shaded trail is deeply rejuvenating."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Snow View Point & Aerial Ropeway",
                        "activity": "Take the cable car to Snow View Point to witness the majestic Nanda Devi and Trishul mountain range.",
                        "tip": "Binocular telescopes at the viewpoint show peak contours clearly."
                    },
                    {
                        "time": "Evening",
                        "place": "Eco Cave Gardens",
                        "activity": "Explore natural interconnected rocky caves named after Himalayan fauna (Tiger Cave, Panther Cave, Bat Cave).",
                        "tip": "Wear sturdy shoes with good grip."
                    }
                ]
            },
            {
                "theme": "Naini Peak & Quiet Pangot Bird Sanctuary",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Naini Peak (China Peak) Summit Trek",
                        "activity": "Trek up to the highest point in Nainital (2,615 m) for an awe-inspiring vista of the entire town and snow wall.",
                        "tip": "Start at 6 AM; pack water and light local roasted soybeans."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Pangot Forest & Kilbury Sanctuary",
                        "activity": "Drive 15 km to peaceful Pangot village, famous for oak forests and rare Himalayan birds like cheer pheasants.",
                        "tip": "Shared taxis run between Mallital and Pangot."
                    },
                    {
                        "time": "Evening",
                        "place": "Bhimtal & Sattal Excursion",
                        "activity": "Visit the picturesque lake island aquarium of Bhimtal and the seven interconnected freshwater lakes of Sattal.",
                        "tip": "Kayaking at Sattal is much quieter and cleaner than the main lake."
                    }
                ]
            }
        ]
    },

    'champawat': {
        'title': "Champawat Ancient Citadel & Spiritual Trail",
        'tagline': "10th-Century Stone Architecture, Sacred Peaks & Quiet Tea Gardens",
        'days': [
            {
                "theme": "Chand Dynasty Stone Marvels & Golu Devta Birthplace",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Baleshwar Temple Complex",
                        "activity": "Explore the 10th-century ASI-protected dark granite temple built by the Chand Kings with celestial apsara stone carvings.",
                        "tip": "Notice the carved stone ceiling mandalas and dragon-headed waterspouts."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Golu Devta Temple Champawat",
                        "activity": "Visit the ancestral seat and birthplace of Golu Devta, surrounded by quiet mountain ridges.",
                        "tip": "Hear the legendary ballads of Golu Devta from the hereditary priests."
                    },
                    {
                        "time": "Evening",
                        "place": "Champawat Heritage Town Walk",
                        "activity": "Walk through traditional stone-slate roofed homes, meeting local coppersmiths and Aipan artisans.",
                        "tip": "Try authentic local Bhatt ki Daal and Dubuk."
                    }
                ]
            },
            {
                "theme": "Sacred Purnagiri & Serene Shyamlatal",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Maa Purnagiri Shakti Peeth",
                        "activity": "Ascend the sacred mountain shrine overlooking the Sharda River and Nepal border plains.",
                        "tip": "Start early to beat the pilgrim queue and enjoy cool mountain breeze."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Shyamlatal Lake & Vivekananda Ashram",
                        "activity": "Visit the tranquil dark-emerald lake and the historic Ramakrishna Vivekananda Ashram established in 1914.",
                        "tip": "The ashram library and meditation hall provide supreme peace."
                    },
                    {
                        "time": "Evening",
                        "place": "Abbott Mount Pine Ridge",
                        "activity": "Walk through the colonial-era church and pine trails of Abbott Mount with views of the snow peaks.",
                        "tip": "Catch the twilight crimson glow over Mount Trishul."
                    }
                ]
            }
        ]
    },

    'pithoragarh': {
        'title': "Pithoragarh & Munsiyari Himalayan Frontier",
        'tagline': "Five Glacial Peaks of Panchachuli & Bhotia Tribal Heritage",
        'days': [
            {
                "theme": "Soar Valley & Historic Chand Fort",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Pithoragarh Fort",
                        "activity": "Climb up to the 18th-century Chand hilltop fort commanding breathtaking views of the entire Soar amphitheater valley.",
                        "tip": "The morning mist lifting over the terraced fields is magical."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Kapileshwar Mahadev Cave Temple",
                        "activity": "Descend into the ancient 10-meter deep natural limestone cave temple dedicated to Lord Shiva.",
                        "tip": "Carry a small flashlight for observing the natural stalactite formations."
                    },
                    {
                        "time": "Evening",
                        "place": "Soar Valley Bazaar",
                        "activity": "Taste locally roasted Bal Mithai and explore Pithoragarh's handloom wool shops.",
                        "tip": "Authentic sheep wool socks and mufflers are incredibly warm and durable."
                    }
                ]
            },
            {
                "theme": "Munsiyari & The Panchachuli Peaks",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Scenic Drive & Birthi Falls",
                        "activity": "Spectacular 120 km mountain drive across Kalamuni Pass (2,700 m) with a stop at the 126m roaring Birthi Waterfall.",
                        "tip": "At Kalamuni top, ring the brass bells at the Kali temple for safe travels."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Munsiyari Panchachuli Viewpoint",
                        "activity": "Arrive in Munsiyari where the five legendary peaks of Panchachuli rise straight up outside your window.",
                        "tip": "Homestays in Sarmoli village offer genuine Bhotia tribal hospitality."
                    },
                    {
                        "time": "Evening",
                        "place": "Tribal Heritage Museum & Darkot Village",
                        "activity": "Visit Dr. S.S. Pangtey's museum preserving Bhotia tribal tools and history; watch women weave Pashmina and Angora shawls.",
                        "tip": "Support local village women's cooperatives directly by purchasing handlooms."
                    }
                ]
            }
        ]
    },

    'rishikesh': {
        'title': "Rishikesh Spiritual & Adventure Gateway",
        'tagline': "Sacred Ganges, Yoga Shalas, Suspension Bridges & Forest Falls",
        'days': [
            {
                "theme": "Ganga Aarti, Ram Jhula & Ashrams",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Ram Jhula & Laxman Jhula Trails",
                        "activity": "Cross the iconic suspension bridges and visit the quiet spiritual ashrams of Swarg Ashram and Geeta Bhawan.",
                        "tip": "Early morning riverside walks offer refreshing mountain breezes."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Beatles Ashram (Chaurasi Kutia)",
                        "activity": "Explore the graffitied meditation domes inside Rajaji National Park where The Beatles composed the White Album in 1968.",
                        "tip": "The stone eco-domes and vintage murals make for memorable photography."
                    },
                    {
                        "time": "Evening",
                        "place": "Triveni Ghat Evening Maha Aarti",
                        "activity": "Participate in the soul-stirring Ganga Aarti with hundreds of floating earthen oil lamps (diyas) dancing on the water.",
                        "tip": "Arrive by 5:30 PM to get seated right by the water steps."
                    }
                ]
            },
            {
                "theme": "River Rafting & Neer Garh Waterfall",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "White-Water Rafting on the Ganges",
                        "activity": "Experience an exhilarating 12 km or 16 km rafting run through rapids like 'Roller Coaster' and 'Golf Course'.",
                        "tip": "Always wear certified life jackets and follow your river guide's signals."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Neer Garh Natural Waterfall",
                        "activity": "A gentle 20-minute hike up through the jungle to natural stepped turquoise pools cascading from the hills.",
                        "tip": "Dip your feet in the cool mountain stream."
                    },
                    {
                        "time": "Evening",
                        "place": "Riverside Ayurvedic Cafe",
                        "activity": "Unwind with herbal tea, Ayurvedic khichdi, and fresh organic salads with live acoustic classical music.",
                        "tip": "Try Little Buddha Cafe or Beatles Cafe in Tapovan."
                    }
                ]
            }
        ]
    },
    'chamoli': {
        'title': "Chamoli & Auli Alpine Expedition",
        'tagline': "Auli Ski Meadows, UNESCO Valley of Flowers & Sacred High Himalayan Shrines",
        'days': [
            {
                "theme": "Auli Meadows, Cable Car & Nanda Devi Panoramic Vista",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Auli Ropeway & High Bugyal",
                        "activity": "Ride Asia's longest cable car from Joshimath to Auli (2,519m), stepping onto lush alpine meadows with front-row views of Nanda Devi.",
                        "tip": "Carry sunglasses; the high-altitude glare on snow and grass is intense."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Auli Artificial Lake & Meadow Trail",
                        "activity": "Hike around the turquoise artificial lake designed for winter snow-making. Enjoy views of Hathi and Ghoda Parbat peaks.",
                        "tip": "Gentle 3km walk suitable for all ages and fitness levels."
                    },
                    {
                        "time": "Evening",
                        "place": "Sunset Bonfire Deck",
                        "activity": "Watch the sunset turn Mount Nanda Devi from brilliant white to deep crimson gold while sipping steaming Pahadi Kahwa.",
                        "tip": "Temperature drops rapidly after 5:30 PM; bundle up in fleece."
                    }
                ]
            },
            {
                "theme": "Mana Village & Badrinath Sacred Heritage",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Sacred Badrinath Temple",
                        "activity": "Visit one of India's four supreme Chardham shrines along the Alaknanda river, framed by the Nar and Narayana mountain ranges.",
                        "tip": "Take a sacred dip in the natural thermal springs of Tapt Kund before darshan."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Mana — The First Indian Village",
                        "activity": "Walk through the border hamlet of Mana (3,200m). Visit Vyas Gufa where the Mahabharata was dictated, and the dramatic natural stone bridge of Bheem Pul.",
                        "tip": "Stop at India's 'First Tea Stall' for herbal tea and homemade barley cookies."
                    },
                    {
                        "time": "Evening",
                        "place": "Joshimath Shankaracharya Math",
                        "activity": "Explore the historic monastery established by Adi Shankaracharya in the 8th century and the revered 2,500-year-old Kalpavriksha tree.",
                        "tip": "Peaceful atmosphere with evening Vedic prayers."
                    }
                ]
            },
            {
                "theme": "UNESCO Valley of Flowers & Floral Sanctuaries",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Valley of Flowers Gateway Trail",
                        "activity": "Trek through the Pushpawati river gorge amidst over 500 species of wild Himalayan blooms including blue poppies and Brahma Kamal.",
                        "tip": "Peak blooming season is July to September; entry permits are issued at the gate."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Mary Legge Memorial & Alpine Streams",
                        "activity": "Picnic beside crystalline glacial streams in the core valley zone surrounded by mist-draped granite cliffs.",
                        "tip": "Pack all litter back; this is a strict zero-plastic UNESCO sanctuary."
                    },
                    {
                        "time": "Evening",
                        "place": "Ghangaria Forest Hamlet",
                        "activity": "Return to the pine hamlet of Ghangaria for hot ginger tea, warm blankets, and wholesome lentil soup.",
                        "tip": "Reliable homestays with hot water buckets available."
                    }
                ]
            }
        ]
    },
    'rudraprayag': {
        'title': "Chopta, Tungnath & Chandrashila Trail",
        'tagline': "Mini Switzerland of Uttarakhand, World's Highest Shiva Temple & 4,000m Peak",
        'days': [
            {
                "theme": "Arrival, Sari Village & Emerald Deoria Tal",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Sari Village Base Camp",
                        "activity": "Arrive in the traditional Garhwali stone hamlet of Sari. Check into an authentic village homestay surrounded by apple trees.",
                        "tip": "Try home-churned butter with warm Mandua (millet) rotis."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Trek to Deoria Tal (2,438m)",
                        "activity": "Take the scenic 2.5 km stone-paved forest trail through rhododendron groves to the sacred high lake of Deoria Tal.",
                        "tip": "The reflection of Chaukhamba peaks on the water surface at 3 PM is jaw-dropping."
                    },
                    {
                        "time": "Evening",
                        "place": "Meadow Stargazing & Bonfire",
                        "activity": "Experience pristine night skies with clear views of the Milky Way galaxy, completely free from city light pollution.",
                        "tip": "Pack a warm beanie and gloves; night winds can be chilly."
                    }
                ]
            },
            {
                "theme": "Tungnath (3,680m) & Chandrashila Summit (4,000m)",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Chopta to Tungnath Temple Ascent",
                        "activity": "Early 6 AM ascent on the 3.5 km stone trail to Tungnath, the highest Shiva temple on Earth, perched majestically against the clouds.",
                        "tip": "The ancient stone shrine dates back over 1,000 years according to local lore."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Chandrashila 4,000m Summit Vista",
                        "activity": "Climb the final steep 1.5 km ridge to the Chandrashila peak for an unparalleled 360-degree panoramic view of Nanda Devi, Trishul, and Kedar Dome.",
                        "tip": "Breathtaking ridge walk; take slow, deep breaths at this altitude."
                    },
                    {
                        "time": "Evening",
                        "place": "Chopta Meadow Cafe & Hot Pahadi Thali",
                        "activity": "Descend back to Chopta meadows for hot steaming rajma, Pahadi potato gutke with local jakhiya seeds, and fresh chai.",
                        "tip": "Local meadow dhabas serve hearty, warming food under ₹150."
                    }
                ]
            },
            {
                "theme": "Sacred Rudraprayag Sangam & Confluence",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Alaknanda-Mandakini Confluence",
                        "activity": "Witness the dramatic confluence of the roaring grey waters of Alaknanda and the emerald green torrent of Mandakini.",
                        "tip": "Sit at the ghat steps where sage Narada is believed to have worshipped."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Ukhimath Omkareshwar Temple",
                        "activity": "Visit the sacred winter seat of Kedarnath and Madhyamaheshwar, where the deities are worshipped when the high temples are snowbound.",
                        "tip": "Intricate wooden carvings and rich Garhwali festival traditions."
                    },
                    {
                        "time": "Evening",
                        "place": "Riverside Sunset Walk",
                        "activity": "Peaceful sunset stroll along the riverside promenade listening to temple bells and river rapids.",
                        "tip": "Relaxing conclusion to an alpine trekking journey."
                    }
                ]
            }
        ]
    },
    'uttarkashi': {
        'title': "Uttarkashi, Harsil & Gangotri Frontier Trail",
        'tagline': "Sacred Bhagirathi River Gorge, Fairy-Tale Apple Valleys & High Alpine Meadows",
        'days': [
            {
                "theme": "Uttarkashi Heritage & Kashi Vishwanath Shrine",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Kashi Vishwanath Temple Uttarkashi",
                        "activity": "Visit the ancient Shiva temple on the banks of Bhagirathi, featuring the legendary 12-meter copper-alloy Shakti trident.",
                        "tip": "Morning aarti is peaceful and deeply grounding."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Nehru Institute of Mountaineering (NIM)",
                        "activity": "Explore India's premier mountaineering museum documenting historic Himalayan ascents, Everest artifacts, and mountaineering lore.",
                        "tip": "Entry open to visitors; excellent documentary screenings."
                    },
                    {
                        "time": "Evening",
                        "place": "Bhagirathi Riverside Promenade",
                        "activity": "Stroll down the river walk and enjoy local Garhwali snacks: warm Singori and wild mountain mint chutney.",
                        "tip": "Comfortable riverside dhabas with river views."
                    }
                ]
            },
            {
                "theme": "Harsil Valley & Gartang Gali Cliff Trail",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Harsil Apple Orchards & River Hamlet",
                        "activity": "Drive 70 km along the roaring Bhagirathi gorge to Harsil (2,745m), famous for sweet apples, deodar woods, and traditional wooden homes.",
                        "tip": "Taste fresh cold-pressed apple juice directly from village orchard owners."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Gartang Gali Historic Cliff Boardwalk",
                        "activity": "Walk along the 150-year-old wooden cantilever bridge carved into a sheer granite gorge, historically used by Bhotia and Tibetan traders.",
                        "tip": "Pre-register online or at the checkpost; spectacular cliff photography."
                    },
                    {
                        "time": "Evening",
                        "place": "Bagori Traditional Bhotia Village",
                        "activity": "Visit Bagori village across the wooden suspension bridge. Meet local artisans weaving pure sheep-wool shawls and carpets on wooden pit looms.",
                        "tip": "Support local tribal weavers directly without middlemen."
                    }
                ]
            },
            {
                "theme": "Gangotri Temple & Sacred River Origin",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Gangotri Dham Temple (3,100m)",
                        "activity": "Visit the white granite temple dedicated to Goddess Ganga where King Bhagiratha did penance to bring the holy river from heaven to earth.",
                        "tip": "The Bhagirath Shila near the temple is where King Bhagiratha meditated."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Surya Kund & Gauri Kund Waterfalls",
                        "activity": "Walk 500m downstream to watch the thunderous falls where the river has carved deep, twisting potholes through solid granite.",
                        "tip": "The roar of the river echoing through the gorge is unforgettable."
                    },
                    {
                        "time": "Evening",
                        "place": "Ashram Tea & Mountain Farewell",
                        "activity": "Sit quietly in one of the riverside ashrams with a cup of hot herbal tea watching the twilight fade over the Sudarshan peak.",
                        "tip": "Pristine mountain silence."
                    }
                ]
            }
        ]
    },
    'haridwar': {
        'title': "Haridwar Ancient Ghats & Vedic Lore",
        'tagline': "Gateway of the Gods, Hypnotic Ganga Aarti & Ancient Ashrams",
        'days': [
            {
                "theme": "Har Ki Pauri, Sacred Dip & Evening Maha Aarti",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Har Ki Pauri & Brahmakund",
                        "activity": "Early morning sacred dip at the famous Brahmakund where drops of Amrit (immortality nectar) fell from the celestial urn.",
                        "tip": "The water is surprisingly clear and refreshing in the early morning."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Moti Bazaar Street Food & Heritage Walk",
                        "activity": "Wander through the narrow historic lanes of Moti Bazaar. Taste famous kachoris, bedmi puris, and sweet kulhad lassi.",
                        "tip": "Visit Kashiram Purivala and Mathura Walo ki Pracheen Dukan."
                    },
                    {
                        "time": "Evening",
                        "place": "Har Ki Pauri Sunset Maha Aarti",
                        "activity": "Witness the world-famous evening Ganga Aarti with thousands of singing pilgrims, giant brass fire-lamps, and floating flower boats.",
                        "tip": "Arrive by 5:15 PM on the opposite bank (Malviya Dweep) for prime viewing."
                    }
                ]
            },
            {
                "theme": "Mansa Devi & Chandi Devi Ridge Shrines",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Mansa Devi Temple & Udankhatola Ropeway",
                        "activity": "Take the scenic cable car up Bilwa Parvat for panoramic vistas of Haridwar city and the meandering channels of the Ganges.",
                        "tip": "Combo cable car tickets for both Mansa and Chandi Devi save money and time."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Chandi Devi Temple on Neel Parvat",
                        "activity": "Cross over to the south bank and ride up Neel Parvat to the ancient shrine established by Adi Shankaracharya in the 8th century.",
                        "tip": "Monkeys are active; keep prasad bags safely inside your backpack."
                    },
                    {
                        "time": "Evening",
                        "place": "Kankhal Daksha Mahadev Temple",
                        "activity": "Visit the mythological kingdom of King Daksha and the serene temple site of Goddess Sati's yajna along the old canal.",
                        "tip": "Peaceful atmosphere far away from the busy main market."
                    }
                ]
            }
        ]
    },
    'dehradun': {
        'title': "Dehradun, Rishikesh & Foothills Trail",
        'tagline': "Ganges Spiritual Corridors, Robber's Cave & Deodar Foothills",
        'days': [
            {
                "theme": "Rishikesh Yoga, Suspension Bridges & Ganga Aarti",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Ram Jhula & Tapovan Riverside Walk",
                        "activity": "Cross the suspension bridges and visit quiet ashrams along the sacred river banks.",
                        "tip": "Join an early morning riverside yoga session by the water."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Beatles Ashram (Chaurasi Kutia)",
                        "activity": "Wander through the graffitied stone meditation domes inside Rajaji National Park where The Beatles composed their music.",
                        "tip": "Great forest atmosphere and artistic murals."
                    },
                    {
                        "time": "Evening",
                        "place": "Triveni Ghat Evening Aarti",
                        "activity": "Experience the devotional Ganga Aarti with Vedic chanting and oil lamps reflected on the river.",
                        "tip": "Arrive 45 minutes before sunset for riverfront seating."
                    }
                ]
            },
            {
                "theme": "Dehradun Natural Wonders & Limestone Canyons",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Robber's Cave (Guchhupani)",
                        "activity": "Wade barefoot through a cool natural limestone cave stream where water flows between 10-meter-high cliff walls.",
                        "tip": "Wear slippers or sandals; water is usually ankle to knee-deep."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Tapkeshwar Mahadev Cave Temple",
                        "activity": "Visit the natural cave shrine dedicated to Lord Shiva where natural spring water continuously drips upon the Shivling.",
                        "tip": "Located inside a peaceful deodar-lined river hollow."
                    },
                    {
                        "time": "Evening",
                        "place": "Rajpur Road Cafes & Tibetan Market",
                        "activity": "Explore Dehradun's famous bakery heritage, steamed momos, and fragrant Dehraduni Basmati cuisine.",
                        "tip": "Try famous Ellora's Melting Moments rusks and sticky toffee."
                    }
                ]
            }
        ]
    },
    'bageshwar': {
        'title': "Bageshwar, Kausani & Katyuri Trail",
        'tagline': "300km Snow Panorama, Anasakti Ashram & 7th-Century Confluence",
        'days': [
            {
                "theme": "Kausani 300km Himalayan Panorama & Anasakti Ashram",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Kausani Sunrise Over Nanda Devi",
                        "activity": "Watch the legendary 180-degree sunrise over the Trishul, Nanda Devi, and Panchachuli peaks that Mahatma Gandhi called the Switzerland of India.",
                        "tip": "Wake up at 5:30 AM for the pristine morning alpine glow."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Anasakti Ashram & Memorial",
                        "activity": "Explore the historic ashram where Gandhi wrote his treatise on the Bhagavad Gita. Stroll through the surrounding organic tea estates.",
                        "tip": "Visit the tea factory to sample authentic organic green and orthodox black teas."
                    },
                    {
                        "time": "Evening",
                        "place": "Rudradhari Falls & Forest Walk",
                        "activity": "A peaceful 1.5 km nature hike through terraced paddy fields and pine woods to a natural cascading waterfall and ancient Shiva cave.",
                        "tip": "Carry a water bottle and wear comfortable walking shoes."
                    }
                ]
            },
            {
                "theme": "Sacred Bagnath Shrine & Saryu Confluence",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Bagnath Temple Bageshwar",
                        "activity": "Visit the revered 7th-century stone temple standing at the confluence of the sacred Saryu and Gomti rivers.",
                        "tip": "Site of the historic 1921 Uttarayani non-cooperation gathering."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Baijnath Katyuri Temple Complex",
                        "activity": "Drive 20 km to the 12th-century stone temple cluster on the banks of the Gomti river, housing magnificent black stone statues of Goddess Parvati.",
                        "tip": "Watch hundreds of golden Mahseer fish swimming peacefully in the temple pool."
                    },
                    {
                        "time": "Evening",
                        "place": "Traditional Kumaoni Riverbank Dinner",
                        "activity": "Enjoy traditional Gahat (horsegram) soup, Dubke, and hot Mandua rotis at a local riverside homestay.",
                        "tip": "Nutritious, authentic mountain cuisine."
                    }
                ]
            }
        ]
    },
    'tehri': {
        'title': "Tehri Dam Turquoise Lake & Dhanaulti Pines",
        'tagline': "Asia's Tallest Dam Watersports, Deodar Eco Parks & Mist-Clad Ridges",
        'days': [
            {
                "theme": "Tehri Lake Watersports & Reservoir Cruise",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Tehri Lake Watersports Hub",
                        "activity": "Experience open-water jet-skiing, speedboating, and kayaking across the massive emerald reservoir of Tehri Dam.",
                        "tip": "Government-regulated life jackets and certified safety boats accompany every tour."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Floating Huts & Lakeside Promenade",
                        "activity": "Relax on a pontoon deck floating directly on the tranquil reservoir with views of surrounding rugged peaks.",
                        "tip": "Enjoy fresh local fish curry or organic Garhwali vegetarian thali."
                    },
                    {
                        "time": "Evening",
                        "place": "New Tehri Viewpoint & Sunset",
                        "activity": "Drive to the town overlook to watch the sunset illuminate the sprawling turquoise expanse of Asia's tallest dam.",
                        "tip": "Unbelievable scale; great wide-angle panoramic photo spot."
                    }
                ]
            },
            {
                "theme": "Dhanaulti Deodar Woods & Surkanda Devi Peak",
                "stops": [
                    {
                        "time": "Morning",
                        "place": "Dhanaulti Eco Park Pine Trail",
                        "activity": "Walk amidst towering deodar cedars and mossy oaks in the tranquil Eco Park, with gentle mountain breezes.",
                        "tip": "Quiet, restorative forest walk far from highway noise."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Surkanda Devi Temple Ridge (2,757m)",
                        "activity": "Take the scenic ropeway or 1.5 km climb to the ancient Shakti Peeth shrine perched on an isolated conical peak.",
                        "tip": "Offers an extraordinary 360-degree vista of both the snow Himalayas and the Doon valley."
                    },
                    {
                        "time": "Evening",
                        "place": "Kanatal Pine Cabin & Bonfire",
                        "activity": "Spend a peaceful evening in a rustic pine-wood cottage with a crackling woodstove and homemade pahadi dinner.",
                        "tip": "Crisp mountain night air; ideal for rest and rejuvenation."
                    }
                ]
            }
        ]
    },
    'kumaon': {
        'title': "Grand Kumaon Heritage Circuit",
        'tagline': "From Emerald Lakes to Living Aipan Lanes & Five Glacial Peaks",
        'days': [
            {
                "theme": "Day 1: Nainital Lakes & British Heritage",
                "stops": [
                    {"time": "Morning", "place": "Naini Lake Boating", "activity": "Early paddleboat ride on emerald waters.", "tip": "Start at 7 AM."},
                    {"time": "Afternoon", "place": "Naina Devi Temple", "activity": "Sacred Shakti Peeth on the lake edge.", "tip": "Respect temple queues."},
                    {"time": "Evening", "place": "Naini Peak Walk", "activity": "Sunset vista across the Himalayan wall.", "tip": "Pack warm layers."}
                ]
            },
            {
                "theme": "Day 2: Almora Cultural Living Heritage",
                "stops": [
                    {"time": "Morning", "place": "Lala Bazaar Cobblestones", "activity": "Explore 200-year-old stone bazaar and Bal Mithai.", "tip": "Taste Sarthi Sweets."},
                    {"time": "Afternoon", "place": "Kasar Devi Energy Ridge", "activity": "Visit the magnetic Van Allen belt meditation caves.", "tip": "Quiet contemplation."},
                    {"time": "Evening", "place": "Chitai Golu Devta Shrine", "activity": "Temple of Justice hung with thousands of brass bells.", "tip": "Ring the bell for justice."}
                ]
            },
            {
                "theme": "Day 3: Jageshwar Dham Deodar Forest Shrines",
                "stops": [
                    {"time": "Morning", "place": "124 Stone Shrines of Jageshwar", "activity": "Primordial Shiva Jyotirlinga in ancient cedar woods.", "tip": "Attend morning aarti."},
                    {"time": "Afternoon", "place": "Vriddha Jageshwar Ridge", "activity": "High ridge trek with 360° snow peak views.", "tip": "Drink sweet spring water."},
                    {"time": "Evening", "place": "Pahadi Thali Experience", "activity": "Wholesome Bhatt ki Churkani and Madua roti.", "tip": "Local village dhabas."}
                ]
            }
        ]
    },
    'garhwal': {
        'title': "Grand Garhwal Spiritual & High Alpine Circuit",
        'tagline': "Holy Ganges River Ghats, Chopta Meadows & Auli Snow Slopes",
        'days': [
            {
                "theme": "Day 1: Haridwar & Rishikesh Ganges Corridor",
                "stops": [
                    {"time": "Morning", "place": "Har Ki Pauri Sacred Dip", "activity": "Holy river dip at the sacred Brahmakund.", "tip": "Early morning is serene."},
                    {"time": "Afternoon", "place": "Beatles Ashram Rishikesh", "activity": "Graffitied meditation domes in the jungle.", "tip": "Quiet forest walk."},
                    {"time": "Evening", "place": "Triveni Ghat Evening Aarti", "activity": "Hypnotic fire aarti with floating lamps.", "tip": "Arrive 45 mins early."}
                ]
            },
            {
                "theme": "Day 2: Chopta Alpine Meadows & Tungnath",
                "stops": [
                    {"time": "Morning", "place": "Trek to Tungnath (3,680m)", "activity": "Ascent to the highest Shiva shrine on Earth.", "tip": "Pace your climb."},
                    {"time": "Afternoon", "place": "Chandrashila 4,000m Summit", "activity": "360-degree panorama of Nanda Devi and Trishul.", "tip": "Unmatched view."},
                    {"time": "Evening", "place": "Chopta Meadow Camp", "activity": "Bonfire and stargazing under the Milky Way.", "tip": "Warm fleece is essential."}
                ]
            },
            {
                "theme": "Day 3: Auli Ski Meadows & High Peaks",
                "stops": [
                    {"time": "Morning", "place": "Auli Cable Car & Bugyal", "activity": "Ride Asia's longest ropeway into high meadows.", "tip": "Stunning ridge views."},
                    {"time": "Afternoon", "place": "Badrinath & Mana Village", "activity": "Sacred shrine and First Indian Village.", "tip": "Taste tea at Last Tea Stall."},
                    {"time": "Evening", "place": "Joshimath Mountain Inn", "activity": "Relaxing evening overlooking Alaknanda valley.", "tip": "Wholesome dinner."}
                ]
            }
        ]
    }
}

# ---------------------------------------------------------------------------
# Verified Uttarakhand Transit & Fares Database
# ---------------------------------------------------------------------------
TRANSIT_DATABASE = {
    'almora': {
        'destination_name': 'Almora',
        'nearest_railway_station': {
            'name': 'Kathgodam Railway Station',
            'code': 'KGM',
            'distance_km': 82,
            'travel_time': '2.5 – 3 hrs',
            'route': 'NH 109 via Bhowali, Garampani & Khairna',
            'train_connections': 'Direct express trains to Delhi (Kathgodam Shatabdi 12040, Ranikhet Express 15014, Uttar Sampark Kranti 15036), Dehradun, Lucknow, and Kolkata.'
        },
        'secondary_railway_station': {
            'name': 'Haldwani Railway Station',
            'code': 'HDW',
            'distance_km': 88,
            'travel_time': '3 hrs'
        },
        'nearest_airport': {
            'name': 'Pantnagar Airport',
            'code': 'PGH',
            'distance_km': 115,
            'travel_time': '3.5 – 4 hrs',
            'flight_connections': 'Daily direct flights to Delhi (IndiGo & Alliance Air).'
        },
        'trip_end_transit_summary': {
            'hub_name': 'Kathgodam Railway Station (KGM)',
            'distance': '82 km',
            'departure_advice': 'For your departure back home, Kathgodam (KGM) is the primary railhead. Shared Maxx/Bolero taxis depart from Almora KMOU Station / Mall Road continuously from 6:00 AM to 4:30 PM (₹250–₹350/seat). For evening trains like Kathgodam Shatabdi (dep 15:35) or Ranikhet Express (dep 20:35), leave Almora at least 4 hours prior.'
        },
        'personal_car_logistics': {
            'start_point': 'Almora Town (Mall Road / Kasar Devi base). If driving up from Delhi/NCR: take NH 9 to Rampur, then NH 109 via Rudrapur, Haldwani, Kathgodam, Bhowali, Garampani, Khairna (360 km, 8–9 hrs).',
            'parking_facilities': 'Designated Almora Multi-level Municipal Parking (Mallital, near Hotel Shikhar) at ₹80–₹100/day. Private parking available at ridge homestays along Kasar Devi & Crank\'s Ridge.',
            'driving_safety': 'Check brake pads, tire treads, and coolant before ascending from Kathgodam. Use engine braking (2nd or 3rd gear) on downhill hairpins. Maintain uphill right of way on single-lane ghat curves.',
            'estimated_fuel_km': '110 km local circuit in hills (~₹1,200 – ₹1,500 fuel + ₹150 toll/entry)'
        },
        'taxi_fares': [
            {
                'service_type': 'Kathgodam to Almora Private Cab (Sedan)',
                'vehicle': 'Maruti Dzire / Toyota Etios (Heater/AC)',
                'capacity': 'Up to 4 passengers',
                'fare': '₹2,200 – ₹2,600',
                'badge': 'Most Popular'
            },
            {
                'service_type': 'Kathgodam to Almora Private Cab (SUV)',
                'vehicle': 'Toyota Innova / Maruti Ertiga',
                'capacity': 'Up to 6–7 passengers',
                'fare': '₹3,200 – ₹3,800',
                'badge': 'Family & Luggage'
            },
            {
                'service_type': 'Shared Mountain Taxi (Bolero / Maxx)',
                'vehicle': 'Mahindra Bolero / Commander (Taxi Union)',
                'capacity': 'Per seat basis',
                'fare': '₹250 – ₹350 / seat',
                'badge': 'Budget Friendly'
            },
            {
                'service_type': 'UTC State Transport Bus',
                'vehicle': 'Uttarakhand Parivahan Nigam (Ordinary/Semi-Deluxe)',
                'capacity': 'Scheduled departures from Haldwani/Kathgodam ISBT',
                'fare': '₹180 – ₹220 / seat',
                'badge': 'Public Transit'
            },
            {
                'service_type': 'Almora Full-Day Sightseeing Cab',
                'vehicle': 'Local Union Taxi (Jageshwar + Kasar Devi + Chitai)',
                'capacity': '8 Hours / 80 km coverage',
                'fare': '₹2,000 – ₹2,400 / day',
                'badge': 'Sightseeing Package'
            }
        ]
    },
    'nainital': {
        'destination_name': 'Nainital',
        'nearest_railway_station': {
            'name': 'Kathgodam Railway Station',
            'code': 'KGM',
            'distance_km': 34,
            'travel_time': '1 – 1.2 hrs',
            'route': 'NH 109 via Ranibagh & Jeolikote',
            'train_connections': 'Frequent direct express trains connecting Delhi, Dehradun, Lucknow, and Howrah.'
        },
        'secondary_railway_station': {
            'name': 'Haldwani Railway Station',
            'code': 'HDW',
            'distance_km': 40,
            'travel_time': '1.3 hrs'
        },
        'nearest_airport': {
            'name': 'Pantnagar Airport',
            'code': 'PGH',
            'distance_km': 70,
            'travel_time': '2 hrs',
            'flight_connections': 'Daily direct regional connections to Delhi.'
        },
        'trip_end_transit_summary': {
            'hub_name': 'Kathgodam Railway Station (KGM)',
            'distance': '34 km',
            'departure_advice': 'Kathgodam is just 1 hour descent from Tallital Taxi Stand. Frequent shared taxis (₹120–₹160/seat) and direct UTC buses (₹65–₹85) run every 20 minutes from 5:30 AM to 8:00 PM.'
        },
        'personal_car_logistics': {
            'start_point': 'Nainital Town (Mallital / Tallital). Inbound from Delhi via Moradabad, Rampur, Bazpur, Kaladhungi (305 km, 6.5–7 hrs) or via Haldwani/Kathgodam (315 km).',
            'parking_facilities': 'Sukhatal Parking, Ashok Cinema Parking, or Tallital Multi-level Parking (₹150–₹250/day). Note: Personal vehicles are barred on Mall Road during peak evening hours (6:00 PM to 8:30 PM).',
            'driving_safety': 'Steep hairpins between Jeolikote and Tallital. Maintain uphill right of way. Keep low gears engaged on rainy days.',
            'estimated_fuel_km': '70 km local lakes circuit (~₹800 – ₹1,100 fuel + ₹100 toll)'
        },
        'taxi_fares': [
            {
                'service_type': 'Kathgodam to Nainital Private Cab (Sedan)',
                'vehicle': 'Maruti Dzire / Indigo',
                'capacity': 'Up to 4 passengers',
                'fare': '₹1,000 – ₹1,300',
                'badge': 'Quick Transit'
            },
            {
                'service_type': 'Kathgodam to Nainital Private Cab (SUV)',
                'vehicle': 'Innova / Ertiga / Scorpio',
                'capacity': 'Up to 6–7 passengers',
                'fare': '₹1,600 – ₹2,000',
                'badge': 'Spacious SUV'
            },
            {
                'service_type': 'Shared Taxi / Maxx',
                'vehicle': 'Station Taxi Stand to Tallital',
                'capacity': 'Per seat basis',
                'fare': '₹120 – ₹160 / seat',
                'badge': 'Budget Pick'
            },
            {
                'service_type': 'UTC State Bus',
                'vehicle': 'Uttarakhand Transport Corp',
                'capacity': 'Frequent departures from Kathgodam/Haldwani',
                'fare': '₹65 – ₹85 / seat',
                'badge': 'State Bus'
            },
            {
                'service_type': 'Lake District Day Tour Cab',
                'vehicle': 'Local Taxi (Bhimtal, Sattal, Naukuchiatal round-trip)',
                'capacity': 'Full day 6–7 hours',
                'fare': '₹1,800 – ₹2,300 / day',
                'badge': 'Lake Tour'
            }
        ]
    },
    'uttarkashi': {
        'destination_name': 'Uttarkashi',
        'nearest_railway_station': {
            'name': 'Rishikesh Railway Station (Yog Nagari Rishikesh)',
            'code': 'YNRK',
            'distance_km': 165,
            'travel_time': '5 – 5.5 hrs',
            'route': 'NH 34 via Chamba, Dharasu Bend & Bhagirathi Valley',
            'train_connections': 'Express and superfast connectivity to Delhi, Mumbai, Ahmedabad, and Jammu.'
        },
        'secondary_railway_station': {
            'name': 'Dehradun Railway Station',
            'code': 'DDN',
            'distance_km': 145,
            'travel_time': '5 hrs via Mussoorie / Suwakholi bypass'
        },
        'nearest_airport': {
            'name': 'Jolly Grant Airport, Dehradun',
            'code': 'DED',
            'distance_km': 160,
            'travel_time': '5.5 hrs',
            'flight_connections': 'Major domestic hub with direct flights to Delhi, Mumbai, Bangalore, and Lucknow.'
        },
        'trip_end_transit_summary': {
            'hub_name': 'Rishikesh (YNRK) / Dehradun (DDN)',
            'distance': '165 km',
            'departure_advice': 'For return journey, plan early morning departure from Uttarkashi. Shared Bolero/Maxx jeeps depart Ramlila Ground taxi stand starting at 5:30 AM to Rishikesh Natraj Chowk (₹450–₹600/seat). Mountain travel takes 5.5 hours along the Bhagirathi river gorge.'
        },
        'personal_car_logistics': {
            'start_point': 'Uttarkashi Town (Gangori or Bhatwari Road). Inbound from Dehradun/Rishikesh via Narendra Nagar, Chamba, and Dharasu Bend on NH 34 (165 km, 5.5 hrs).',
            'parking_facilities': 'Municipal Parking near Vishwanath Temple, Ramlila Ground, and hotel courtyards (₹60–₹100/day).',
            'driving_safety': 'Mountain road with narrow gorge stretches. Drive carefully near Dharasu and steep ascents to Harsil/Gangotri. Watch for falling stones during monsoon or early spring.',
            'estimated_fuel_km': '190 km valley circuit (~₹2,200 – ₹2,700 fuel)'
        },
        'taxi_fares': [
            {
                'service_type': 'Rishikesh/Haridwar to Uttarkashi Dedicated Sedan',
                'vehicle': 'Maruti Dzire / Etios',
                'capacity': 'Up to 4 passengers',
                'fare': '₹3,600 – ₹4,200',
                'badge': 'Direct Private Cab'
            },
            {
                'service_type': 'Rishikesh to Uttarkashi Dedicated SUV',
                'vehicle': 'Toyota Innova / Mahindra Scorpio',
                'capacity': 'Up to 6–7 passengers',
                'fare': '₹5,200 – ₹6,000',
                'badge': 'Hill SUV'
            },
            {
                'service_type': 'Shared Mountain Taxi (Bolero)',
                'vehicle': 'Rishikesh Natraj Chowk to Uttarkashi',
                'capacity': 'Per seat basis',
                'fare': '₹450 – ₹600 / seat',
                'badge': 'Shared Jeep'
            },
            {
                'service_type': 'UTC / GMOU Bus',
                'vehicle': 'Garhwal Mandal Owners Union & UTC',
                'capacity': 'Early morning daily buses',
                'fare': '₹280 – ₹360 / seat',
                'badge': 'State Transit'
            },
            {
                'service_type': 'Uttarkashi to Harsil Valley & Gangotri Cab',
                'vehicle': 'Local Hill Taxi (Full-day Himalayan excursion)',
                'capacity': 'Full day ~180 km mountain route',
                'fare': '₹3,600 – ₹4,400 / day',
                'badge': 'Himalayan Tour'
            }
        ]
    },
    'pithoragarh': {
        'destination_name': 'Pithoragarh',
        'nearest_railway_station': {
            'name': 'Tanakpur Railway Station',
            'code': 'TPU',
            'distance_km': 138,
            'travel_time': '4.5 hrs',
            'route': 'NH 9 via Champawat, Lohaghat & Ghat',
            'train_connections': 'Express trains to Delhi, Bareilly, and Lucknow.'
        },
        'secondary_railway_station': {
            'name': 'Kathgodam Railway Station',
            'code': 'KGM',
            'distance_km': 188,
            'travel_time': '6.5 hrs via Almora & Ghat'
        },
        'nearest_airport': {
            'name': 'Naini Saini Airport (Regional) / Pantnagar Airport',
            'code': 'PGH',
            'distance_km': 210,
            'travel_time': '7 hrs',
            'flight_connections': 'Regional helicopter / small craft flights to Dehradun (Naini Saini); regular commercial flights from Pantnagar.'
        },
        'trip_end_transit_summary': {
            'hub_name': 'Tanakpur (TPU) / Kathgodam (KGM)',
            'distance': '138 km / 188 km',
            'departure_advice': 'Departure shared cabs start from Siltham Taxi Stand as early as 5:00 AM to Tanakpur or Haldwani. Book shared seats a day in advance during holiday seasons.'
        },
        'personal_car_logistics': {
            'start_point': 'Pithoragarh Town (Siltham / KMVN base). Inbound from plains via Tanakpur, Champawat, Lohaghat, Ghat on all-weather NH 9 (138 km from Tanakpur, 4.5 hrs).',
            'parking_facilities': 'KMVN Tourist Rest House complex, Siltham Municipal Ground (₹60–₹100/day).',
            'driving_safety': 'High altitude bends, morning fog near Lohaghat passes. Ensure good tires and fuel up at Ghat or Lohaghat before the final ridge ascent.',
            'estimated_fuel_km': '210 km mountain circuit (~₹2,400 – ₹3,000 fuel)'
        },
        'taxi_fares': [
            {
                'service_type': 'Kathgodam/Tanakpur to Pithoragarh Dedicated Sedan',
                'vehicle': 'Maruti Dzire / Etios',
                'capacity': 'Up to 4 passengers',
                'fare': '₹4,400 – ₹5,200',
                'badge': 'Long Distance Cab'
            },
            {
                'service_type': 'Kathgodam/Tanakpur to Pithoragarh Dedicated SUV',
                'vehicle': 'Innova / Bolero Camper',
                'capacity': 'Up to 6–7 passengers',
                'fare': '₹6,400 – ₹7,400',
                'badge': 'Rugged SUV'
            },
            {
                'service_type': 'Shared Bolero / Cruiser',
                'vehicle': 'Siltham / Haldwani Taxi Stand',
                'capacity': 'Per seat basis',
                'fare': '₹600 – ₹750 / seat',
                'badge': 'Shared Mountain Jeep'
            },
            {
                'service_type': 'UTC State Bus',
                'vehicle': 'Uttarakhand Parivahan Nigam',
                'capacity': 'Daily morning bus service',
                'fare': '₹350 – ₹450 / seat',
                'badge': 'State Bus'
            },
            {
                'service_type': 'Soar Valley & Mostamanu Sightseeing Cab',
                'vehicle': 'Local Pithoragarh Taxi',
                'capacity': 'Full day local exploration',
                'fare': '₹2,200 – ₹2,800 / day',
                'badge': 'Local Valley Tour'
            }
        ]
    }
}


# ---------------------------------------------------------------------------
# Dynamic Itinerary Generator (Local & Gemini-backed)
# ---------------------------------------------------------------------------
def generate_itinerary(days=4, budget=7000, group_type='couple', interests=None, start_city='Delhi', destination='almora', prompt='', members=2, budget_type='total', transport_mode='personal_car'):
    """
    Generates a rich, day-by-day itinerary tailored to the requested parameters.
    Attempts real Gemini API if configured; otherwise generates high-fidelity
    authentic Uttarakhand travel plans from the domain database.
    """
    dest_key = (destination or 'almora').lower().strip()
    if dest_key not in DESTINATION_PLANS:
        # Fallback to almora if unrecognized
        for k in DESTINATION_PLANS:
            if k in dest_key:
                dest_key = k
                break
        else:
            dest_key = 'almora'

    try:
        members = max(1, int(members or 2))
    except (ValueError, TypeError):
        members = 2

    transport_mode = transport_mode or 'personal_car'
    if transport_mode not in ['personal_car', 'taxi', 'shared']:
        if 'taxi' in str(transport_mode).lower() or 'cab' in str(transport_mode).lower():
            transport_mode = 'taxi'
        elif 'bus' in str(transport_mode).lower() or 'shared' in str(transport_mode).lower():
            transport_mode = 'shared'
        else:
            transport_mode = 'personal_car'

    # Compute total_budget and per_person_budget
    if budget_type == 'per_person':
        per_person_budget = max(400, int(budget))
        total_budget = per_person_budget * members
    else:
        total_budget = max(500, int(budget))
        per_person_budget = max(1, int(total_budget / members))

    # Try calling Gemini if API key is present
    api_key = current_app.config.get('GEMINI_API_KEY')
    if api_key and not current_app.config.get('STUB_AI', True):
        gemini_result = _call_gemini_rest(prompt, days, total_budget, per_person_budget, members, transport_mode, group_type, interests, start_city, dest_key, api_key)
        if gemini_result:
            dest_transit = TRANSIT_DATABASE.get(dest_key, TRANSIT_DATABASE['almora'])
            pc_stay = int(total_budget * 0.40)
            pc_fuel = min(max(400, int(total_budget * 0.25)), 2500)
            pc_parking = min(max(100, int(total_budget * 0.05)), 400)
            pc_food = int(total_budget * 0.22)
            pc_activities = max(50, total_budget - (pc_stay + pc_fuel + pc_parking + pc_food))
            pc_total = pc_stay + pc_fuel + pc_parking + pc_food + pc_activities

            personal_car_plan = {
                'title': 'Personal Car (Self-Drive)',
                'subtitle': 'Own vehicle / Road trip with mountain parking & fuel',
                'icon': 'car',
                'stay': pc_stay,
                'fuel': pc_fuel,
                'parking_tolls': pc_parking,
                'food': pc_food,
                'activities': pc_activities,
                'total': pc_total,
                'per_person': max(1, int(pc_total / members)),
                'highlights': [
                    f"Hill circuit fuel & ascent from Kathgodam/plain (~₹{pc_fuel:,})",
                    f"Designated municipal parking ({dest_transit['personal_car_logistics']['parking_facilities'].split('(')[0].strip()})",
                    "Full freedom for sunset points & offbeat hill trails"
                ]
            }

            pt_stay = int(total_budget * 0.40)
            pt_transit = min(max(400, int(total_budget * 0.26)), 2600)
            pt_food = int(total_budget * 0.22)
            pt_activities = max(50, total_budget - (pt_stay + pt_transit + pt_food))
            pt_total = pt_stay + pt_transit + pt_food + pt_activities

            public_transport_plan = {
                'title': 'Public Transport & Shared Cabs',
                'subtitle': 'UTC state buses + Taxi Union shared Boleros + local jeeps',
                'icon': 'bus',
                'stay': pt_stay,
                'transit': pt_transit,
                'food': pt_food,
                'activities': pt_activities,
                'total': pt_total,
                'per_person': max(1, int(pt_total / members)),
                'highlights': [
                    f"Railhead connecting cabs ({dest_transit['nearest_railway_station']['name']})",
                    "Shared mountain Boleros & local KMOU/UTC hill buses",
                    "Zero parking hassle in crowded heritage town bazaars"
                ]
            }

            transit_info = {
                'destination_name': dest_transit['destination_name'],
                'nearest_railway_station': dest_transit['nearest_railway_station'],
                'secondary_railway_station': dest_transit.get('secondary_railway_station'),
                'nearest_airport': dest_transit['nearest_airport'],
                'trip_end_transit_summary': dest_transit['trip_end_transit_summary'],
                'personal_car_logistics': dest_transit['personal_car_logistics'],
                'taxi_fares': dest_transit['taxi_fares'],
                'personal_car_plan': personal_car_plan,
                'public_transport_plan': public_transport_plan
            }
            min_total = int(total_budget * 0.88)
            max_total = total_budget
            total_formatted = f"₹{min_total:,} – ₹{max_total:,} total"

            min_per_person = int(per_person_budget * 0.88)
            max_per_person = per_person_budget
            per_person_formatted = f"₹{min_per_person:,} – ₹{max_per_person:,} per person"

            gemini_result['transit_info'] = transit_info
            gemini_result['members'] = members
            gemini_result['transport_mode'] = transport_mode
            gemini_result['budget_type'] = budget_type
            gemini_result['total_budget'] = total_budget
            gemini_result['per_person_budget'] = per_person_budget
            gemini_result['total_budget_formatted'] = total_formatted
            gemini_result['per_person_budget_formatted'] = per_person_formatted
            gemini_result['budget_estimate'] = total_formatted if members > 1 else per_person_formatted
            gemini_result['budget_target'] = total_budget if budget_type == 'total' else per_person_budget
            gemini_result['destination'] = dest_key.title()
            gemini_result['days_count'] = days
            cb_stay = max(50, int(per_person_budget * 0.40))
            cb_transit = max(50, int(per_person_budget * 0.25))
            cb_food = max(50, int(per_person_budget * 0.25))
            cb_act = max(20, per_person_budget - (cb_stay + cb_transit + cb_food))
            gemini_result['cost_breakdown_per_person'] = {
                'stay': cb_stay,
                'transit': cb_transit,
                'food': cb_food,
                'activities': cb_act
            }
            gemini_result['cost_breakdown'] = gemini_result['cost_breakdown_per_person']
            gemini_result['cost_breakdown_total'] = {
                'stay': cb_stay * members,
                'transit': cb_transit * members,
                'food': cb_food * members,
                'activities': cb_act * members
            }
            group_desc = {
                'solo': "solo backpacker",
                'couple': "couple",
                'family': f"family of {members}",
                'friends': f"group of {members} friends"
            }.get(group_type, f"{members} travelers")
            trans_desc = {
                'personal_car': "by personal car (self-drive)",
                'taxi': "with dedicated taxi/cab",
                'shared': "via shared mountain jeeps & buses"
            }.get(transport_mode, "")
            gemini_result['summary'] = (
                f"A tailored {days}-day journey through {dest_key.title()} for a {group_desc} {trans_desc}, "
                f"crafted for a total budget of ₹{total_budget:,} (~₹{per_person_budget:,} per person). "
                f"Experience ancient heritage stone shrines, cobblestone bazaars, peaceful pine trails, and authentic regional cuisine."
            )
            return gemini_result

    # High-quality dynamic generator
    plan_data = DESTINATION_PLANS.get(dest_key, DESTINATION_PLANS['almora'])
    dest_name = dest_key.title()
    available_days = plan_data['days']

    generated_days = []
    total_available = len(available_days)

    for i in range(days):
        day_num = i + 1
        if i < total_available:
            src_day = available_days[i]
            clean_theme = re.sub(r'^Day\s*\d+\s*[:\-]\s*', '', src_day['theme'])
            generated_days.append({
                "day": day_num,
                "theme": f"Day {day_num}: {clean_theme}",
                "stops": src_day['stops']
            })
        else:
            # Generate extra days dynamically based on destination
            extra_idx = (i - total_available) % 3
            if extra_idx == 0:
                theme = f"Day {day_num}: Offbeat Pine Forests & Village Craft Trail"
                stops = [
                    {
                        "time": "Morning",
                        "place": f"{dest_name} Rural Homestay Excursion",
                        "activity": "Morning walk through terraced organic farms and pine groves. Learn traditional grain harvesting and Aipan ritual patterns.",
                        "tip": "Homestay hosts love teaching traditional pottery and cooking."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Hidden Stream & Forest Ridge Picnic",
                        "activity": "Gentle hike down to a mountain freshwater stream with packed organic millet rotis and homemade wild berry chutney.",
                        "tip": "The water is crystalline; pack a camera for butterfly sightings."
                    },
                    {
                        "time": "Evening",
                        "place": "Village Council Square & Folk Tales",
                        "activity": "Evening bonfire with village elders recounting mountain folklore and the brave history of Kumaoni regiments.",
                        "tip": "Sip hot herbal rhododendron (Buransh) tea."
                    }
                ]
            elif extra_idx == 1:
                theme = f"Day {day_num}: Sacred Ridge & Panoramic Summit Trek"
                stops = [
                    {
                        "time": "Morning",
                        "place": f"{dest_name} High Ridge Viewpoint",
                        "activity": "Early 5:30 AM sunrise hike to watch the first golden rays illuminate the Trishul, Nanda Kot, and Nanda Devi peaks.",
                        "tip": "Dress in warm layers; mornings are brisk and crisp."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Ancient Katyuri Stone Shrines",
                        "activity": "Visit hidden centuries-old stone stepwells (naulas) and intricately carved guardian shrines in the cedar forest.",
                        "tip": "Ancient naulas have natural architectural filtration systems."
                    },
                    {
                        "time": "Evening",
                        "place": "Local Market & Sweet Confectionery",
                        "activity": "Browse traditional brass and copper utensil shops and taste seasonal mountain sweets like Singodi and Bal Mithai.",
                        "tip": "Buy locally grown rajma, hemp seeds (bhang jeera), and mountain honey."
                    }
                ]
            else:
                theme = f"Day {day_num}: Peaceful Meditation & Farewell Journey"
                stops = [
                    {
                        "time": "Morning",
                        "place": f"{dest_name} Valley Lookout",
                        "activity": "Relaxing yoga and pranayama session overlooking the mist-filled river valley.",
                        "tip": "The mountain air is pure and revitalizing."
                    },
                    {
                        "time": "Afternoon",
                        "place": "Artisan Cooperatives & Souvenirs",
                        "activity": "Support local women's cooperatives by purchasing handwoven shawls, natural essential oils, and herbal teas.",
                        "tip": "Fair-trade certified items directly support local families."
                    },
                    {
                        "time": "Evening",
                        "place": "Return Departure via Scenic Foothill Highway",
                        "activity": f"Board your return bus/taxi to Kathgodam/Dehradun connecting to {start_city}.",
                        "tip": "Keep mountain road motion sickness tablets handy if needed."
                    }
                ]
            generated_days.append({
                "day": day_num,
                "theme": theme,
                "stops": stops
            })

    # Transport label, description, and icon
    if transport_mode == 'taxi':
        transit_label = "Private Taxi / Dedicated Cab"
        transit_desc = "Dedicated cab & hill driver"
        transit_icon = "car"
    elif transport_mode == 'shared':
        transit_label = "Shared Jeeps & GMOU Buses"
        transit_desc = "Local mountain shared transit"
        transit_icon = "bus"
    else:
        transit_label = "Personal Car (Fuel, Tolls & Parking)"
        transit_desc = "Own vehicle / self-drive route"
        transit_icon = "car"

    # Contextual tips for selected transport mode
    if generated_days and len(generated_days) > 0 and 'stops' in generated_days[0] and len(generated_days[0]['stops']) > 0:
        first_stop = generated_days[0]['stops'][0]
        if transport_mode == 'personal_car':
            first_stop['tip'] = first_stop.get('tip', '') + " • Personal Car Tip: Check brakes & coolant before hill ascent; multi-level parking available near Mallital/town center."
        elif transport_mode == 'taxi':
            first_stop['tip'] = first_stop.get('tip', '') + " • Taxi Tip: Your private driver will drop you at the hotel doorstep and coordinate local sightseeing timing."

    # Budget range calculations strictly adhering to user's specified budget
    min_total = int(total_budget * 0.88)
    max_total = total_budget
    total_formatted = f"₹{min_total:,} – ₹{max_total:,} total"

    min_per_person = int(per_person_budget * 0.88)
    max_per_person = per_person_budget
    per_person_formatted = f"₹{min_per_person:,} – ₹{max_per_person:,} per person"

    if members > 1:
        budget_formatted = total_formatted
    else:
        budget_formatted = per_person_formatted

    # Itemized cost breakdown (per person and group total)
    cb_stay = max(50, int(per_person_budget * 0.40))
    cb_transit = max(50, int(per_person_budget * 0.25))
    cb_food = max(50, int(per_person_budget * 0.25))
    cb_act = max(20, per_person_budget - (cb_stay + cb_transit + cb_food))

    cost_breakdown_per_person = {
        'stay': cb_stay,
        'transit': cb_transit,
        'food': cb_food,
        'activities': cb_act
    }

    cost_breakdown_total = {
        'stay': cb_stay * members,
        'transit': cb_transit * members,
        'food': cb_food * members,
        'activities': cb_act * members
    }

    cost_breakdown = cost_breakdown_per_person

    # Dual Budget Calculations: Personal Car (Self-Drive) vs Public Transport
    dest_transit = TRANSIT_DATABASE.get(dest_key, TRANSIT_DATABASE['almora'])
    
    # 1. Personal Car Plan (strictly scaled within total_budget)
    pc_stay = int(total_budget * 0.40)
    pc_fuel = min(max(400, int(total_budget * 0.25)), 2500)
    pc_parking = min(max(100, int(total_budget * 0.05)), 400)
    pc_food = int(total_budget * 0.22)
    pc_activities = max(50, total_budget - (pc_stay + pc_fuel + pc_parking + pc_food))
    pc_total = pc_stay + pc_fuel + pc_parking + pc_food + pc_activities

    personal_car_plan = {
        'title': 'Personal Car (Self-Drive)',
        'subtitle': 'Own vehicle / Road trip with mountain parking & fuel',
        'icon': 'car',
        'stay': pc_stay,
        'fuel': pc_fuel,
        'parking_tolls': pc_parking,
        'food': pc_food,
        'activities': pc_activities,
        'total': pc_total,
        'per_person': max(1, int(pc_total / members)),
        'highlights': [
            f"Hill circuit fuel & ascent from Kathgodam/plain (~₹{pc_fuel:,})",
            f"Designated municipal parking ({dest_transit['personal_car_logistics']['parking_facilities'].split('(')[0].strip()})",
            "Full freedom for sunset points & offbeat hill trails"
        ]
    }

    # 2. Public Transport & Shared Cabs Plan (strictly scaled within total_budget)
    pt_stay = int(total_budget * 0.40)
    pt_transit = min(max(400, int(total_budget * 0.26)), 2600)
    pt_food = int(total_budget * 0.22)
    pt_activities = max(50, total_budget - (pt_stay + pt_transit + pt_food))
    pt_total = pt_stay + pt_transit + pt_food + pt_activities

    public_transport_plan = {
        'title': 'Public Transport & Shared Cabs',
        'subtitle': 'UTC state buses + Taxi Union shared Boleros + local jeeps',
        'icon': 'bus',
        'stay': pt_stay,
        'transit': pt_transit,
        'food': pt_food,
        'activities': pt_activities,
        'total': pt_total,
        'per_person': max(1, int(pt_total / members)),
        'highlights': [
            f"Railhead connecting cabs ({dest_transit['nearest_railway_station']['name']})",
            "Shared mountain Boleros & local KMOU/UTC hill buses",
            "Zero parking hassle in crowded heritage town bazaars"
        ]
    }

    transit_info = {
        'destination_name': dest_transit['destination_name'],
        'nearest_railway_station': dest_transit['nearest_railway_station'],
        'secondary_railway_station': dest_transit.get('secondary_railway_station'),
        'nearest_airport': dest_transit['nearest_airport'],
        'trip_end_transit_summary': dest_transit['trip_end_transit_summary'],
        'personal_car_logistics': dest_transit['personal_car_logistics'],
        'taxi_fares': dest_transit['taxi_fares'],
        'personal_car_plan': personal_car_plan,
        'public_transport_plan': public_transport_plan
    }

    # Feasibility check: if per-day per-person budget is very low (< ₹750/day)
    daily_budget = int(per_person_budget / max(1, days))
    budget_warning = None
    if daily_budget < 750:
        recommended_total = days * 900 * members
        budget_warning = (
            f"Budget Calibration Notice: ₹{total_budget:,} for {days} days ({members} travelers) works out to ~₹{daily_budget:,}/person/day. "
            f"This itinerary is calibrated for an ultra-budget backpacker route utilizing government dharamshalas, "
            f"shared dorms, and local GMOU state buses. For a comfortable private homestay experience, we recommend ~₹{recommended_total:,}."
        )

    group_desc = {
        'solo': "solo backpacker",
        'couple': "couple",
        'family': f"family of {members}",
        'friends': f"group of {members} friends"
    }.get(group_type, f"{members} travelers")

    trans_desc = {
        'personal_car': "by personal car (self-drive)",
        'taxi': "with dedicated taxi/cab",
        'shared': "via shared mountain jeeps & buses"
    }.get(transport_mode, "")

    summary = (
        f"A tailored {days}-day journey through {dest_name} for a {group_desc} {trans_desc}, "
        f"crafted for a total budget of ₹{total_budget:,} (~₹{per_person_budget:,} per person). "
        f"Experience ancient heritage stone shrines, cobblestone bazaars, peaceful pine trails, and authentic regional cuisine."
    )

    raw_title = plan_data.get('title', 'Himalayan Journey')
    if dest_name.lower() in raw_title.lower():
        title = f"{days}-Day {raw_title}"
    else:
        title = f"{days}-Day {dest_name} {raw_title}"

    return {
        "title": title,
        "summary": summary,
        "destination": dest_name,
        "budget_estimate": budget_formatted,
        "total_budget": total_budget,
        "total_budget_formatted": total_formatted,
        "per_person_budget": per_person_budget,
        "per_person_budget_formatted": per_person_formatted,
        "budget_type": budget_type,
        "members": members,
        "transport_mode": transport_mode,
        "transit_label": transit_label,
        "transit_desc": transit_desc,
        "transit_icon": transit_icon,
        "budget_target": total_budget if budget_type == 'total' else per_person_budget,
        "days_count": days,
        "daily_budget": daily_budget,
        "cost_breakdown": cost_breakdown,
        "cost_breakdown_per_person": cost_breakdown_per_person,
        "cost_breakdown_total": cost_breakdown_total,
        "transit_info": transit_info,
        "budget_warning": budget_warning,
        "engine_badge": "Gemini AI & Uttarakhand Domain Engine",
        "days": generated_days,
        "query_prompt": prompt or f"{days} days {dest_name} trip for {members} in ₹{total_budget:,}"
    }


# ---------------------------------------------------------------------------
# Gemini REST API caller
# ---------------------------------------------------------------------------
def _call_gemini_rest(prompt, days, total_budget, per_person_budget, members, transport_mode, group_type, interests, start_city, destination, api_key):
    """
    Direct Gemini REST API call using requests (gemini-1.5-flash or gemini-2.0-flash).
    """
    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
        user_prompt = prompt or f"{days} days in {destination} with total budget ₹{total_budget:,} for {members} people ({group_type}) by {transport_mode} starting from {start_city}"
        
        sys_prompt = f"""You are an expert Uttarakhand tourism specialist. Create a detailed {days}-day travel itinerary for {destination}, Uttarakhand.
Context:
- User Prompt: "{user_prompt}"
- Duration: {days} days
- Group Size: {members} travelers ({group_type})
- Transport Mode: {transport_mode}
- Total Budget: ₹{total_budget:,} (approx ₹{per_person_budget:,} per person)
- Interests: {', '.join(interests or ['culture', 'nature'])}
- Starting From: {start_city}

Return ONLY valid JSON matching this exact structure:
{{
  "title": "{days}-Day {destination.title()} Itinerary",
  "summary": "2-sentence compelling overview",
  "budget_estimate": "₹{int(total_budget*0.88):,} – ₹{total_budget:,} total",
  "days": [
    {{
      "day": 1,
      "theme": "Day Theme Title",
      "stops": [
        {{"time": "Morning", "place": "Place Name", "activity": "Specific activity description", "tip": "Insider local tip"}},
        {{"time": "Afternoon", "place": "Place Name", "activity": "Specific activity description", "tip": "Insider local tip"}},
        {{"time": "Evening", "place": "Place Name", "activity": "Specific activity description", "tip": "Insider local tip"}}
      ]
    }}
  ]
}}

CRITICAL: Do NOT output ANY emojis (no cars, lights, mountains, people, etc.). Use only clean, luxury English prose. Emphasize authentic Uttarakhand experiences, local Kumaoni/Garhwali food, local homestays, and budget tips fitting total budget ₹{total_budget:,}."""

        payload = {
            "contents": [
                {
                    "parts": [{"text": sys_prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.3,
                "responseMimeType": "application/json"
            }
        }

        resp = requests.post(url, json=payload, timeout=8)
        if resp.status_code == 200:
            data = resp.json()
            text_resp = data['candidates'][0]['content']['parts'][0]['text']
            match = re.search(r'\{.*\}', text_resp, re.DOTALL)
            if match:
                parsed_json = json.loads(match.group())
                if 'days' in parsed_json and len(parsed_json['days']) > 0:
                    parsed_json['query_prompt'] = user_prompt
                    return parsed_json
    except Exception as e:
        # Fallback to local high-fidelity generator
        pass

    return None

# Centralized definition and helpers for location-based cards across
# Hotels & Homestays, Guides, and Community pages.

DISTRICT_CARDS_BASE = [
    {
        'slug': 'almora',
        'name': 'Almora',
        'tagline': 'CULTURAL HEART OF KUMAON',
        'overview': 'Perched on a 5 km horse-saddle ridge, the intellectual and artistic capital of Kumaon famed for Kasar Devi and Aipan art.',
        'image': '/static/images/Almora/almora.png',
        'region': 'Kumaon',
        'default_stay_price': 750,
        'default_guide_rate': 2200,
    },
    {
        'slug': 'nainital',
        'name': 'Nainital',
        'tagline': 'THE LAKE DISTRICT OF INDIA',
        'overview': 'Emerald pear-shaped lake surrounded by seven deodar-clad hills, vibrant boat docks, and panoramic Himalayan viewpoints.',
        'image': '/static/images/Nanital/Nanital_city.png',
        'region': 'Kumaon',
        'default_stay_price': 750,
        'default_guide_rate': 2000,
    },
    {
        'slug': 'pithoragarh',
        'name': 'Pithoragarh',
        'tagline': 'SOAR VALLEY & PANCHACHULI PEAKS',
        'overview': 'Bordering Tibet and Nepal, Kumaon\'s eastern frontier of five Panchachuli peaks, Munsiyari high meadows, and Shauka handlooms.',
        'image': '/static/images/destinations/pithoragarh_fort.jpg',
        'region': 'Kumaon',
        'default_stay_price': 750,
        'default_guide_rate': 2400,
    },
    {
        'slug': 'uttarkashi',
        'name': 'Uttarkashi',
        'tagline': 'GATEWAY TO GANGOTRI & RAWAIN VALLEY',
        'overview': 'Sacred Garhwal highlands cradling the holy Bhagirathi river, ancient timber temples in Barkot, and alpine apple orchards of Harsil.',
        'image': '/static/images/destinations/uttarkashi.jpg',
        'region': 'Garhwal',
        'default_stay_price': 700,
        'default_guide_rate': 2300,
    },
    {
        'slug': 'champawat',
        'name': 'Champawat',
        'tagline': 'ANCIENT CAPITAL OF CHAND KINGS & ABBOTT MOUNT',
        'overview': 'Historic cradle of Kumaon heritage, ancient stone temples of Baleshwar, tea gardens, and sacred Purnagiri Dham near Tanakpur.',
        'image': '/static/images/champwat/champawat.png',
        'region': 'Kumaon',
        'default_stay_price': 800,
        'default_guide_rate': 2100,
    }
]

DISTRICT_LOOKUP = {
    'almora': ['almora', 'jageshwar', 'kasar', 'kasar devi', 'chitai', 'binsar', 'ranikhet', 'katarmal'],
    'nainital': ['nainital', 'nanital', 'bhimtal', 'pangot', 'naini', 'mukteshwar', 'sattal', 'bhowali'],
    'pithoragarh': ['pithoragarh', 'pithoraghar', 'munsiyari', 'munsyari', 'panchachuli', 'soar', 'askot'],
    'uttarkashi': ['uttarkashi', 'harsil', 'barkot', 'gangotri', 'yamunotri', 'dayara bugyal', 'dayara', 'gartang gali', 'dodital'],
    'champawat': ['champawat', 'champwat', 'tanakpur', 'lohaghat', 'banbasa', 'purnagiri', 'baleshwar', 'abbott mount', 'shyamlatal']
}


def get_district_search_terms(district_input):
    """
    Returns an expanded list of search terms/aliases for a given district name or slug.
    E.g. 'Rishikesh' -> ['rishikesh', 'dehradun', 'mussoorie', ...]
    """
    if not district_input:
        return []
    cleaned = district_input.lower().replace('&', ' ').replace('-', ' ').strip()
    terms = {district_input.strip().lower()}
    for key, aliases in DISTRICT_LOOKUP.items():
        if key in cleaned or cleaned in key or any(a in cleaned or cleaned in a for a in aliases):
            terms.add(key)
            terms.update(aliases)
    return list(terms)


def get_canonical_district(district_input):
    """
    Returns canonical district slug for a given location or query term.
    """
    if not district_input:
        return None
    cleaned = district_input.lower().replace('&', ' ').replace('-', ' ').strip()
    for key, aliases in DISTRICT_LOOKUP.items():
        if key in cleaned or cleaned in key or any(a in cleaned or cleaned in a for a in aliases):
            return key
    return cleaned


def _matches_district(base, dist_text):
    if not dist_text:
        return False
    target = str(dist_text).lower().replace('&', ' ').replace('-', ' ')
    slug = base['slug'].lower()
    
    # Direct slug or name match
    if slug in target:
        return True
    parts = [p.strip().lower() for p in base['name'].split('&')]
    if any(p in target for p in parts):
        return True
        
    # Alias lookup match
    aliases = DISTRICT_LOOKUP.get(slug, [])
    return any(a in target for a in aliases)


def get_hotel_location_cards(hotels_list):
    """
    Computes location cards for Hotels & Homestays page with dynamic counts
    and minimum prices based on current listings.
    """
    cards = []
    for base in DISTRICT_CARDS_BASE:
        matching = [
            h for h in hotels_list
            if _matches_district(base, h.district)
        ]
        stays = [h for h in matching if h.hotel_type in ('homestay', 'hotel')]
        dining = [h for h in matching if h.hotel_type in ('restaurant', 'cafe')]
        stay_count = len(stays)
        dining_count = len(dining)

        prices = [h.price_min for h in stays if h.price_min]
        min_price = min(prices) if prices else base['default_stay_price']

        cards.append({
            **base,
            'stay_count': stay_count,
            'dining_count': dining_count,
            'total_count': len(matching),
            'min_price': min_price,
            'count_label': f"{stay_count} Stay{'s' if stay_count != 1 else ''}"
        })
    return cards


def get_guide_location_cards(guides_list):
    """
    Computes location cards for Guides page with dynamic guide counts
    and minimum rates.
    """
    cards = []
    for base in DISTRICT_CARDS_BASE:
        matching = [
            g for g in guides_list
            if _matches_district(base, g.district) or _matches_district(base, g.districts_served)
        ]
        guide_count = len(matching)
        rates = [g.daily_rate for g in matching if g.daily_rate]
        min_rate = min(rates) if rates else base['default_guide_rate']

        cards.append({
            **base,
            'guide_count': guide_count,
            'min_rate': min_rate,
            'count_label': f"{guide_count} Guide{'s' if guide_count != 1 else ''}"
        })
    return cards


def get_community_location_cards(posts_list):
    """
    Computes location cards for Community Stories page with dynamic post counts.
    """
    cards = []
    for base in DISTRICT_CARDS_BASE:
        matching = [
            p for p in posts_list
            if _matches_district(base, p.district_tag) or _matches_district(base, getattr(p, 'destination_tag', None))
        ]
        post_count = len(matching)

        cards.append({
            **base,
            'post_count': post_count,
            'count_label': f"{post_count} Stor{'ies' if post_count != 1 else 'y'}"
        })
    return cards

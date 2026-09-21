"""
Comprehensive script to arrange hotels and homestays strictly for the 4 core districts:
Almora, Nainital, Pithoragarh, and Uttarkashi, with starting prices between ₹700 and ₹3000.
"""
from app import create_app
from app.extensions import db
from app.models import Hotel, Destination, User

def arrange_all_hotels():
    app = create_app()
    with app.app_context():
        print("Arranging hotels and homestays strictly for Almora, Nainital, Pithoragarh, Uttarkashi...")
        
        owner = User.query.filter_by(role='business').first() or User.query.first()
        owner_id = owner.id if owner else 1

        def get_dest_id(dist_name):
            d = Destination.query.filter(Destination.district.ilike(f'%{dist_name}%')).first()
            return d.id if d else None

        # Portfolio of authentic Hotels and Homestays strictly for the 4 districts
        curated_hotels = [
            # ================= NAINITAL =================
            {
                'name': 'The Naini Retreat',
                'hotel_type': 'hotel',
                'district': 'Nainital',
                'destination_id': get_dest_id('nainital'),
                'price_min': 1950,
                'price_max': 2950,
                'rating': 4.9,
                'review_count': 128,
                'host_name': 'Vikramaditya Shah',
                'host_story': 'A converted royal residence perched on Ayarpatta Slopes, offering sweeping views of Naini Lake and centuries-old colonial hospitality.',
                'cover_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80',
                'amenities': '["wifi", "parking", "mountain-view", "lake-view", "restaurant"]',
                'lat': 29.3889, 'lng': 79.4480,
                'featured': True
            },
            {
                'name': 'Ridge Pines Hotel',
                'hotel_type': 'hotel',
                'district': 'Nainital',
                'destination_id': get_dest_id('nainital'),
                'price_min': 1400,
                'price_max': 2600,
                'rating': 4.7,
                'review_count': 84,
                'host_name': 'Sunil Mehra',
                'host_story': 'Mid-range hotel with mountain-facing rooms, panoramic views of the high peaks, and a sunset bonfire deck overlooking the pine valley.',
                'cover_image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80',
                'amenities': '["wifi", "parking", "mountain-view", "bonfire", "restaurant"]',
                'lat': 29.3980, 'lng': 79.4600,
                'featured': True
            },
            {
                'name': 'Ayarpata Pine View Homestay',
                'hotel_type': 'homestay',
                'district': 'Nainital',
                'destination_id': get_dest_id('nainital'),
                'price_min': 750,
                'price_max': 1400,
                'rating': 4.8,
                'review_count': 49,
                'host_name': 'Hemant Joshi',
                'host_story': 'Cozy traditional wooden homestay on the serene upper Ayarpatta hills away from traffic. Fresh home-cooked Kumaoni meals and guided forest walks.',
                'cover_image_url': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&q=80',
                'amenities': '["mountain-view", "meals-included", "bonfire", "wifi"]',
                'lat': 29.3840, 'lng': 79.4450,
                'featured': True
            },
            {
                'name': 'Pangot Oak Forest Eco Stay',
                'hotel_type': 'homestay',
                'district': 'Nainital',
                'destination_id': get_dest_id('nainital'),
                'price_min': 900,
                'price_max': 1700,
                'rating': 4.9,
                'review_count': 62,
                'host_name': 'Tara Dutt Pant',
                'host_story': 'Renowned birding homestay nestled deep inside the dense oak and rhododendron sanctuary of Pangot (15km from Nainital). Organic farm meals.',
                'cover_image_url': 'https://images.unsplash.com/photo-1604537529428-15bcbeecfe4d?w=800&q=80',
                'amenities': '["birding-tours", "mountain-view", "meals-included", "bonfire"]',
                'lat': 29.4300, 'lng': 79.4300,
                'featured': True
            },

            # ================= ALMORA =================
            {
                'name': 'Almora Heritage Homestay',
                'hotel_type': 'homestay',
                'district': 'Almora',
                'destination_id': get_dest_id('almora'),
                'price_min': 950,
                'price_max': 1800,
                'rating': 4.9,
                'review_count': 61,
                'host_name': 'Gopal Bhandari',
                'host_story': 'Restored traditional Kumaoni stone house with carved wooden balconies and terrace views of the Kasar Devi hills. Mother draws daily ritual Aipan art.',
                'cover_image_url': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&q=80',
                'amenities': '["wifi", "mountain-view", "meals-included", "bonfire"]',
                'lat': 29.5969, 'lng': 79.6538,
                'featured': True
            },
            {
                'name': 'Bright End Corner Stay',
                'hotel_type': 'hotel',
                'district': 'Almora',
                'destination_id': get_dest_id('almora'),
                'price_min': 1300,
                'price_max': 2200,
                'rating': 4.6,
                'review_count': 39,
                'host_name': 'Deepak Joshi',
                'host_story': 'Budget guesthouse located near the Kasar Devi temple trail. Peaceful garden courtyard popular among artists, readers, and trek enthusiasts.',
                'cover_image_url': 'https://images.unsplash.com/photo-1611892440504-42a792e24d32?w=800&q=80',
                'amenities': '["wifi", "mountain-view", "parking"]',
                'lat': 29.6050, 'lng': 79.6600,
                'featured': False
            },
            {
                'name': 'Kasar Devi Pine Cottage',
                'hotel_type': 'homestay',
                'district': 'Almora',
                'destination_id': get_dest_id('almora'),
                'price_min': 750,
                'price_max': 1500,
                'rating': 4.9,
                'review_count': 53,
                'host_name': 'Mohan Chandra',
                'host_story': 'Rustic stone cottage right on Crank\'s Ridge with unobstructed 180-degree Himalayan sunrise views. Meditative calm and organic Pahadi cuisine.',
                'cover_image_url': 'https://images.unsplash.com/photo-1604537529428-15bcbeecfe4d?w=800&q=80',
                'amenities': '["mountain-view", "meditation-deck", "meals-included", "wifi"]',
                'lat': 29.6380, 'lng': 79.6740,
                'featured': True
            },
            {
                'name': 'Jageshwar Sacred Deodar Lodge',
                'hotel_type': 'hotel',
                'district': 'Almora',
                'destination_id': get_dest_id('almora'),
                'price_min': 1650,
                'price_max': 2750,
                'rating': 4.8,
                'review_count': 71,
                'host_name': 'Devendra Bhatt',
                'host_story': 'Cedar-built sanctuary located 500 meters from the 8th-century Jageshwar Dham temple cluster. Peaceful stream sound and meditation deck.',
                'cover_image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80',
                'amenities': '["wifi", "mountain-view", "vegetarian-restaurant", "bonfire", "parking"]',
                'lat': 29.6420, 'lng': 79.8520,
                'featured': True
            },

            # ================= PITHORAGARH =================
            {
                'name': 'Hill Fort Homestay',
                'hotel_type': 'homestay',
                'district': 'Pithoragarh',
                'destination_id': get_dest_id('pithoragarh'),
                'price_min': 1100,
                'price_max': 1950,
                'rating': 4.8,
                'review_count': 29,
                'host_name': 'Captain B.S. Chand',
                'host_story': 'Colonial-era heritage residence turned homestay, perched on a pine knoll with open vistas of the lush Soar valley.',
                'cover_image_url': '/static/images/destinations/pithoragarh_fort.jpg',
                'amenities': '["wifi", "mountain-view", "meals-included", "bonfire"]',
                'lat': 29.5828, 'lng': 80.2182,
                'featured': True
            },
            {
                'name': 'Munsyari Base Camp Lodge',
                'hotel_type': 'hotel',
                'district': 'Pithoragarh',
                'destination_id': get_dest_id('pithoragarh'),
                'price_min': 1550,
                'price_max': 2650,
                'rating': 4.9,
                'review_count': 44,
                'host_name': 'Dhan Singh Martolia',
                'host_story': 'Trekker-focused lodge equipped with secure gear storage, drying rooms, and certified local mountain guide tie-ups for high-altitude passes.',
                'cover_image_url': '/static/images/destinations/munsiyari.jpg',
                'amenities': '["wifi", "mountain-view", "parking"]',
                'lat': 30.0668, 'lng': 80.2369,
                'featured': True
            },
            {
                'name': 'Soar Valley Orchard Homestay',
                'hotel_type': 'homestay',
                'district': 'Pithoragarh',
                'destination_id': get_dest_id('pithoragarh'),
                'price_min': 800,
                'price_max': 1500,
                'rating': 4.8,
                'review_count': 33,
                'host_name': 'Birendra Singh Rawat',
                'host_story': 'Charming orchard stay set among pear and plum trees in the fertile Soar Valley. Warm Kumaoni hospitality and views of Chandak hills.',
                'cover_image_url': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=800&q=80',
                'amenities': '["farm-stay", "meals-included", "mountain-view", "bonfire"]',
                'lat': 29.5850, 'lng': 80.2100,
                'featured': True
            },
            {
                'name': 'Panchachuli Glaciers View Inn',
                'hotel_type': 'hotel',
                'district': 'Pithoragarh',
                'destination_id': get_dest_id('pithoragarh'),
                'price_min': 1350,
                'price_max': 2400,
                'rating': 4.9,
                'review_count': 51,
                'host_name': 'Kamal Martolia',
                'host_story': 'Front-row balcony view facing the five sacred peaks of Panchachuli. Authentic Bhotia thali and trekking base camp logistics.',
                'cover_image_url': '/static/images/destinations/munsiyari.jpg',
                'amenities': '["glacier-view", "wifi", "restaurant", "trek-guides"]',
                'lat': 30.0680, 'lng': 80.2400,
                'featured': True
            },

            # ================= UTTARKASHI =================
            {
                'name': 'Bhagirathi Eco Homestay',
                'hotel_type': 'homestay',
                'district': 'Uttarkashi',
                'destination_id': get_dest_id('uttarkashi'),
                'price_min': 750,
                'price_max': 1400,
                'rating': 4.8,
                'review_count': 38,
                'host_name': 'Rajeshwar Rana',
                'host_story': 'Riverside homestay on the banks of holy Bhagirathi. Fresh mountain trout and organic Garhwali thali, surrounded by apple orchards.',
                'cover_image_url': '/static/images/destinations/uttarkashi.jpg',
                'amenities': '["river-view", "organic-food", "bonfire", "parking"]',
                'lat': 30.7300, 'lng': 78.4400,
                'featured': True
            },
            {
                'name': 'Gangotri Heights Lodge',
                'hotel_type': 'hotel',
                'district': 'Uttarkashi',
                'destination_id': get_dest_id('uttarkashi'),
                'price_min': 1350,
                'price_max': 2350,
                'rating': 4.7,
                'review_count': 45,
                'host_name': 'Surendra Rawat',
                'host_story': 'Well-equipped lodge serving pilgrims and mountaineers heading to Gangotri Dham and Gaumukh glacier. Clean warm rooms and 24h hot water.',
                'cover_image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?w=800&q=80',
                'amenities': '["wifi", "parking", "restaurant", "hot-water"]',
                'lat': 30.7350, 'lng': 78.4500,
                'featured': True
            },
            {
                'name': 'Harsil Apple Valley Retreat',
                'hotel_type': 'homestay',
                'district': 'Uttarkashi',
                'destination_id': get_dest_id('uttarkashi'),
                'price_min': 1200,
                'price_max': 2100,
                'rating': 4.9,
                'review_count': 54,
                'host_name': 'Pradeep Negi',
                'host_story': 'Wooden cottage inside Wilson\'s historic apple orchards in Harsil Valley. Whispering deodars, bubbling mountain streams, and fresh apple cider.',
                'cover_image_url': 'https://images.unsplash.com/photo-1604537529428-15bcbeecfe4d?w=800&q=80',
                'amenities': '["apple-orchard", "river-view", "meals-included", "bonfire"]',
                'lat': 31.0370, 'lng': 78.7380,
                'featured': True
            },
            {
                'name': 'Dayara Bugyal Mountain Camp',
                'hotel_type': 'hotel',
                'district': 'Uttarkashi',
                'destination_id': get_dest_id('uttarkashi'),
                'price_min': 950,
                'price_max': 1800,
                'rating': 4.8,
                'review_count': 41,
                'host_name': 'Gajendra Bisht',
                'host_story': 'Base meadow camp for the Dayara Bugyal high-altitude trek. Cozy alpine tents with beds, dining tent, and local mountain guiding.',
                'cover_image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80',
                'amenities': '["mountain-view", "bonfire", "meals-included", "trekking"]',
                'lat': 30.8400, 'lng': 78.5200,
                'featured': True
            }
        ]

        # First, remove hotels not belonging to the 4 districts
        allowed_districts = {'Nainital', 'Almora', 'Pithoragarh', 'Uttarkashi'}
        removed_count = Hotel.query.filter(~Hotel.district.in_(allowed_districts)).delete(synchronize_session=False)
        if removed_count:
            print(f"Purged {removed_count} hotels from other districts.")

        # Insert or update each listing in the 4 districts
        for item in curated_hotels:
            existing = Hotel.query.filter_by(name=item['name']).first()
            if not existing:
                h = Hotel(
                    owner_id=owner_id,
                    name=item['name'],
                    hotel_type=item['hotel_type'],
                    district=item['district'],
                    destination_id=item['destination_id'],
                    price_min=item['price_min'],
                    price_max=item['price_max'],
                    rating=item['rating'],
                    review_count=item['review_count'],
                    host_name=item['host_name'],
                    host_story=item['host_story'],
                    cover_image_url=item['cover_image_url'],
                    amenities=item['amenities'],
                    lat=item['lat'],
                    lng=item['lng'],
                    featured=item['featured']
                )
                db.session.add(h)
            else:
                existing.price_min = item['price_min']
                existing.price_max = item['price_max']
                existing.district = item['district']
                existing.cover_image_url = item['cover_image_url']
                existing.host_name = item['host_name']
                existing.host_story = item['host_story']

        db.session.commit()
        print("Finished seeding 16 authentic hotels strictly across Almora, Nainital, Pithoragarh, Uttarkashi.")

if __name__ == '__main__':
    arrange_all_hotels()

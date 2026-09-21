"""
Safely syncs database with stays, dining spots, guides, and community posts
for Almora, Champawat, Nainital, Uttarkashi, and Pithoragarh.
"""
from app import create_app
from app.extensions import db
from app.models import Destination, Hotel, Guide, CommunityPost, User

def sync_data():
    app = create_app()
    with app.app_context():
        # Get users for relationships
        admin = User.query.filter_by(role='admin').first() or User.query.first()
        host = User.query.filter_by(role='business').first() or admin
        traveler = User.query.filter_by(role='tourist').first() or admin

        # Ensure Uttarkashi destination exists
        uttarkashi = Destination.query.filter_by(slug='uttarkashi').first()
        if not uttarkashi:
            uttarkashi = Destination(
                name='Uttarkashi',
                slug='uttarkashi',
                region='garhwal',
                category='temple',
                district='Uttarkashi',
                lat=30.7268,
                lng=78.4354,
                altitude_m=1158,
                description='Gateway to the Gangotri glacier and Yamunotri shrines, nestled along the sacred Bhagirathi River with ancient temples and vibrant mountain culture.',
                cover_image_url='https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80',
                best_time='March–June, September–November',
                featured=True
            )
            db.session.add(uttarkashi)
            db.session.flush()
            print("Added Uttarkashi destination.")

        nainital_dest = Destination.query.filter_by(slug='nainital').first()
        almora_dest = Destination.query.filter_by(slug='almora').first()
        champawat_dest = Destination.query.filter_by(slug='baleshwar-temple').first()
        pithoragarh_dest = Destination.query.filter_by(slug='pithoragarh-fort').first()

        # Target hotels, homestays, and restaurants
        items_to_add = [
            # Nainital
            {
                'name': 'Ayarpata Pine View Homestay',
                'hotel_type': 'homestay',
                'district': 'Nainital',
                'dest_id': nainital_dest.id if nainital_dest else None,
                'price_min': 1200,
                'price_max': 2400,
                'amenities': '["wifi", "mountain-view", "lake-view", "bonfire", "home-cooked-meals"]',
                'cover_image_url': 'https://images.unsplash.com/photo-1587474260584-136574528ed5?w=800&q=80',
                'host_name': 'Meera Negi',
                'host_story': 'Rustic wooden cottage high on Ayarpatta slope offering morning lake mist views and traditional pahadi breakfast.',
                'rating': 4.9,
                'review_count': 52,
                'featured': True,
                'lat': 29.3850,
                'lng': 79.4490
            },
            {
                'name': 'Sakley’s Mountain Cafe & Bakery',
                'hotel_type': 'restaurant',
                'district': 'Nainital',
                'dest_id': nainital_dest.id if nainital_dest else None,
                'price_min': 350,
                'price_max': 800,
                'amenities': '["lake-view", "pahadi-herbal-tea", "bakery", "outdoor-seating", "wood-fired-pizza"]',
                'cover_image_url': 'https://images.unsplash.com/photo-1554118811-1e0d58224f24?w=800&q=80',
                'host_name': 'Chef Rajesh Sakley',
                'host_story': 'A mountain bakery institution since 1944, serving apple tarts, roasted coffee, and comforting local soups beside oak woods.',
                'rating': 4.8,
                'review_count': 114,
                'featured': True,
                'lat': 29.3900,
                'lng': 79.4520
            },

            # Almora
            {
                'name': 'Kasar Devi Pine Cottage',
                'hotel_type': 'homestay',
                'district': 'Almora',
                'dest_id': almora_dest.id if almora_dest else None,
                'price_min': 900,
                'price_max': 1600,
                'amenities': '["wifi", "mountain-view", "organic-farm", "bonfire"]',
                'cover_image_url': '/static/images/Almora/kashardevi.png',
                'host_name': 'Harish Rawat',
                'host_story': 'Cozy stone sanctuary right along Crank’s Ridge with sweeping panoramic vistas of Trishul and Nanda Devi.',
                'rating': 4.9,
                'review_count': 41,
                'featured': True,
                'lat': 29.6100,
                'lng': 79.6700
            },
            {
                'name': 'Sarthi Traditional Kumaoni Dining',
                'hotel_type': 'restaurant',
                'district': 'Almora',
                'dest_id': almora_dest.id if almora_dest else None,
                'price_min': 200,
                'price_max': 550,
                'amenities': '["kumaoni-thali", "bal-mithai", "singodi", "wood-fired-roti", "jhangora-kheer"]',
                'cover_image_url': 'https://images.unsplash.com/photo-1546069901-ba9599a7e63c?w=800&q=80',
                'host_name': 'Kewal Ram Sarthi',
                'host_story': 'Historic family-run kitchen serving the finest Bhatti ki Churkani, Gahat dal, and authentic Bal Mithai in Lala Bazaar.',
                'rating': 4.9,
                'review_count': 89,
                'featured': True,
                'lat': 29.5980,
                'lng': 79.6540
            },

            # Champawat
            {
                'name': 'Abbott Mount Pine Homestay',
                'hotel_type': 'homestay',
                'district': 'Champawat',
                'dest_id': champawat_dest.id if champawat_dest else None,
                'price_min': 700,
                'price_max': 1400,
                'amenities': '["wifi", "mountain-view", "organic-tea", "nature-walks"]',
                'cover_image_url': '/static/images/destinations/abbott_mount.jpg',
                'host_name': 'Trilok Chand',
                'host_story': 'Serene homestay perched along the historic deodar ridge looking out towards the high Kali valley peaks.',
                'rating': 4.8,
                'review_count': 32,
                'featured': True,
                'lat': 29.4180,
                'lng': 80.1200
            },
            {
                'name': 'Chand Heritage Tea Room & Kitchen',
                'hotel_type': 'restaurant',
                'district': 'Champawat',
                'dest_id': champawat_dest.id if champawat_dest else None,
                'price_min': 180,
                'price_max': 450,
                'amenities': '["organic-tea", "pahadi-thali", "bhang-chutney", "terrace-dining"]',
                'cover_image_url': 'https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?w=800&q=80',
                'host_name': 'Kamla Devi',
                'host_story': 'Serving fragrant green tea harvested from Champawat hills alongside smoking madua rotis and spicy hemp-seed chutney.',
                'rating': 4.7,
                'review_count': 28,
                'featured': False,
                'lat': 29.3380,
                'lng': 80.0980
            },

            # Uttarkashi
            {
                'name': 'Bhagirathi Eco Homestay',
                'hotel_type': 'homestay',
                'district': 'Uttarkashi',
                'dest_id': uttarkashi.id if uttarkashi else None,
                'price_min': 800,
                'price_max': 1500,
                'amenities': '["river-view", "organic-food", "hot-water", "bonfire", "temple-trail"]',
                'cover_image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80',
                'host_name': 'Devendra Rawat',
                'host_story': 'Riverfront stone cottage with gentle sounds of the holy Bhagirathi and home-cooked red rice thalis.',
                'rating': 4.9,
                'review_count': 38,
                'featured': True,
                'lat': 30.7280,
                'lng': 78.4360
            },
            {
                'name': 'Gangotri Heights Lodge',
                'hotel_type': 'hotel',
                'district': 'Uttarkashi',
                'dest_id': uttarkashi.id if uttarkashi else None,
                'price_min': 1600,
                'price_max': 2800,
                'amenities': '["wifi", "mountain-view", "parking", "restaurant"]',
                'cover_image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=800&q=80',
                'host_name': 'Sanjay Panwar',
                'host_story': 'Reliable mountain hotel catering to pilgrims and mountaineering expeditions setting out for Gangotri and Gaumukh.',
                'rating': 4.7,
                'review_count': 45,
                'featured': True,
                'lat': 30.7310,
                'lng': 78.4410
            },
            {
                'name': 'Rawain Valley Pahadi Kitchen',
                'hotel_type': 'restaurant',
                'district': 'Uttarkashi',
                'dest_id': uttarkashi.id if uttarkashi else None,
                'price_min': 150,
                'price_max': 380,
                'amenities': '["red-rice-thali", "chainsoo", "jakhya-gutke", "river-view"]',
                'cover_image_url': 'https://images.unsplash.com/photo-1585937421612-70a008356fbe?w=800&q=80',
                'host_name': 'Pushpa Devi',
                'host_story': 'Authentic Garhwali dhaba known for hot Chainsoo dal, fresh red rice, and crunchy jakhiya-tempered potatoes.',
                'rating': 4.8,
                'review_count': 63,
                'featured': False,
                'lat': 30.7290,
                'lng': 78.4380
            },

            # Pithoragarh
            {
                'name': 'Soar Valley Orchard Homestay',
                'hotel_type': 'homestay',
                'district': 'Pithoragarh',
                'dest_id': pithoragarh_dest.id if pithoragarh_dest else None,
                'price_min': 850,
                'price_max': 1600,
                'amenities': '["wifi", "mountain-view", "orchard-walk", "bonfire"]',
                'cover_image_url': 'https://images.unsplash.com/photo-1580289248525-f9413c1d9b7c?w=800&q=80',
                'host_name': 'Birendra Joshi',
                'host_story': 'Apple and apricot orchard stay with uninterrupted sunrise views over the five peaks of Panchachuli.',
                'rating': 4.8,
                'review_count': 26,
                'featured': False,
                'lat': 29.5850,
                'lng': 80.2200
            },
            {
                'name': 'Milan Dhaba & Bhotia Kitchen',
                'hotel_type': 'restaurant',
                'district': 'Pithoragarh',
                'dest_id': pithoragarh_dest.id if pithoragarh_dest else None,
                'price_min': 180,
                'price_max': 420,
                'amenities': '["bhotia-momos", "thukpa", "gahat-soup", "mountain-view"]',
                'cover_image_url': 'https://images.unsplash.com/photo-1546549032-9571cd6b27df?w=800&q=80',
                'host_name': 'Sonam Bhotia',
                'host_story': 'Cozy mountain diner specializing in steamed Himalayan dumplings, Tibetan thukpa, and hot herb-infused broths.',
                'rating': 4.8,
                'review_count': 72,
                'featured': False,
                'lat': 29.5840,
                'lng': 80.2190
            }
        ]

        # Insert missing hotels/restaurants
        for item in items_to_add:
            existing = Hotel.query.filter_by(name=item['name']).first()
            if not existing:
                hotel = Hotel(
                    owner_id=host.id,
                    name=item['name'],
                    hotel_type=item['hotel_type'],
                    district=item['district'],
                    destination_id=item['dest_id'],
                    price_min=item['price_min'],
                    price_max=item['price_max'],
                    amenities=item['amenities'],
                    cover_image_url=item['cover_image_url'],
                    host_name=item['host_name'],
                    host_story=item['host_story'],
                    rating=item['rating'],
                    review_count=item['review_count'],
                    featured=item['featured'],
                    lat=item['lat'],
                    lng=item['lng']
                )
                db.session.add(hotel)
                print(f"Added Hotel/Restaurant: {item['name']} ({item['district']})")

        # Target Guides - only the 4 provided guide profiles exist in seed_data.py
        guides_to_add = []

        # Target Community Posts
        posts_to_add = [
            {
                'district_tag': 'Uttarkashi',
                'content': 'Evening bells echoing over the Bhagirathi river during the twilight Ganga Aarti in Uttarkashi. Pure tranquility after a trek from Gaumukh.',
                'media_type': 'photo',
                'aspect_ratio': '4:5',
                'images': '["https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1080&q=85"]',
                'likes_count': 168
            },
            {
                'district_tag': 'Champawat',
                'content': 'Discovered intricate 10th-century stone carvings at the Baleshwar Temple compound in Champawat. The craftsmanship is mesmerizing.',
                'media_type': 'photo',
                'aspect_ratio': '4:5',
                'images': '["/static/images/champwat/Baleshwar_Temple.png"]',
                'likes_count': 134
            }
        ]

        for p in posts_to_add:
            existing = CommunityPost.query.filter(
                (CommunityPost.district_tag == p['district_tag']) &
                (CommunityPost.content.like(p['content'][:30] + '%'))
            ).first()
            if not existing:
                post = CommunityPost(
                    user_id=traveler.id,
                    content=p['content'],
                    media_type=p['media_type'],
                    aspect_ratio=p['aspect_ratio'],
                    images=p['images'],
                    district_tag=p['district_tag'],
                    likes_count=p['likes_count']
                )
                db.session.add(post)
                print(f"Added Community Post: {p['district_tag']}")

        db.session.commit()
        print("Database sync completed successfully!")

if __name__ == '__main__':
    sync_data()

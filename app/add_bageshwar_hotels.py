"""
Adds authentic homestays and hotels for Bageshwar in beyond_tour.db
"""
from app import create_app
from app.extensions import db
from app.models import Hotel, Destination, User

def add_bageshwar_hotels():
    app = create_app()
    with app.app_context():
        # Check if already added
        existing = Hotel.query.filter_by(district='Bageshwar').first()
        if existing:
            print("Bageshwar hotels already exist.")
            return

        dest = Destination.query.filter(Destination.district.ilike('%bageshwar%')).first()
        dest_id = dest.id if dest else None

        owner = User.query.filter_by(role='business').first()
        owner_id = owner.id if owner else None

        h1 = Hotel(
            name='Bageshwar Saryu Riverside Homestay',
            hotel_type='homestay',
            destination_id=dest_id,
            district='Bageshwar',
            price_min=950,
            price_max=1600,
            rating=4.9,
            review_count=34,
            host_name='Trilok Singh Pande',
            host_story='Overlooking the sacred Saryu riverbank in Bageshwar, our family homestay welcomes pilgrims and cultural travelers to experience traditional Kumaoni hospitality, woodfire cooking, and local folklore.',
            cover_image_url='/static/images/festivals/uttarayani_fair.jpg',
            featured=True,
            owner_id=owner_id
        )

        h2 = Hotel(
            name='Kausani Himalayan Orchard Lodge',
            hotel_type='hotel',
            destination_id=dest_id,
            district='Bageshwar',
            price_min=1600,
            price_max=2800,
            rating=4.8,
            review_count=48,
            host_name='Deepak Rawat',
            host_story='Set amidst terraced apple and peach orchards in Kausani (Bageshwar), offering 180-degree unobstructed panoramas of Trishul, Nanda Devi, and Panchachuli peaks.',
            cover_image_url='https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80',
            featured=True,
            owner_id=owner_id
        )

        db.session.add_all([h1, h2])
        db.session.commit()
        print("Added Bageshwar hotels successfully!")

if __name__ == '__main__':
    add_bageshwar_hotels()

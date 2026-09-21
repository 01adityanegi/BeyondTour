"""
Synchronizes the 7 Upcoming Festivals of Kumaon into the database CultureEntry table.
"""
from app import create_app
from app.extensions import db
from app.models import CultureEntry
from app.blueprints.culture.kumaon_festivals import KUMAON_UPCOMING_FESTIVALS

def sync(app=None):
    if app is None:
        app = create_app()
        with app.app_context():
            _do_sync()
    else:
        _do_sync()

def _do_sync():
    for fest in KUMAON_UPCOMING_FESTIVALS:
        entry = CultureEntry.query.filter_by(slug=fest['slug']).first()
        if not entry:
            # Also check by title if slug differs
            entry = CultureEntry.query.filter(CultureEntry.title.ilike(fest['title'])).first()

        if entry:
            entry.slug = fest['slug']
            entry.title = fest['title']
            entry.subtitle = fest['important_date']
            entry.district = fest['location']
            entry.venue = fest['location']
            entry.region = 'kumaon'
            entry.entry_type = 'festival'
            entry.when_celebrated = f"{fest['date']} ({fest['important_date']})"
            entry.month_name = fest['month_name']
            entry.month_number = fest['month_number']
            entry.cover_image_url = fest['image']
            entry.story_text = fest['full_story']
            entry.travel_tips = fest['travel_info']
            entry.deity_or_ritual = ', '.join(fest['what_to_experience'])
            entry.attendance = 'Traditional Kumaon Valley Community Celebration'
            entry.is_happening_soon = (fest['season_filter'] == 'september')
            print(f"Updated existing festival: {fest['title']}")
        else:
            new_entry = CultureEntry(
                slug=fest['slug'],
                title=fest['title'],
                subtitle=fest['important_date'],
                district=fest['location'],
                venue=fest['location'],
                region='kumaon',
                entry_type='festival',
                category='Cultural',
                when_celebrated=f"{fest['date']} ({fest['important_date']})",
                month_name=fest['month_name'],
                month_number=fest['month_number'],
                cover_image_url=fest['image'],
                story_text=fest['full_story'],
                travel_tips=fest['travel_info'],
                deity_or_ritual=', '.join(fest['what_to_experience']),
                attendance='Traditional Kumaon Valley Community Celebration',
                is_happening_soon=(fest['season_filter'] == 'september')
            )
            db.session.add(new_entry)
            print(f"Created new festival: {fest['title']}")

    db.session.commit()
    print("Kumaon festivals sync complete!")

if __name__ == '__main__':
    sync()

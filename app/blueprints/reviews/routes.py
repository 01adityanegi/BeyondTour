from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app.blueprints.reviews import bp
from app.extensions import db
from app.models import Review

@bp.route('/write', methods=['GET', 'POST'])
@login_required
def write():
    target_type = request.args.get('target_type', 'destination')
    target_id = request.args.get('target_id', type=int)
    if request.method == 'POST':
        review = Review(
            user_id=current_user.id,
            target_type=request.form.get('target_type'),
            target_id=int(request.form.get('target_id', 0)),
            rating=int(request.form.get('rating', 5)),
            comment=request.form.get('comment', '').strip()
        )
        db.session.add(review)
        db.session.commit()
        flash('Thank you! Your review has been published.', 'success')
        target_t = request.form.get('target_type')
        target_i = int(request.form.get('target_id', 0))
        if target_t == 'hotel' and target_i:
            return redirect(url_for('hotels.detail', hotel_id=target_i))
        elif target_t == 'destination' and target_i:
            return redirect(url_for('destinations.detail', dest_id=target_i))
        elif target_t == 'guide' and target_i:
            return redirect(url_for('guides.detail', guide_id=target_i))
        return redirect(url_for('main.index'))
    return render_template('reviews/write.html', target_type=target_type, target_id=target_id)

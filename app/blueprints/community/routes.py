import json
import re
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.blueprints.community import bp
from app.extensions import db
from app.models import CommunityPost, User, Comment, PostLike

IG_REGEX = re.compile(r'(?:https?:\/\/)?(?:www\.)?instagram\.com\/(?:p|reel|reels|tv)\/([A-Za-z0-9_-]+)', re.IGNORECASE)
YT_SHORTS_REGEX = re.compile(r'(?:https?:\/\/)?(?:www\.|m\.)?youtube\.com\/shorts\/([A-Za-z0-9_-]+)', re.IGNORECASE)
YT_VIDEO_REGEX = re.compile(r'(?:https?:\/\/)?(?:www\.|m\.)?(?:youtube\.com\/(?:watch\?(?:.*&)?v=|embed\/|v\/|live\/)|youtu\.be\/)([A-Za-z0-9_-]+)', re.IGNORECASE)

ALLOWED_IMG_EXTS = {'jpg', 'jpeg', 'png', 'webp', 'avif', 'gif'}
ALLOWED_VID_EXTS = {'mp4', 'webm', 'mov', 'm4v'}

from app.district_cards import get_community_location_cards

@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    district_filter = request.args.get('district', '').strip().lower()
    format_filter = request.args.get('format', 'all').strip().lower()

    canonical_map = {
        'chamoli': 'uttarkashi',
        'rudraprayag': 'uttarkashi',
        'haridwar': 'uttarkashi',
        'dehradun': 'uttarkashi',
        'tehri': 'uttarkashi',
        'tehri garhwal': 'uttarkashi',
        'bageshwar': 'almora',
        'champawat': 'pithoragarh',
    }
    if district_filter in canonical_map:
        district_filter = canonical_map[district_filter]

    query = CommunityPost.query.filter_by(is_hidden=False)
    if district_filter and district_filter != 'all':
        query = query.filter(
            (CommunityPost.district_tag.ilike(f'%{district_filter}%')) |
            (CommunityPost.destination_tag.ilike(f'%{district_filter}%'))
        )
    
    if format_filter == 'videos':
        query = query.filter(CommunityPost.media_type.in_(['youtube', 'video']))
    elif format_filter == 'shorts':
        query = query.filter(CommunityPost.media_type == 'youtube_shorts')
    elif format_filter == 'photos':
        query = query.filter(CommunityPost.media_type == 'photo')
    elif format_filter == 'reels':
        query = query.filter(CommunityPost.media_type.in_(['instagram', 'youtube_shorts']))

    posts = query.order_by(CommunityPost.created_at.desc()).paginate(page=page, per_page=16, error_out=False)

    user_liked_post_ids = set()
    if current_user.is_authenticated:
        user_liked_post_ids = {l.post_id for l in PostLike.query.filter_by(user_id=current_user.id).all()}
    
    if request.headers.get('HX-Request'):
        return render_template(
            'community/_posts.html',
            posts=posts,
            active_district=district_filter,
            active_format=format_filter,
            user_liked_post_ids=user_liked_post_ids
        )

    all_posts = CommunityPost.query.filter_by(is_hidden=False).all()
    location_cards = get_community_location_cards(all_posts)
    total_stories = len(all_posts)

    return render_template(
        'community/index.html',
        posts=posts,
        location_cards=location_cards,
        active_district=district_filter or 'all',
        active_format=format_filter,
        total_stories=total_stories,
        user_liked_post_ids=user_liked_post_ids,
        title='Community Stories & Videos — Beyond Tour'
    )


@bp.route('/<int:post_id>')
def post_detail(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    user_liked = False
    if current_user.is_authenticated:
        user_liked = PostLike.query.filter_by(user_id=current_user.id, post_id=post.id).first() is not None
    return render_template('community/_modal_detail.html', post=post, user_liked=user_liked)


@bp.route('/upload-media', methods=['POST'])
@login_required
def upload_media():
    if not current_user.email_verified:
        current_user.email_verified = True
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'community')
    os.makedirs(upload_folder, exist_ok=True)
    timestamp = int(datetime.utcnow().timestamp())

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in request'}), 400

    f = request.files['file']
    if not f or not f.filename:
        return jsonify({'error': 'No selected file'}), 400

    orig_fn = secure_filename(f.filename)
    ext = orig_fn.rsplit('.', 1)[-1].lower() if '.' in orig_fn else ''

    if ext in ALLOWED_IMG_EXTS:
        media_kind = 'image'
        safe_fn = f"comm_img_{current_user.id}_{timestamp}_{orig_fn}"
    elif ext in ALLOWED_VID_EXTS:
        media_kind = 'video'
        safe_fn = f"comm_vid_{current_user.id}_{timestamp}_{orig_fn}"
    else:
        return jsonify({'error': f"Unsupported format (.{ext}). Allowed: JPG, PNG, WEBP, MP4, WEBM, MOV"}), 400

    dest = os.path.join(upload_folder, safe_fn)
    f.save(dest)
    public_url = f"/static/uploads/community/{safe_fn}"

    return jsonify({
        'status': 'success',
        'url': public_url,
        'media_type': media_kind,
        'filename': safe_fn
    })


@bp.route('/post', methods=['POST'])
@login_required
def create_post():
    raw_district = request.form.get('district_tag', '').strip() or request.form.get('destination_tag', 'Almora')
    canonical_map = {
        'chamoli': 'Uttarkashi',
        'rudraprayag': 'Uttarkashi',
        'haridwar': 'Uttarkashi',
        'dehradun': 'Uttarkashi',
        'tehri': 'Uttarkashi',
        'bageshwar': 'Almora',
        'champawat': 'Pithoragarh',
        'almora': 'Almora',
        'nainital': 'Nainital',
        'pithoragarh': 'Pithoragarh',
        'uttarkashi': 'Uttarkashi',
    }
    district_tag = canonical_map.get(raw_district.lower(), raw_district or 'Almora')
    media_type = request.form.get('media_type', 'photo').lower().strip()
    aspect_ratio = request.form.get('aspect_ratio', '4:5').strip()
    video_format = request.form.get('video_format', '16:9').strip()

    # Retrieve content from form
    content = request.form.get('content', '').strip() or request.form.get('caption', '').strip()
    if not content:
        content = f"Breathtaking mountain experience in {district_tag}, Uttarakhand."

    # Auto-verify email for convenience
    if not current_user.email_verified:
        current_user.email_verified = True
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    media_url = None
    instagram_shortcode = None
    youtube_id = None
    images_list = []

    upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'community')
    os.makedirs(upload_folder, exist_ok=True)
    timestamp = int(datetime.utcnow().timestamp())

    # 1. Process direct photo file uploads (drag-and-drop or file input)
    photo_files = request.files.getlist('photo_files')
    if not photo_files or (len(photo_files) == 1 and not photo_files[0].filename):
        if 'photo_file' in request.files and request.files['photo_file'].filename:
            photo_files = [request.files['photo_file']]
        else:
            photo_files = []

    for pf in photo_files:
        if pf and pf.filename:
            orig_pfn = secure_filename(pf.filename)
            pext = orig_pfn.rsplit('.', 1)[-1].lower() if '.' in orig_pfn else ''
            if pext in ALLOWED_IMG_EXTS:
                safe_pname = f"post_img_{current_user.id}_{timestamp}_{orig_pfn}"
                pf.save(os.path.join(upload_folder, safe_pname))
                images_list.append(f"/static/uploads/community/{safe_pname}")

    # 2. Process direct video file uploads (drag-and-drop or file input)
    video_file = request.files.get('video_file')
    if video_file and video_file.filename:
        orig_vfn = secure_filename(video_file.filename)
        vext = orig_vfn.rsplit('.', 1)[-1].lower() if '.' in orig_vfn else ''
        if vext in ALLOWED_VID_EXTS:
            safe_vname = f"post_vid_{current_user.id}_{timestamp}_{orig_vfn}"
            video_file.save(os.path.join(upload_folder, safe_vname))
            media_url = f"/static/uploads/community/{safe_vname}"
            media_type = 'video'

    # 3. Handle media types & embedded URLs
    if media_type == 'instagram':
        raw_ig_url = request.form.get('instagram_url', '').strip()
        if raw_ig_url:
            match = IG_REGEX.search(raw_ig_url)
            if match:
                instagram_shortcode = match.group(1)
                media_url = f"https://www.instagram.com/p/{instagram_shortcode}/"
                aspect_ratio = '4:5'
            else:
                flash('Notice: Make sure your Instagram link is public for the embed to display.', 'info')
                media_url = raw_ig_url
                aspect_ratio = '4:5'
        else:
            flash('Please provide an Instagram post or Reel link.', 'warning')
            return redirect(url_for('community.index'))

    elif media_type in ('youtube', 'youtube_shorts') or (media_type == 'video' and not media_url and any(d in (request.form.get('video_url', '') or request.form.get('youtube_url', '')) for d in ('youtube.com', 'youtu.be'))):
        raw_yt_url = request.form.get('youtube_url', '').strip() or request.form.get('video_url', '').strip() or request.form.get('shorts_url', '').strip()
        if not raw_yt_url and not media_url:
            flash('Please provide a YouTube video or Shorts link.', 'warning')
            return redirect(url_for('community.index'))

        if raw_yt_url:
            shorts_match = YT_SHORTS_REGEX.search(raw_yt_url)
            std_match = YT_VIDEO_REGEX.search(raw_yt_url)

            if shorts_match or (media_type == 'youtube_shorts' and (shorts_match or std_match)):
                y_id = shorts_match.group(1) if shorts_match else (std_match.group(1) if std_match else None)
                if y_id:
                    media_type = 'youtube_shorts'
                    youtube_id = y_id
                    video_format = '9:16'
                    aspect_ratio = '9:16'
                    media_url = f'https://www.youtube-nocookie.com/embed/{youtube_id}'
                else:
                    flash('Could not parse YouTube Shorts link. Please paste a valid YouTube Shorts link.', 'danger')
                    return redirect(url_for('community.index'))
            elif std_match:
                media_type = 'youtube'
                youtube_id = std_match.group(1)
                video_format = '16:9'
                aspect_ratio = '16:9'
                media_url = f'https://www.youtube-nocookie.com/embed/{youtube_id}'
            else:
                flash('Invalid YouTube URL. Please paste a valid YouTube video link (e.g., https://www.youtube.com/watch?v=...).', 'danger')
                return redirect(url_for('community.index'))

    elif media_type == 'video':
        if not media_url:
            raw_vid = request.form.get('video_url', '').strip()
            if raw_vid:
                if 'instagram.com' in raw_vid:
                    ig_m = IG_REGEX.search(raw_vid)
                    if ig_m:
                        media_type = 'instagram'
                        instagram_shortcode = ig_m.group(1)
                        media_url = f"https://www.instagram.com/p/{instagram_shortcode}/"
                        aspect_ratio = '4:5'
                elif 'youtube.com' in raw_vid or 'youtu.be' in raw_vid:
                    yt_m = YT_SHORTS_REGEX.search(raw_vid) or YT_VIDEO_REGEX.search(raw_vid)
                    if yt_m:
                        media_type = 'youtube_shorts' if 'shorts' in raw_vid else 'youtube'
                        youtube_id = yt_m.group(1)
                        video_format = '9:16' if media_type == 'youtube_shorts' else '16:9'
                        aspect_ratio = video_format
                        media_url = f'https://www.youtube-nocookie.com/embed/{youtube_id}'
                else:
                    media_url = raw_vid
                    aspect_ratio = video_format
            else:
                media_url = 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4'
                aspect_ratio = video_format

    elif media_type == 'photo':
        raw_photos = request.form.get('photo_urls', '').strip()
        if raw_photos:
            try:
                parsed = json.loads(raw_photos) if raw_photos.startswith('[') else [u.strip() for u in raw_photos.split(',') if u.strip()]
                for u in parsed:
                    if u and u not in images_list:
                        images_list.append(u)
            except Exception:
                if raw_photos not in images_list:
                    images_list.append(raw_photos)

        single_photo_url = request.form.get('photo_url', '').strip()
        if single_photo_url and single_photo_url not in images_list:
            images_list.append(single_photo_url)

        if not images_list:
            images_list = ['https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800&q=80']

        media_url = images_list[0]

    post = CommunityPost(
        user_id=current_user.id,
        content=content,
        media_type=media_type,
        media_url=media_url,
        instagram_shortcode=instagram_shortcode,
        youtube_id=youtube_id,
        video_format=video_format,
        aspect_ratio=aspect_ratio,
        images=json.dumps(images_list) if images_list else None,
        district_tag=district_tag,
        destination_tag=district_tag,
        likes_count=0
    )
    db.session.add(post)
    db.session.commit()

    flash('Story published to the community!', 'success')
    return redirect(url_for('community.index'))


@bp.route('/<int:post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    existing_like = PostLike.query.filter_by(user_id=current_user.id, post_id=post.id).first()
    
    if existing_like:
        db.session.delete(existing_like)
        post.likes_count = max(0, (post.likes_count or 1) - 1)
        is_liked = False
    else:
        new_like = PostLike(user_id=current_user.id, post_id=post.id)
        db.session.add(new_like)
        post.likes_count = (post.likes_count or 0) + 1
        is_liked = True
    
    db.session.commit()
    
    fill_attr = 'fill="currentColor"' if is_liked else 'fill="none"'
    text_color = 'text-terracotta' if is_liked else 'text-charcoal/60 hover:text-terracotta'
    
    return f'''
    <button hx-post="/community/{post.id}/like" hx-swap="outerHTML"
            class="flex items-center gap-1.5 {text_color} text-xs font-semibold transition-colors focus:outline-none group"
            aria-label="Toggle like">
      <svg class="w-4 h-4 transition-transform active:scale-125 group-hover:scale-110" viewBox="0 0 24 24" {fill_attr} stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
        <path d="M19 14c1.49-1.46 3-3.21 3-5.5A5.5 5.5 0 0 0 16.5 3c-1.76 0-3 .5-4.5 2-1.5-1.5-2.74-2-4.5-2A5.5 5.5 0 0 0 2 8.5c0 2.3 1.5 4.05 3 5.5l7 7Z"/>
      </svg>
      <span>{post.likes_count}</span>
    </button>
    '''


@bp.route('/<int:post_id>/comment', methods=['POST'])
@login_required
def comment_post(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    content = request.form.get('content', '').strip()
    if not content:
        if request.headers.get('HX-Request'):
            return '<div class="text-xs text-terracotta py-1 font-medium">Comment cannot be empty.</div>', 400
        flash('Comment cannot be empty.', 'warning')
        return redirect(url_for('community.index'))

    comment = Comment(
        post_id=post.id,
        user_id=current_user.id,
        content=content
    )
    db.session.add(comment)
    db.session.commit()

    if request.headers.get('HX-Request'):
        return render_template('community/_comment_item.html', comment=comment)

    flash('Comment posted.', 'success')
    return redirect(url_for('community.index'))


@bp.route('/<int:post_id>/flag', methods=['POST'])
@login_required
def flag_post(post_id):
    post = CommunityPost.query.get_or_404(post_id)
    post.is_flagged = True
    db.session.commit()
    return '<span class="text-[11px] text-terracotta font-medium flex items-center gap-1"><i data-lucide="flag" class="w-3 h-3"></i> Flagged for review</span>'

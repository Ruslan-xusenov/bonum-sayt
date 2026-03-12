from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.db import transaction
from django.db.models import Q, F
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import JsonResponse
from django.db.models import Q, F, Count
from .models import Product, Category, CartItem, Banner, Profile, Favorite, Order, OrderItem
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User

def home(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')
    
    products = Product.objects.all().select_related('category').order_by('-created_at')
    
    if query:
        products = products.filter(
            Q(name__icontains=query) | 
            Q(description__icontains=query) |
            Q(keywords__icontains=query)
        )
    
    if category_id:
        products = products.filter(category_id=category_id)
        
    categories = Category.objects.filter(parent=None)
    banners = Banner.objects.filter(is_active=True).order_by('order')
    
    # Get favorite product IDs for the current user/session
    favorite_ids = []
    if request.user.is_authenticated:
        favorite_ids = Favorite.objects.filter(user=request.user).values_list('product_id', flat=True)
    else:
        if not request.session.session_key:
            request.session.create()
        favorite_ids = Favorite.objects.filter(session_key=request.session.session_key).values_list('product_id', flat=True)
    
    return render(request, 'market/index.html', {
        'products': products,
        'categories': categories,
        'banners': banners,
        'query': query,
        'favorite_ids': list(favorite_ids),
    })

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'market/detail.html', {'product': product})

def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    # Simple session-based cart or authenticated user cart
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        # For non-authenticated, use session
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart_item, created = CartItem.objects.get_or_create(session_key=session_key, product=product)
        if not created:
            cart_item.quantity += 1
            cart_item.save()
            
    # Redirect based on 'next' parameter
    next_url = request.GET.get('next')
    if next_url == 'checkout':
        return redirect('market:checkout')
    if next_url == 'cart':
        return redirect('market:cart_view')
        
    return redirect(request.META.get('HTTP_REFERER', 'market:home'))

def cart_view(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
    else:
        guest_uuid = getattr(request, 'guest_uuid', None)
        cart_items = CartItem.objects.filter(guest_uuid=guest_uuid) if guest_uuid else []
        
    total_price = sum(item.total_price for item in cart_items)
    
    return render(request, 'market/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
    })

def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('market:cart_view')

@never_cache
def api_add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    guest_uuid = getattr(request, 'guest_uuid', None)
    
    if request.user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(user=request.user, product=product)
    else:
        # Fallback if middleware didn't set a guest_uuid
        if not guest_uuid:
            import uuid
            guest_uuid = str(uuid.uuid4())
            request.guest_uuid = guest_uuid
            
        cart_item, created = CartItem.objects.get_or_create(guest_uuid=guest_uuid, product=product)
    
    if not created:
        cart_item.quantity = F('quantity') + 1
        cart_item.save()
        cart_item.refresh_from_db()
        
    response = JsonResponse({
        'status': 'ok', 
        'quantity': cart_item.quantity,
        'guest_uuid': str(guest_uuid) if guest_uuid else None
    })
    
    # Ensure guest_uuid cookie is set if we generated one in fallback
    if not request.user.is_authenticated and not request.COOKIES.get('guest_uuid'):
        response.set_cookie('guest_uuid', guest_uuid, max_age=365*24*60*60)
        
    return response

@never_cache
def get_cart_items(request):
    guest_uuid = getattr(request, 'guest_uuid', None)
    
    print(f"DEBUG: get_cart_items user={request.user}, guest={guest_uuid}")
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        print(f"DEBUG: Found {cart_items.count()} items for user")
    else:
        cart_items = CartItem.objects.filter(guest_uuid=guest_uuid) if guest_uuid else []
        print(f"DEBUG: Found {cart_items.count() if hasattr(cart_items, 'count') else 0} items for guest")
        
    items_data = []
    total_price = 0
    for item in cart_items:
        items_data.append({
            'id': item.id,
            'name': item.product.name,
            'price': str(item.product.price),
            'quantity': item.quantity,
            'total_price': str(item.total_price),
            'image_url': item.product.image.url if item.product.image else 'https://via.placeholder.com/100x130'
        })
        total_price += item.total_price
        
    return JsonResponse({
        'items': items_data,
        'total_price': str(total_price),
        'count': cart_items.count() if hasattr(cart_items, 'count') else len(cart_items),
        'guest_uuid': str(guest_uuid) if guest_uuid else None
    })

@never_cache
@require_POST
def api_update_cart_quantity(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    
    # Check ownership
    guest_uuid_str = request.COOKIES.get('guest_uuid')
    if request.user.is_authenticated:
        if cart_item.user != request.user:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
    else:
        if not guest_uuid_str or str(cart_item.guest_uuid) != guest_uuid_str:
            return JsonResponse({'status': 'error', 'message': 'Unauthorized'}, status=403)
            
    action = request.POST.get('action')
    if action == 'increment':
        cart_item.quantity += 1
    elif action == 'decrement':
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
        else:
            cart_item.delete()
            return JsonResponse({'status': 'removed'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid action'}, status=400)
        
    cart_item.save()
    return JsonResponse({
        'status': 'ok',
        'quantity': cart_item.quantity,
        'total_price': float(cart_item.total_price)
    })

# Admin Dashboard Views
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            return redirect('/django-secret-admin/login/?next=/adminnn/')
        return view_func(request, *args, **kwargs)
    return wrapper

@admin_required
def admin_dashboard(request):
    # Optimize product & category fetching
    products = Product.objects.all().select_related('category').order_by('-created_at')
    categories = Category.objects.all().annotate(p_count=Count('products'))
    banners = Banner.objects.all().order_by('order')
    
    # Base Order Queryset with optimizations
    orders_base = Order.objects.all().annotate(
        items_count=Count('items')
    ).select_related('user').prefetch_related('items__product').order_by('-created_at')

    orders_yangi = orders_base.filter(status='yangi')
    orders_tasdiqlangan = orders_base.filter(status='tasdiqlangan')
    orders_bekor = orders_base.filter(status='bekor')
    orders_kuryer = orders_base.filter(status='kuryer')
    
    # Customer optimization
    users = User.objects.all().annotate(
        cart_count=Count('cart_items', distinct=True),
        fav_count=Count('favorites', distinct=True)
    ).select_related('profile').order_by('-date_joined')
    
    return render(request, 'market/admin_dashboard.html', {
        'products': products,
        'categories': categories,
        'banners': banners,
        'orders_yangi': orders_yangi,
        'orders_tasdiqlangan': orders_tasdiqlangan,
        'orders_bekor': orders_bekor,
        'orders_kuryer': orders_kuryer,
        'users_list': users,
    })

@admin_required
def admin_add_banner(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        subtitle = request.POST.get('subtitle') or request.POST.get('description', '')
        link = request.POST.get('link') or request.POST.get('button_text') or '#'
        order = request.POST.get('order', 0)
        
        banner_data = {
            'title': title,
            'subtitle': subtitle,
            'link': link,
            'order': order,
        }
        
        if request.FILES.get('image'):
            banner_data['image'] = request.FILES['image']
            
        Banner.objects.create(**banner_data)
        
        return redirect('market:admin_dashboard')
    
    return render(request, 'market/admin_add_banner.html')

@admin_required
def admin_edit_banner(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    
    if request.method == 'POST':
        banner.title = request.POST.get('title')
        banner.subtitle = request.POST.get('subtitle') or request.POST.get('description', banner.subtitle)
        banner.link = request.POST.get('link') or request.POST.get('button_text') or banner.link
        banner.order = request.POST.get('order', 0)
        banner.is_active = request.POST.get('is_active') == 'on'
        
        if request.FILES.get('image'):
            banner.image = request.FILES['image']
        
        banner.save()
        return redirect('market:admin_dashboard')
    
    return render(request, 'market/admin_edit_banner.html', {'banner': banner})

@admin_required
def admin_delete_banner(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    banner.delete()
    return redirect('market:admin_dashboard')

# Category Management
@admin_required
def admin_add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        
        category = Category.objects.create(
            name=name,
            parent_id=parent_id if parent_id else None
        )
        
        if request.FILES.get('icon'):
            category.icon = request.FILES['icon']
            category.save()
            
        return redirect('market:admin_dashboard')
        
    categories = Category.objects.filter(parent=None)
    return render(request, 'market/admin_add_category.html', {'categories': categories})

@admin_required
def admin_edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        category.parent_id = parent_id if parent_id else None
        
        if request.FILES.get('icon'):
            category.icon = request.FILES['icon']
            
        category.save()
        return redirect('market:admin_dashboard')
        
    categories = Category.objects.filter(parent=None).exclude(pk=pk)
    return render(request, 'market/admin_edit_category.html', {
        'category': category,
        'categories': categories
    })

@admin_required
def admin_delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('market:admin_dashboard')

# Product Management
@admin_required
def admin_add_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        old_price = request.POST.get('old_price')
        brand = request.POST.get('brand')
        category_id = request.POST.get('category')
        stock = request.POST.get('stock', 0)
        image_url = request.POST.get('image_url')
        
        product = Product.objects.create(
            name=name,
            brand=brand,
            description=description,
            price=price,
            old_price=old_price if old_price else None,
            category_id=category_id,
            stock=stock,
            image_url=image_url if image_url else None
        )
        
        if request.FILES.get('image'):
            product.image = request.FILES['image']
            product.save()
        
        return redirect('market:admin_dashboard')
    
    categories = Category.objects.all()
    return render(request, 'market/admin_add_product.html', {'categories': categories})

@admin_required
def admin_edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        product.name = request.POST.get('name')
        product.brand = request.POST.get('brand')
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.old_price = request.POST.get('old_price') if request.POST.get('old_price') else None
        product.category_id = request.POST.get('category')
        product.stock = request.POST.get('stock', 0)
        product.image_url = request.POST.get('image_url')
        
        if request.FILES.get('image'):
            product.image = request.FILES['image']
        
        product.save()
        return redirect('market:admin_dashboard')
    
    categories = Category.objects.all()
    return render(request, 'market/admin_edit_product.html', {
        'product': product,
        'categories': categories,
    })

@admin_required
def admin_delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('market:admin_dashboard')

# User Profile
@login_required
def complete_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    # If already complete, redirect to home
    is_complete = (
        request.user.first_name and
        profile.phone_number and
        profile.address
    )
    if is_complete:
        return redirect('market:home')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', 'User').strip()
        phone = request.POST.get('phone', '').strip()
        address = request.POST.get('address', '').strip()

        # Auto-prepend +998 if not present
        if phone and not phone.startswith('+'):
            phone = '+998' + phone

        request.user.first_name = first_name
        request.user.last_name = last_name or 'User'
        request.user.save()

        profile.phone_number = phone
        profile.address = address
        profile.save()

        return redirect('market:home')

    return render(request, 'market/complete_profile.html')
def toggle_favorite(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.user.is_authenticated:
        favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True
    else:
        if not request.session.session_key:
            request.session.create()
        favorite, created = Favorite.objects.get_or_create(session_key=request.session.session_key, product=product)
        if not created:
            favorite.delete()
            is_favorite = False
        else:
            is_favorite = True
            
    return JsonResponse({'is_favorite': is_favorite})

def get_favorites(request):
    if request.user.is_authenticated:
        favorites = Favorite.objects.filter(user=request.user).select_related('product')
    else:
        if not request.session.session_key:
            request.session.create()
        favorites = Favorite.objects.filter(session_key=request.session.session_key).select_related('product')
        
    items = []
    for fav in favorites:
        items.append({
            'id': fav.product.id,
            'name': fav.product.name,
            'price': float(fav.product.price),
            'image_url': fav.product.image.url
        })
    return JsonResponse({'items': items})
@transaction.atomic
def checkout(request):
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user).select_related('product')
    else:
        guest_uuid = getattr(request, 'guest_uuid', None)
        if not guest_uuid:
            return redirect('market:cart_view')
        cart_items = CartItem.objects.filter(guest_uuid=guest_uuid).select_related('product')
        
    if not cart_items.exists():
        return redirect('market:cart_view')
    
    total_amount = sum(item.total_price for item in cart_items)
    
    # Get profile for authenticated users
    profile = getattr(request.user, 'profile', None) if request.user.is_authenticated else None
    
    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone_raw = request.POST.get('phone_number', '')
        # Clean phone number: remove spaces and common separators
        phone_number = phone_raw.replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
        address = request.POST.get('address', '').strip()
        
        if not full_name or not phone_number or not address:
            from django.contrib import messages
            messages.error(request, "Iltimos, barcha maydonlarni to'ldiring")
            return redirect('market:checkout')
        
        try:
            # Create Order
            order_data = {
                'full_name': full_name,
                'phone_number': phone_number,
                'address': address,
                'total_amount': 0 # Calculate after stock check
            }
            
            if request.user.is_authenticated:
                order_data['user'] = request.user
            else:
                order_data['guest_uuid'] = request.guest_uuid
                
            order = Order.objects.create(**order_data)
            
            calc_total = 0
            for item in cart_items:
                # Critical: Lock product for update
                product = Product.objects.select_for_update().get(pk=item.product.pk)
                
                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=product.price
                )
                
                calc_total += product.price * item.quantity
            
            order.total_amount = calc_total
            order.save()
            
            # Clear cart
            cart_items.delete()
            
            return render(request, 'market/order_success.html', {'order': order})
            
        except Exception as e:
            # The transaction will automatically rollback
            from django.contrib import messages
            error_msg = str(e)
            
            # If it's a validation error (phone number), stay on checkout
            if "phone_number" in error_msg.lower():
                error_msg = "Telefon raqami noto'g'ri formatda. Iltimos, +998901234567 formatida kiriting."
                messages.error(request, error_msg)
                return redirect('market:checkout')
            
            # For other errors (like stock shortage), go back to cart to adjust quantity
            messages.error(request, error_msg)
            return redirect('market:cart_view')
        
    return render(request, 'market/checkout.html', {
        'cart_items': cart_items,
        'total_amount': total_amount,
        'profile': profile
    })

@login_required
def get_user_profile(request):
    user = request.user
    profile = user.profile
    
    # Get recent orders
    orders_qs = Order.objects.filter(user=user).order_by('-created_at')[:5]
    orders_data = []
    
    for order in orders_qs:
        items = []
        for item in order.items.all():
            items.append({
                'product_name': item.product.name,
                'image_url': item.product.image.url if item.product.image else None,
                'price': float(item.price),
                'quantity': item.quantity
            })
        
        orders_data.append({
            'id': order.id,
            'total_amount': float(order.total_amount),
            'status': order.status,
            'user_note': order.user_note or '',
            'created_at': order.created_at.strftime("%d.%m.%Y"),
            'items': items
        })
    
    data = {
        'first_name': user.first_name,
        'phone_number': profile.phone_number,
        'address': profile.address,
        'orders': orders_data
    }
    return JsonResponse(data)

@login_required
@require_POST
def add_order_note(request, pk):
    order = get_object_or_404(Order, pk=pk, user=request.user)
    note = request.POST.get('note', '')
    order.user_note = note
    order.save()
    return JsonResponse({'status': 'ok'})

@login_required
@require_POST
def update_profile_api(request):
    user = request.user
    profile = user.profile
    
    first_name = request.POST.get('first_name')
    phone_number = request.POST.get('phone_number')
    address = request.POST.get('address')
    
    if first_name:
        user.first_name = first_name
        user.save()
    
    if phone_number:
        profile.phone_number = phone_number
    if address:
        profile.address = address
    profile.save()
    
    return JsonResponse({'status': 'ok'})

@admin_required
def update_order_status(request, pk, status):
    order = get_object_or_404(Order, pk=pk)
    if status in dict(Order.STATUS_CHOICES):
        order.status = status
        order.save()
    return redirect('market:admin_dashboard')
